# [역할] 학습 전용 파일: CSV → X/Y 분리 → 전처리 → Ridge 학습 → 평가 → 저장
# 수업 참고: day15/s-08.py의 ColumnTransformer/Pipeline, mpractice3.py의 Ridge/GridSearchCV
# 이 파일은 모델을 처음 준비할 때 별도로 실행합니다. API 요청 시에는 실행하지 않습니다.
from pathlib import Path
import hashlib
import joblib
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV, GroupKFold, GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def train_model():
    base_dir = Path(__file__).resolve().parent
    # team 폴더의 회복 데이터 원본을 읽기만 합니다.
    csv_path = base_dir.parent / "athlete_recovery_synthetic.csv"
    model_dir = base_dir / "models"
    model_path = model_dir / "recovery_model.pkl"
    metrics_path = model_dir / "recovery_metrics.pkl"

    # 1. 확인: 팀원이 제공한 기존 모델 또는 지표를 덮어쓰지 않습니다.
    if model_path.exists() or metrics_path.exists():
        raise FileExistsError("기존 모델 또는 성능 지표가 있습니다. 재학습 전 별도로 보관해 주세요.")

    # 2. 분리: 확정된 8개 X와 회복 점수 Y만 사용합니다. 선수 ID는 분할에만 사용합니다.
    columns = [
        "Age", "Gender", "Training_Duration_Min", "Training_Intensity",
        "Sleep_Duration_Hours", "Stress_Level", "Caffeine_Intake_mg", "Muscle_Soreness",
    ]
    num_features = [
        "Age", "Training_Duration_Min", "Training_Intensity",
        "Sleep_Duration_Hours", "Caffeine_Intake_mg", "Muscle_Soreness",
    ]
    cat_features = ["Gender", "Stress_Level"]
    df = pd.read_csv(csv_path)
    X = df[columns]             # 문제지: 예측에 사용할 8개 입력 특성
    Y = df["Recovery_Score"]    # 정답지: 실제 회복 점수
    groups = df["Athlete_ID"]
    # [데이터 특성에 따른 보완] train_test_split처럼 훈련/테스트를 나누되 선수별로 묶습니다.
    # 같은 선수의 다른 날 기록이 학습과 테스트에 섞이지 않도록 나눕니다.
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    # split()이 돌려주는 분할 중 첫 번째(한 번의 분할)의 행 위치를 가져옵니다.
    train_index, test_index = next(splitter.split(X, Y, groups))
    # iloc은 행의 정수 위치로 데이터를 선택합니다. 행 이름을 사용하는 loc과 구분합니다.
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    Y_train, Y_test = Y.iloc[train_index], Y.iloc[test_index]
    train_groups, test_groups = groups.iloc[train_index], groups.iloc[test_index]

    # 3. 전처리: 중앙값과 최빈값은 훈련 데이터에서만 학습합니다.
    # 성별과 스트레스 결측값도 학습된 최빈값으로 대체한 뒤 원-핫 인코딩합니다.
    # median: 중앙값으로 결측값 대체 → scaler: 수치형 특성의 단위를 표준화
    num_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    # most_frequent: 최빈값 대체 → encoder: 문자열 범주를 숫자 열로 변환
    cat_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    # ('식별자', 변환기, 적용할 컬럼 목록) 구조는 수업 코드와 같습니다.
    pp = ColumnTransformer(transformers=[
        ("num", num_pipe, num_features),
        ("cat", cat_pipe, cat_features),
    ])
    # 원본 X를 넣으면 pp 전처리 후 model 회귀가 순서대로 실행됩니다.
    pipe = Pipeline([("pp", pp), ("model", Ridge())])

    # 4. 학습: 교차 검증 안에서도 전처리를 함께 학습해 데이터 누수를 방지합니다.
    # 교차 검증도 같은 선수가 두 집합에 섞이지 않도록 그룹을 유지합니다.
    cv = GroupKFold(n_splits=5)
    # model은 Pipeline의 단계 이름, alpha는 Ridge의 규제 강도입니다.
    # 두 밑줄 __은 Pipeline 안의 model 단계에 있는 alpha를 지정하는 문법입니다.
    param_grid = {"model__alpha": [0.01, 0.1, 1.0, 10.0, 100.0]}
    # 수업용 PC에서 불필요한 다중 프로세스 생성을 피하도록 한 작업씩 실행합니다.
    grid = GridSearchCV(pipe, param_grid, cv=cv, scoring="r2", n_jobs=1, error_score="raise")
    grid.fit(X_train, Y_train, groups=train_groups)
    best_model = grid.best_estimator_  # 가장 좋은 alpha로 훈련 데이터에 다시 학습한 Pipeline

    # 5. 평가: 학습과 alpha 탐색에 포함하지 않은 선수들의 원본 예측값으로 평가합니다.
    Y_pred = best_model.predict(X_test)
    # 두 입력의 순서: 실제 정답 Y_test, 모델의 예측 Y_pred
    test_r2 = float(r2_score(Y_test, Y_pred))
    test_mae = float(mean_absolute_error(Y_test, Y_pred))
    # 중첩 딕셔너리도 축약식 대신 for문으로 만들어 각 단계가 보이도록 합니다.
    training_ranges = {}
    for column in num_features:
        training_ranges[column] = {
            "min": float(X_train[column].min()),
            "max": float(X_train[column].max()),
        }
    metrics = {
        "r2_score": test_r2,
        "mae": test_mae,
        "input_columns": columns,
        "target_column": "Recovery_Score",
        "best_alpha": grid.best_params_["model__alpha"],
        "cv_r2_score": float(grid.best_score_),
        "train_rows": len(X_train),
        "test_rows": len(X_test),
        "test_size": 0.2,
        "random_state": 42,
        "split_method": "GroupShuffleSplit + GroupKFold (Athlete_ID)",
        "train_athlete_ids": sorted(train_groups.unique().tolist()),
        "test_athlete_ids": sorted(test_groups.unique().tolist()),
        "training_ranges": training_ranges,
        "sklearn_version": sklearn.__version__,
        "csv_sha256": hashlib.sha256(csv_path.read_bytes()).hexdigest(),
    }

    # 6. 저장: 원본 CSV는 읽기만 하며, Pipeline 전체와 실제 평가 결과를 저장합니다.
    # 기존 models 폴더에 사용자에게 승인받은 회복 모델 결과 2개만 생성합니다.
    # xb: 새 바이너리 파일만 생성합니다. with문이 끝나면 파일은 자동으로 닫힙니다.
    # 이미 존재하는 파일은 실패하므로 기존 학습 결과를 덮어쓰지 않습니다.
    with model_path.open("xb") as file:
        joblib.dump(best_model, file)
    with metrics_path.open("xb") as file:
        joblib.dump(metrics, file)
    print("Saved: models/recovery_model.pkl, models/recovery_metrics.pkl")
    print("Best alpha:", metrics["best_alpha"])
    print("Test R2:", metrics["r2_score"])
    print("Test MAE:", metrics["mae"])


if __name__ == "__main__":
    train_model()
