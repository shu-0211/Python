# 1] 항 추가 하는 함수 
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures()    # 객체 생성
poly.fit( [ [ 2 ] ] )
print( poly.transform( [  [2]  ] ))        # [[1. 2. 4.]]

# 2] 기본 절펴 제외 
poly = PolynomialFeatures( include_bias=False)
poly.fit([[2]])
print( poly.transform([[2]]))       # [[2. 4.]]

# 3]
poly = PolynomialFeatures( include_bias= False )
poly.fit( [[ 2 , 3 ] ] )
print( poly.transform( [[2,3]] ))       # [[2. 3. 4. 6. 9.]]

# *] 특성 3개 인 경우 
poly = PolynomialFeatures( include_bias= False )
poly.fit( [ [ 2,3,4 ] ] )

# =====================================================================
# 2] 다항 회귀 모델 
import pandas as pd
df = pd.read_csv('')