# PythonML Practice4: 로지스틱 이진 분류 (Logistic Regression)
# 데이터 출처: https://www.kaggle.com/datasets/uciml/breast-cancer-wisconsin-data
#
# [단계 1] 데이터 로드 및 전처리, 독립/종속 변수 추출
# 파일명: ./data.csv
# 1. 식별자('id') 및 결측 열('Unnamed: 32')이 존재한다면 제외합니다.
# 2. 'diagnosis' 열을 종속 변수 y로 추출하고, 악성(M)은 1, 양성(B)은 0으로 매핑(변환)하세요.
# 3. 'diagnosis'를 제외한 30개의 수치형 피처를 독립 변수 X로 추출하세요.
import pandas as pd
df = pd.read_csv('MLpractice/data.csv')
# # id 컬럼 드롭 및 전체가 결측치(NaN)인 열 자동 제거
df = df.drop(columns=['id'])
df = df.dropna(axis=1, how='all') # Unnamed: 32 등 모든 값이 NaN인 열을 자동으로 날립니다.
# # 종속 변수(문자열 'M', 'B' 유지) 및 독립 변수 분리
Y = df['diagnosis'].map({'M':1 , 'B' : 0 })
X = df.drop(columns=['diagnosis'])

# [단계 2] 훈련용 / 테스트용 데이터 분리
# train_test_split을 사용하여 8:2 비율(test_size=0.2)로 분리하고,
# 재현성을 위해 random_state=42, 클래스 비율 유지를 위해 stratify=y로 설정하세요.
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train , Y_test = train_test_split( X , Y , test_size = 0.2 , random_state = 42 , stratify=Y)



# [단계 3] 데이터 표준화 (Standardization)
# StandardScaler를 활용하여 훈련 데이터(X_train) 기준으로 스케일러를 학습(fit)시키고,
# X_train과 X_test를 각각 표준화(transform) 변환하세요.
from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
ss.fit(X_train)
X_train_scaled = ss.transform( X_train )
X_test_scaled = ss.transform( X_test )




# [단계 4] 로지스틱 회귀 모델 학습 (Logistic Regression)
# LogisticRegression() 모델을 생성하고 훈련 세트(X_train_scaled, y_train)로 학습시키세요.
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train_scaled , Y_train )

#
# [단계 5] 모델 평가 및 분류 정확도(Accuracy) 확인
# 테스트 세트에 대한 예측을 수행하고 정확도(accuracy_score)를 출력하세요.
from sklearn.metrics import accuracy_score
Y_pred = model.predict( X_test_scaled )
acc = accuracy_score(Y_test , Y_pred)
print( '정확도' , acc )


print( model.classes_ ) 
# [단계 6] 샘플 데이터 예측 및 예측 확률 확인
# 테스트 세트의 앞선 3개 샘플 데이터에 대해:
# 1. 모델이 예측한 클래스(0 또는 1)를 출력하세요.
print(Y_pred)
# 2. 각 샘플별 양성(0)/악성(1) 클래스에 대한 예측 확률(predict_proba)을 출력하세요.
print(model.predict_proba(X_test_scaled[:3]))
