
# Athlete_ID   운동선수 ID   운동선수 고유 식별번호
# Day   일차   운동 기록 일차
# Day_of_Week   요일   운동한 요일
# Week   주차   운동 기록 주차
# Age   나이   운동선수의 나이
# Gender   성별   남성 / 여성
# Sport_Type   운동 종목   축구, 농구, 달리기 등
# Training_Type   훈련 유형   근력 운동, 유산소 운동 등
# Training_Duration_Min   운동 시간   운동한 시간(분)
# Training_Intensity   운동 강도   운동의 강도 수준
# Sleep_Duration_Hours   수면 시간   수면한 시간(시간)
# Caffeine_Intake_mg   카페인 섭취량   섭취한 카페인 양(mg)
# Stress_Level   스트레스 수준   스트레스 정도
# Resting_Heart_Rate   안정 시 심박수   휴식 상태의 분당 심박수(bpm)
# HRV_ms   심박변이도   심장 박동 간 시간 변동(ms)
# Mood_Score   기분 점수   기분 상태를 나타내는 점수
# Muscle_Soreness   근육통 정도   운동 후 근육통 수준
# Energy_Level   에너지 수준   신체의 활력 및 에너지 상태
# Recovery_Score   회복 점수   운동 후 신체 회복 상태 점수


#============================
# | --------------------- | ----------- |
# | Age                   | 나이          |
# | Gender                | 성별          |
# | Training_Duration_Min | 운동 시간(분)    |
# | Training_Intensity    | 운동 강도       |
# | Sleep_Duration_Hours  | 수면 시간(시간)   |
# | Stress_Level          | 스트레스 수준     |
# | Caffeine_Intake_mg    | 카페인 섭취량(mg) |
# | Muscle_Soreness       | 근육통 정도      |

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures, StandardScaler


df = pd.read_csv("day16/team/athlete_recovery_synthetic.csv")

feature_cols = [
    "Age",
    "Gender",
    "Training_Duration_Min",
    "Training_Intensity",
    "Sleep_Duration_Hours",
    "Stress_Level",
    "Caffeine_Intake_mg",
    "Muscle_Soreness",
]
target_col = "Recovery_Score"

# 성별 , 스트레스 지수 숫자로 변환
# 1. Gender는 2개뿐이므로 기존 방식 그대로 유지해도 원핫인코딩과 동일합니다.
df["Gender"] = df["Gender"].map({"Male": 0, "Female": 1})

# 2. Stress_Level(및 Training_Intensity 등 3개 이상 범주) 원핫인코딩
df = pd.get_dummies(df, columns=["Stress_Level"], drop_first=True, dtype=int)


# 타겟이 결측치가 있는 행 삭제
df = df.dropna(subset=[target_col])
X = df[feature_cols]



# 결측치 있는 값 확인
print( "결측치 있는 값 확인" )
print(X.isna().sum())

# Age                        0
# Gender                   252
# Training_Duration_Min      0
# Training_Intensity         1
# Sleep_Duration_Hours     604
# Stress_Level               0
# Caffeine_Intake_mg         0
# Muscle_Soreness            0

print("특성 데이터 행 수:", X.shape[0])
df = df.dropna()

X = X.dropna(subset=["Gender", "Training_Intensity", "Sleep_Duration_Hours"])


# X["Gender"] = X["Gender"].fillna(X["Gender"].median())
# X["Training_Intensity"] = X["Training_Intensity"].fillna(X["Training_Intensity"].median())
# X["Sleep_Duration_Hours"] = X["Sleep_Duration_Hours"].fillna(X["Sleep_Duration_Hours"].mean())

print( "결측치 있는 값 확인" )
print(X.isna().sum())

# Age                      0
# Gender                   0
# Training_Duration_Min    0
# Training_Intensity       0
# Sleep_Duration_Hours     0
# Stress_Level             0
# Caffeine_Intake_mg       0
# Muscle_Soreness          0

print("특성 데이터 행 수:", X.shape[0])
Y = df["Recovery_Score"]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# 4) 과소적합 방지 하고자 항 추가 PolynomialFeatures   -> 제곱 / 곱셈 자동으로 다해줌
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures( degree=2 , include_bias=False )     # include_bias=False 1을 생성하지 않음
poly.fit(X_train)
X_train_poly = poly.transform( X_train )
X_test_poly = poly.transform( X_test )

