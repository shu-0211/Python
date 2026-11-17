import joblib
import pandas as pd
# 학습 시킨 모델 가져오기 
saved_data = joblib.load('./day19/lgbm_insurance_model.pkl')
model = saved_data['model']

class ModelService : 
    # 생성자 
    
    # 받은 값을 모델에 넣고 쌀뭔지 확인
    def check( paramete ) : 
        checkDf = pd.DataFrame( [paramete] )
        pred = model.predict(checkDf)
        return pred

model_service = ModelService()