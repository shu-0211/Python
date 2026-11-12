import pandas as pd
df = pd.read_csv('day16/team/calories.csv')

df['Gender'] = df['Gender'].map({'male': 0, 'female': 1})
print(df.info())

#  0   User_ID     15000 non-null  int64  
#  1   Gender      15000 non-null  str    
#  2   Age         15000 non-null  int64  
#  3   Height      15000 non-null  float64
#  4   Weight      15000 non-null  float64
#  5   Duration    15000 non-null  float64
#  6   Heart_Rate  15000 non-null  float64
#  7   Body_Temp   15000 non-null  float64
#  8   Calories    15000 non-null  float64
X = df[['Gender', 'Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp']]
Y = df['Calories']


#   훈련 / 테스트 분리 
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
X_train, X_test, Y_train , Y_test = train_test_split(X,Y,test_size=0.2, random_state=42)


# 과소적합 방지 항 추가  
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures( degree=2 , include_bias=False)
poly.fit( X_train)
X_train_poly = poly.transform( X_train )
X_test_poly = poly.transform( X_test )

# 스케일링 
from sklearn.preprocessing import StandardScaler
ss = StandardScaler( )
ss.fit( X_train_poly )
X_train_scaled = ss.transform( X_train_poly )
X_test_scaled = ss.transform( X_test_poly )

# 모델 선택  = 단순 선형 회귀 
from sklearn.linear_model import LinearRegression, Ridge
model = LinearRegression() 
model.fit(X_train_scaled , Y_train)

# =========================================

# 파이프라인으로 구성 
from sklearn.pipeline import Pipeline
pipe_model = Pipeline([
        ('poly', PolynomialFeatures(include_bias=False)),
        ('scaler', StandardScaler()),
        ('ridge', Ridge()),
    ])

param_grid = { 
    'poly__degree' : [ 2, 3] , 
    'ridge__alpha' : [0.001 , 0.01 , 0.1 , 1 , 10 , 100]
} 

kf = KFold(
        n_splits=5,
        shuffle=True,
        random_state=42,
    )

grid = GridSearchCV(
        estimator=pipe_model,
        param_grid=param_grid,
        scoring='r2',
        cv=kf,
        n_jobs=-1,
        refit=True,
        verbose=1,
    )

grid.fit(X_train, Y_train)

# 최적의 모델
best_model = grid.best_estimator_

train_r2 = best_model.score(X_train, Y_train)

Y_pred = best_model.predict(X_test)

test_r2 = r2_score(Y_test, Y_pred)
test_mae = mean_absolute_error(Y_test, Y_pred)

print('\n===== 모델 학습 결과 =====')
print('최적 파라미터:', grid.best_params_)
print(f'교차 검증 평균 R²: {grid.best_score_:.4f}')
print(f'훈련 데이터 R²: {train_r2:.4f}')
print(f'테스트 데이터 R²: {test_r2:.4f}')
print(f'테스트 데이터 MAE: {test_mae:.2f} kcal')


# sample = [[0, 25, 175, 70, 30, 125, 39.5]]