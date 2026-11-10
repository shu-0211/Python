import pandas as pd
df = pd.read_csv("day13/Fish.csv")     # 1) 자료수집
X = df[ ['Length2' , 'Height' , 'Width'] ]  # 2) 특성 선정/구성
Y = df['Weight']        # 2) 타깃(정답)     선정 / 구성 

# 3) 훈련 / 테스트  분리 
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
X_train, X_test, Y_train , Y_test = train_test_split( X, Y, test_size = 0.2 , random_state = 42 )

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

# 7) 결정계수
print( 'r2 : ' , model.score(X_train_scaled , Y_train))     # r2 :  0.9833194466740022
print( 'r2 : ' , model.score(X_test_scaled , Y_test))       # r2 :  0.971937241576259


# ========================================================== (4) ~ (6) 과정 묶음
from sklearn.pipeline import Pipeline
# pipe_model =  Pipeline( [ ("식별자" , 클래스명()) ] )     # 파이썬 인스턴스생성 , 변수 = 클래스명( 인자값 )
# [] 리스트 () 튜플
pipe_model =  Pipeline( [ 
    ('poly', PolynomialFeatures(degree=2, include_bias=False)), # 4
    ( 'scaler' , StandardScaler()) ,                            # 5
    ( 'regressor' , LinearRegression())                         # 6
] ) 

# 9) 파이프 라인으로 학습
pipe_model.fit( X_train , Y_train)
print( 'r2 : ' , model.score(X_train_scaled , Y_train))
print( 'r2 : ' , model.score(X_test_scaled , Y_test))



# 10 ) 최적( 성능 좋은/ 오차적은 ) 의 파라미터(매개변수/대입값)  찾기 
# degree = 2 , alpha = 0.01
# 1. 파이프라인 만들기
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

# 6. 주요속성
best_model = grid.best_estimator_ # 가장 성능 좋은 모델 반환 
print( grid.best_params_ )  # 가장 좋은 성능을 낸 하이퍼 파라미터
print( grid.best_score_)    # 교차 검증을 통해 얻은 최고 점수 

# 7. 최적 모델로 평가 
print( 'r2 : ' , best_model.score( X_train , Y_train ))
print( 'r2 : ' , best_model.score( X_test , Y_test))

# 11) 서빙 , 학습된 모델 저장하고 다른곳에서 호출
# 연구 / 학습 : 코랩( 고사양 GPU )에서 학습 --> 실제 서버( FAST API )에서 호출
import joblib
# 1) 모델 저장한다. 
# joblib.dump(저장할 모델 , 경로.pkl )
joblib.dump( best_model , './day14/fish_model.pkl')  
# 2. 다른 파이썬 파일에서 저장된 모델 불러오기 . s-05.py 