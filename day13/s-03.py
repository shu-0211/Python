# 1] 항 추가 하는 함수 
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures()    # 객체 생성
poly.fit( [ [ 2 ] ] )
print( poly.transform( [  [2]  ] ))        # [[1. 2. 4.]]

# 2] 기본 절편 제외 
poly = PolynomialFeatures( include_bias=False)
poly.fit([[2]])
print( poly.transform([[2]]))       # [[2. 4.]]

# 3] 특성이 2개 인 경우 
poly = PolynomialFeatures( include_bias= False )
poly.fit( [[ 2 , 3 ] ] )
print( poly.transform( [[2,3]] ))       # [[2. 3. 4. 6. 9.]]

# *] 특성 3개 인 경우 
poly = PolynomialFeatures( include_bias= False )
poly.fit( [ [ 2,3,4 ] ] )
print( poly.transform( [[ 3,5,6]]))     # [[ 3.  5.  6.  9. 15. 18. 25. 30. 36.]]

# =====================================================================
# 2] 다항 회귀 모델 
# 1) 특성과 타깃 구성 
import pandas as pd
df = pd.read_csv('./day13/Fish.csv')
X = df[['Length2' , 'Height' , 'Width' ]]   # 특성 3개 
Y = df['Weight']    # 타깃 1개 
# 2) 훈련용/테스트용 분리 8:2
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train , Y_test = train_test_split(X,Y,test_size=0.2,random_state=42)

# 3) 과소적합 해결/방지 하고자 항 추가 == PolynomialFeatures
poly = PolynomialFeatures(include_bias=False)
poly.fit(X_train)       # 학습할 특성들을 규칙(제곱/곱셈) 찾기 
print(poly)
X_train_poly = poly.transform(X_train)
X_test_poly = poly.transform(X_test)
print(X_train.shape)
print( X_train_poly.shape)

# 4) 모델 학습 
from sklearn.linear_model import LinearRegression
model = LinearRegression( )
model.fit(X_train_poly,Y_train)     # g항이 추가된 특성으로 학습 

# 5) 결정 계수 
from sklearn.metrics import r2_score
Y_pred = model.predict( X_test_poly )
print( 'r2 : ', r2_score( Y_test , Y_pred ))    # r2_score( 정답지 , 예측값 )
# 0.9719372415762598

# =====================================================================
# 3] 다항의 차수 늘리기 , degree = 10 , ( 차수n ) 제곱까지 항 추가하기/생략시 2
poly = PolynomialFeatures( include_bias=False , degree=10)
poly.fit( X_train )
X_train_poly2 = poly.transform(X_train)
print( X_train_poly2.shape)     # 차수2 --> 차수 10 증가 에 따른 ( 127,9) -> ( 127.285)
X_test_poly2 = poly.transform( X_test )

# 학습 후 결정계수 확인 
model = LinearRegression() 
model.fit( X_train_poly2 , Y_train )    # 훈련용 다항 특성으로 학습 * 
from sklearn.metrics import r2_score
Y_pred = model.predict(X_test_poly2)       # 테스트용 다항 특성으로 예측 &*
print('r2 : ' , r2_score(Y_test , Y_pred))  # r2_score( 정답지 , 예측값)
#  r2 :  0.0727666321391145
# *] 모델 구현에서 다양한 속성값( degree = N ) 들을 테스트 하여 설계 /구현한다. 
# *] 특성이 너무 많아지면 훈련 데이터가 과하게 집학하여 과대 적합이 발생하여 점수가 낮아진다. 
