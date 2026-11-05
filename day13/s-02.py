import pandas as pd
df = pd.read_csv('./day13/Fish.csv')
# 1. 특성 , 타깃 분류
x = df[ ['Length2'] ]
y = df['Weight']
# 2. 훈련용/테스트용 분리
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train , Y_test = train_test_split(x,y,test_size=0.2,random_state=42)
# 3. 단순 회귀모델
from sklearn.linear_model import LinearRegression
model = LinearRegression()
# 4. 학습
model.fit(X_train,Y_train)
# 5. 모델 결정계수
Y_pred = model.predict(X_test)
from sklearn.metrics import r2_score
print( 'r2 : ', r2_score(Y_test,Y_pred))   #   0.8199897860284712

# ===================================================================================
# 1] 특성[x] 에 제곱하여 항 추가 
import numpy as np
# np.column_stack( ( 배열1, 배열2 ) ) # 배열 연결
X_train_poly = np.column_stack( ( X_train**2 , X_train ) )
print( X_train_poly ) # [ ]  -> [ 262.22 16.2 ]
# 2] 제곱된 모델 학습
model = LinearRegression( )
model.fit( X_train_poly , Y_train )
# 3] 예측 
print( model.predict( [[ 30**2 , 30 ]]))
# 4] 시각화 
point = np.arange( 0 , 101)     # 0 ~ 100 까지의 회귀선
point_poly = np.column_stack( ( point**2 , point ) )

import matplotlib.pyplot as plt
plt.scatter( X_train , Y_train )    # 특성자료
plt.plot(point, model.predict(point_poly) , color="red")
plt.plot( )                         # ( 제곱항이 추가된 ) 회귀선
plt.show( )

# 5] 결정계수 
X_test_poly = np.column_stack( ( X_test**2, X_test ) )  # 테스트 
Y_pred = model.predict( X_test_poly )
print(r2_score(Y_test , Y_pred ) )

# day12 : 단순 선형 회귀 결정계수 : 0.8199897860284712
    # 직선 공식( 1차 방정식 ) : Y = WX + B
# day13 : 다항 선형 회귀 결정계수 : 0.8249869834428712
    # 곡선 공식 ( 2차 방정식 ) : Y = (WX(제곱)) + (WX(원본)) + B