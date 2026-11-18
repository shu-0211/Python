import joblib
import pandas as pd
# 학습 시킨 모델 가져오기 
saved_data = joblib.load('./lgbm_insurance_model.pkl')
model = saved_data['model']

class ModelService : 
    # 생성자 
    def __init__(self):
            # self.변수명 = 값 # 맴버변수 선어 
            self.df = pd.DataFrame([
                {
                        "Area": 15231,
                        "Perimeter": 525.5789794921875,
                        "Major_Axis_Length": 229.7498779296875,
                        "Minor_Axis_Length": 85.09378814697266,
                        "Eccentricity": 0.9288820028305054,
                        "Convex_Area": 15617,
                        "Extent": 0.5728955268859863
                    },
                    {
                        "Area": 14656,
                        "Perimeter": 494.3110046386719,
                        "Major_Axis_Length": 206.0200653076172,
                        "Minor_Axis_Length": 91.73097229003906,
                        "Eccentricity": 0.8954049944877625,
                        "Convex_Area": 15072,
                        "Extent": 0.615436315536499
                    },
                    {
                        "Area": 13447,
                        "Perimeter": 455.64801025390625,
                        "Major_Axis_Length": 183.95758056640625,
                        "Minor_Axis_Length": 94.45813751220703,
                        "Eccentricity": 0.8581028580665588,
                        "Convex_Area": 13867,
                        "Extent": 0.6259076595306396
                    }
            ])
    
    # 받은 값을 모델에 넣고 쌀뭔지 확인
    @staticmethod
    def check( paramete ) : 
        # 모델 학습에 사용한 순서대로 입력 열을 맞춥니다.
        checkDf = pd.DataFrame( [paramete] )[model.feature_names_in_]
        pred = model.predict(checkDf)
        proba = model.predict_proba(checkDf)[0]
        probabilities = {
            str(name): float(probability)
            for name, probability in zip(model.classes_, proba)
        }
        return {"prediction": str(pred[0]), "probabilities": probabilities}

model_service = ModelService()
