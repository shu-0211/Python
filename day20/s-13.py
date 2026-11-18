# 지도학습 
# 비지도 학습 

import pandas as pd
url = "https://raw.githubusercontent.com/arunk13/MSDA-Assignments/master/IS607Fall2015/Assignment3/student-mat.csv"
df = pd.read_csv(url, sep=';')

X = df[['studytime', 'absences', 'G1', 'G2', 'G3']]

from sklearn.model_selection import train_test_split
X_train, X_test = train_test_split(X, test_size=0.02, random_state=42)

# 1) 스케일링/단위표준화 ,              트리는 스케일링 할 필요가 없음
from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
X_train_scaled = ss.fit_transform( X_train )
X_test_scaled = ss.transform( X_test )

# 2) 군집 = 그룹만들기 =  클러스터  ,  K개의 군집을 찾는 k_means 모델 
from sklearn.cluster import KMeans
model = KMeans( n_clusters=3 )
model.fit(X_train_scaled)  # 군집 학습
train_labels = model.predict(X_train_scaled)    # 군집 추론
print( '앞에서 10명 그룹 확인 : ' , train_labels[ : 10])
# 앞에서 10명 그룹 확인 :  [2 1 1 0 1 1 1 2 2 1]

print( '테스트 학생 : ' , model.predict( X_test_scaled ) )
# 테스트 학생 :  [1 0 1 1 1 0 0 1]


# 3) 시각화 : 특성 여러개 이므로 2D 시각화 한계 
# 판다스 복습
# list_2 = [ [2,3] , [4,5] ]
# print( list_2[ :  , 1])
import matplotlib.pyplot as plt 
plt.scatter(X_train_scaled[ : , 4] , X_train_scaled[ : , 1] , c=train_labels)
plt.scatter( X_test_scaled[ : , 4], X_test_scaled[ : , 1] , c='red' , marker='*')
plt.show()


# 4) 최적의 k(군집/그룹) 수 찾기 vs 지도학습(F1 분류 / R2 회귀 ) 
sse_list = [ ]
for k in range( 2 , 20 ) : # range( 시작값 : 끝값 -1 )
    k_temp = KMeans( n_clusters=k , random_state=42)
    preds = k_temp.fit_predict( X_train_scaled )        # 모델 학습/추론 동시에 , fit + predict
    sse_list.append( k_temp.inertia_ )                  # 군집 결과에 각 샘플과 중심점 거리 제곱의 합 저장

plt.plot( range(2,20))
plt.plot()