# 5) 항 많아지면 항/특성 간에 단위 표준화 / 스케일링
from sklearn.preprocessing import StandardScaler
ss = StandardScaler( )
ss.fit( X_train_poly )
X_train_scaled = ss.transform( X_train_poly )
X_test_scaled = ss.transform( X_test_poly )

# 6) 모델 선택 = 단순선형회귀 , 규제( 릿지 / 라쏘 ) alpha 규제강도
from sklearn.linear_model import LinearRegression, Ridge
model = LinearRegression()
model.fit( X_train_scaled , Y_train)

print('선형회귀')
# 7) 결정계수
print( 'r2 : ' , model.score(X_train_scaled , Y_train))     # r2 :  0.6809891357804501
print( 'r2 : ' , model.score(X_test_scaled , Y_test))       # r2 :  0.6854720901189741

#======================================================
print( "릿지" )
pipe_model = Pipeline([
    ('poly' , PolynomialFeatures(include_bias=False)),
    ('scaler' , StandardScaler() ) ,
    ('ridge' , Ridge() )    # alpha 튜닝
])

# 2. 후보군 파라미터 만들기 , { '식별자_파라미터명' : [ 후보값 , 후보값 ] }
param_grid = { 
    'poly__degree' : [ 2, 3] , 
    'ridge__alpha' : [0.001 , 0.01 , 0.1 , 1 , 10 , 100]
} 

# 3. k-fold 교차 검증 
# kf = KFold( n_splits= K개의 동일한 폴드로 분할 , shuffle=True -> 분할시 무작위 섞기 여부 , random_state=42)
kf = KFold( n_splits=5 ,shuffle=True , random_state=42 )
# 학습 데이터들을 5개로 나누어 4개 학습하고 1개로 검증하는 과정을 5번 교차 검증 = 평균오차 / 손실

# 4. 그리서치 cv = 교차검증과 다양한 파라미터 자동으로 실행하고 최적 성능 찾기 
# GridSearchCV( estimator = 진행할모델/파이프라인, param_grid = {파라미터 후보군} , 
# scoring ='평가지표명' , cv = 교차 검증)
grid = GridSearchCV(
    estimator=pipe_model ,
    param_grid= param_grid , 
    scoring= 'r2' ,
    cv= kf , 
    n_jobs= -1 
)

# 5. 그리드서치로 학습 
grid.fit( X_train , Y_train )

# 6. 
best_model = grid.best_estimator_ # 가장 성능 좋은 모델 반환 


# 7. 최적 모델로 평가 
print( 'r2 : ' , best_model.score( X_train , Y_train ))  # 0.6921481671726891
print( 'r2 : ' , best_model.score( X_test , Y_test))     # 0.6921373259271997

import joblib
joblib.dump( best_model , './day16/model.pkl')


#===============================================================
print('라쏘')
# 1. 라쏘 파이프라인 만들기
pipe_model = Pipeline([
    ("poly", PolynomialFeatures(include_bias=False)),
    ("scaler", StandardScaler()),
    ("lasso", Lasso()),
])

# 2. 다항 차수와 라쏘 규제 강도 후보
param_grid = {
    "poly__degree": [2, 3],
    "lasso__alpha": [0.001, 0.01, 0.1, 1, 10, 100],
}

# 3. 5겹 교차 검증
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# 4. 그리드 서치 설정
grid = GridSearchCV(
    estimator=pipe_model,
    param_grid=param_grid,
    scoring="r2",
    cv=kf,
    n_jobs=-1,
)

# 5. 모델 학습
grid.fit(X_train, Y_train)

# 6. 최적 모델 선택
# 6. 주요속성
best_model = grid.best_estimator_ # 가장 성능 좋은 모델 반환 
print( grid.best_params_ )  # 가장 좋은 성능을 낸 하이퍼 파라미터
print( grid.best_score_)    # 교차 검증을 통해 얻은 최고 점수 

# 7. 최적 모델로 평가 
print( 'r2 : ' , best_model.score( X_train , Y_train ))         # 0.6858115878393294
print( 'r2 : ' , best_model.score( X_test , Y_test))            # 0.6894752690304831