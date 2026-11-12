# 저장된 회복 모델을 읽고 예측 점수와 테스트 지표를 반환합니다.
import math
from threading import Lock

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline

from recovery_data import CATEGORY_CODES, FEATURE_COLUMNS, MODEL_PATH, split_recovery_data


class RecoveryService:
    def __init__(self):
        self.model_path = MODEL_PATH
        self.columns = FEATURE_COLUMNS
        self.model = None
        self.metrics = None
        self._load_lock = Lock()

    def load_model(self):
        with self._load_lock:
            if self.model is not None:
                return

            model = joblib.load(self.model_path)
            if not isinstance(model, Pipeline):
                raise ValueError("전처리를 포함한 학습 Pipeline이 필요합니다.")
            if list(getattr(model, "feature_names_in_", [])) != self.columns:
                raise ValueError("모델의 원본 입력 컬럼과 API 컬럼 순서가 다릅니다.")

            # 최초 요청에서 team.py와 같은 테스트 분할로 저장 모델을 평가합니다.
            X_train, X_test, _, y_test = split_recovery_data()
            predictions = model.predict(X_test)
            training_ranges = {}
            for column in self.columns:
                if column not in CATEGORY_CODES:
                    training_ranges[column] = (X_train[column].min(), X_train[column].max())

            self.metrics = {
                "r2_score": float(r2_score(y_test, predictions)),
                "mae": float(mean_absolute_error(y_test, predictions)),
                "training_ranges": training_ranges,
            }
            self.model = model

    def predict(self, data):
        self.load_model()

        # 폼의 범주 문자열을 학습 때 사용한 숫자로 바꿉니다.
        row = data.copy()
        for column, codes in CATEGORY_CODES.items():
            row[column] = codes[data[column]]
        df = pd.DataFrame([row], columns=self.columns)

        with np.errstate(over="raise", invalid="raise"):
            raw_prediction = float(self.model.predict(df)[0])
        if not math.isfinite(raw_prediction):
            raise ArithmeticError("모델이 유한하지 않은 회복 점수를 예측했습니다.")
        score = min(100.0, max(0.0, raw_prediction))

        warnings = []
        for column, (minimum, maximum) in self.metrics["training_ranges"].items():
            if not minimum <= data[column] <= maximum:
                warnings.append(f"{column}: 학습 데이터 범위({minimum}~{maximum}) 밖의 입력입니다.")

        return {
            "predicted_recovery_score": score,
            "raw_prediction": raw_prediction,
            "score_was_clipped": score != raw_prediction,
            "r2_score": self.metrics["r2_score"],
            "mae": self.metrics["mae"],
            "warnings": warnings,
        }


# 수업 예제의 item_service = ItemService()와 같은 구조입니다.
# Controller는 이 객체를 import해서 recovery_service.predict()를 호출합니다.
recovery_service = RecoveryService()
