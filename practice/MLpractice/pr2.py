# PythonML Practice 2: 다항 규제 회귀 기반 성적 예측
# 데이터 출처: https://www.kaggle.com/datasets/shambhurajejagadale/student-performance-prediction-dataset
# 1. 데이터 준비 및 전처리
#  - Kaggle 데이터셋을 불러옵니다.
import numpy as np
import pandas as pd
df = pd.read_csv('practice/MLpractice/student_dataset_10000_rows.csv')
df.info()
#  - 범주형 변수를 제외한 6개 수치형 컬럼을 독립변수(X, 문제지)로 추출하세요:
#    ['study_hours', 'attendance', 'sleep_hours', 'internet_usage', 'assignments_completed', 'previous_score']
x =  df[['study_hours', 'attendance', 'sleep_hours', 'internet_usage', 'assignments_completed', 'previous_score']]
#  - 시험 성적인 'exam_score' 컬럼을 종속변수(Y, 정답지)로 설정하세요.
y = df['exam_score']

# 2. 데이터 분할
#  - train_test_split을 사용하여 훈련 세트(80%)와 테스트 세트(20%)로 분할하세요.
#  - 재현성을 위해 random_state=42로 고정합니다.
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train , Y_test = train_test_split( x, y, test_size=0.2, random_state=42)


# 3. 다항 특성 확장 및 표준화 (고정 차수: degree=2)
#  - PolynomialFeatures(degree=2, include_bias=False)를 사용하여 2차 다항 특성을 생성하세요.
#    * 훈련 세트(X_train)로만 .fit()을 수행하고, X_train과 X_test를 각각 .transform() 하세요.
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures( include_bias = False )
poly.fit(X_train)
X_train_poly = poly.transform(X_train)
X_test_poly = poly.transform(X_test)
print(X_train.shape)            # (8000, 6)
print( X_train_poly.shape)      # (8000, 27)
print(X_test.shape)             # (2000, 6)
print( X_test_poly.shape)       # (2000, 27)

#  - StandardScaler를 생성하고, 다항 확장된 훈련 세트(X_train_poly) 기준으로 .fit()한 뒤 표준 점수로 변환하세요.
#    * 특성 간 스케일 차이를 맞추기 위해 훈련 세트와 테스트 세트 모두 .transform() 하세요.
from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
ss.fit( X_train_poly )
X_train_scaled = ss.transform( X_train_poly )
X_test_scaled = ss.transform( X_test_poly)
print( X_train_poly[0])    # [  11.   58.    5. ~ ]
print( X_train_scaled[0])   # [ 1.57957213 -0.67513979 -0.88741767  ~  ]



# 4. 3가지 모델 학습 및 결정계수(R²) 비교 (고정 규제: alpha=1.0)
#  - 3가지 회귀 모델을 각각 생성하고 스케일링된 훈련 데이터로 학습시키세요:
from sklearn.metrics import r2_score
#    1) LinearRegression()
from sklearn.linear_model import LinearRegression
model1 = LinearRegression()
model1.fit(X_train_scaled , Y_train)
Y_pred1 = model1.predict( X_train_scaled )


#    2) Ridge(alpha=1.0, random_state=42)
from sklearn.linear_model import Ridge
model2 = Ridge( alpha=1.0 , random_state=42 )
model2.fit(X_train_scaled , Y_train)
Y_pred2 = model2.predict( X_train_scaled )


#    3) Lasso(alpha=1.0, random_state=42)
from sklearn.linear_model import Lasso
model3 = Lasso( alpha=1.0, random_state=42)
model3.fit(X_train_scaled , Y_train)
Y_pred3 = model3.predict( X_train_scaled )

#  - 각 모델별 훈련 세트 R² 점수(Train R²)와 테스트 세트 R² 점수(Test R²)를 각각 산출하여 비교 출력하세요.
print('LinearRegression model - Train R² : ' , model1.score( X_train_scaled , Y_train ) )
print('LinearRegression model - Test R² : ' , model1.score( X_test_scaled , Y_test ) )
print('Ridge model - Train R² : ' , model2.score( X_train_scaled , Y_train ) )
print('Ridge model - Test R² : ' , model2.score( X_test_scaled , Y_test ) )
print('Lasso model - Train R² : ' , model3.score( X_train_scaled , Y_train ) )
print('Lasso model - Test R² : ' , model3.score( X_test_scaled , Y_test ) )


# 5. 임의 대조군 데이터에 대한 3가지 모델 예측 비교
#  - 아래 대조군 샘플 2개를 준비하세요:
#    * 샘플 1 (상위권): study_hours=9, attendance=95, sleep_hours=7, internet_usage=2, assignments_completed=18, previous_score=85
high = pd.DataFrame([{'study_hours': 9,'attendance': 95,'sleep_hours': 7,'internet_usage': 2,'assignments_completed': 18,'previous_score': 85}])
#    * 샘플 2 (하위권): study_hours=2, attendance=60, sleep_hours=5, internet_usage=9, assignments_completed=4, previous_score=50
low = pd.DataFrame([{'study_hours': 2,'attendance': 60,'sleep_hours': 5,'internet_usage': 9,'assignments_completed': 4,'previous_score': 50}])
#  - 각 샘플 데이터를 앞서 학습시킨 동일한 변환기(PolynomialFeatures, StandardScaler)로 변환하세요.
high = poly.transform(high)
low = poly.transform(low)
high = ss.transform(high)
low = ss.transform(low)

#  - 3가지 모델(LinearRegression, Ridge, Lasso)에 변환된 데이터를 각각 대입하여 예상 시험 성적을 산출하고 비교 출력하세요.
print('LinearRegression(상위권) : ' , model1.predict(high) )
print('Ridge(상위권) : ' , model2.predict(high) )
print('Lasso(상위권) : ' , model3.predict(high) )
print('LinearRegression(하위권) : ' , model1.predict(low) )
print('Ridge(하위권) : ' , model2.predict(low) )
print('Lasso(하위권) : ' , model3.predict(low) )

print( '# ===================== 결과값 보정 ======================')

print('LinearRegression(상위권) : ' , np.clip(model1.predict(high), 0 , 100 ) )
print('Ridge(상위권) : ' , model2.predict(high) )
print('Lasso(상위권) : ' , model3.predict(high) )

print( '# ===================시각화====================================')