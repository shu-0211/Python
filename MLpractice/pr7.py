# PythonML Practice7: 비지도학습 기반 통신사 고객 등급화
# 데이터셋: 통신사 고객의 가입 기간 및 요금 청구 데이터
# URL: 'https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv'

import pandas as pd
url = 'https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv'
df = pd.read_csv(url)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df = df.dropna(subset=['TotalCharges'])
X = df[['tenure', 'MonthlyCharges', 'TotalCharges']]

# [단계 1] 수치형 정제 및 데이터 표준화
# 1. 가입 기간(개월)과 요금(달러) 간의 단위 차이를 보정하기 위해 StandardScaler().fit_transform(X)를 적용하여 X_scaled를 생성하세요.
from sklearn.metrics import silhouette_score
# from sklearn.model_selection import train_test_split
# X_train, X_test = train_test_split(X, test_size=0.02, random_state=42)

from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
X_scaled = ss.fit_transform( X )


# [단계 2] 엘보우 기법(SSE) 및 실루엣 계수를 활용한 최적의 K 탐색
# 1. k를 2부터 10까지(range(2, 11)) 반복하면서 KMeans(n_clusters=k)의 fit_predict(X_scaled)를 수행하세요.
# 2. 각 k별 오차제곱합(model.inertia_)과 실루엣 점수(silhouette_score(X_scaled, preds))를 각각의 리스트에 저장하세요.
# 3. k에 따른 SSE 변화 차트와 실루엣 점수 변화 차트를 각각 선 그래프(marker='o')로 시각화하여 최적의 K 지점을 확인하세요.
from sklearn.cluster import KMeans
sse_list = []
sil_list = []
for k in range(2 , 20) : 
    k_temp = KMeans(n_clusters=k , random_state=42)
    preds = k_temp.fit_predict(X_scaled)
    sse_list.append(k_temp.inertia_)
    sil_list.append(silhouette_score( X_scaled , preds ))

import matplotlib.pyplot as plt
plt.plot( range(2,20) , sse_list , marker='o')
plt.show()

plt.plot( range(2,20) , sil_list , marker='o')
plt.show()

# [단계 3] 최적의 K 기반 K-Means 모델 생성 및 군집 예측
# 1. 이전 단계에서 도출된 최적의 군집 수(n_clusters=k)로 최종 KMeans 모델을 생성하세요.
# 2. fit_predict(X_scaled)를 실행하여 고객별 군집 번호를 예측하고, 원본 데이터프레임 X에 'cluster' 컬럼으로 추가하세요.
# 3. X['cluster'].value_counts()를 출력하여 각 군집별 고객 분포를 확인하세요.
best_model = KMeans(n_clusters=5)
pred = best_model.fit_predict(X_scaled)
X['cluster'] = pred
print(X['cluster'].value_counts())

# cluster
# 4    1911
# 0    1645
# 1    1384
# 3    1141
# 2     951
# Name: count, dtype: int64

# [단계 4] 주성분 분석(PCA)을 통한 2차원 차원 축소
# 1. 3차원 고객 요금/기간 데이터를 2D 평면에 시각화하기 위해 PCA(n_components=2) 객체를 생성하고 X_scaled에 fit_transform()을 적용하여 X_pca를 생성하세요.
# 2. pca.components_.T를 출력하여 주성분 1(PC1)과 주성분 2(PC2)에 영향을 주는 원본 피처('tenure', 'MonthlyCharges', 'TotalCharges')의 가중치를 확인하세요.
# 3. 축소된 좌표 값을 원본 데이터프레임 X의 'PC1', 'PC2' 컬럼으로 각각 추가하세요.
from sklearn.decomposition import PCA 
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
print( pca.components_.T )

# Name: count, dtype: int64
# [[ 0.56721122 -0.60697524]
#  [ 0.48571362  0.79237469]
#  [ 0.66509677 -0.06101971]]

X['PC1'] = X_pca[ : , 0]
X['PC2'] = X_pca[ : , 1]
print(X['PC1'])
print(X['PC2'])

# [단계 5] 총 청구액 평균 기준 군집 정렬 및 고객 등급 자동 라벨링
# 1. 군집별 'TotalCharges' 평균을 X.groupby('cluster')['TotalCharges'].mean()으로 계산하고 오름차순(ascending=True)으로 정렬하세요.
# 2. 누적 매출 기여도가 낮은 군집부터 순서대로 'Grade1', 'Grade2', ... 등급을 부여하는 딕셔너리(label_map)를 자동 생성하세요.
# 3. replace(label_map)를 이용해 X['cluster_label'] 컬럼을 생성한다.

X_means = X.groupby('cluster')['TotalCharges'].mean()
X_sorted = X_means.sort_values(ascending=True)
print(X_sorted)
# cluster
# 0     304.569042
# 4     856.424123
# 2    1475.867386
# 3    3348.734405
# 1    6238.120376
# Name: TotalCharges, dtype: float64

label_map = { }
for idx , cluster_id in enumerate( X_sorted.index , start=1 ) :
    label_map[cluster_id] = f'Grade{idx}'

    X['cluster_label'] = X['cluster'].replace(label_map)

# [단계 6] PCA 산점도 최종 시각화
# 1. label_map.values() 순서대로 반복문을 실행하여 각 등급('Grade1', 'Grade2', ...)별 데이터를 추출하세요.
# 2. matplotlib.pyplot의 plt.scatter()를 이용해 x축은 'PC1', y축은 'PC2'로 각 등급별 산점도를 원형 마커('o')로 겹쳐 그리세요.

for lbl in label_map.values() : 
    sub = X[X['cluster_label'] == lbl]
    if lbl == 'Outlier' : 
        plt.scatter( sub['PC1'] , sub['PC2'] , c='red' , marker='o' , label=lbl)
    else :
        plt.scatter(sub['PC1'] , sub['PC2'] , marker='o' , label = lbl)
plt.legend()
plt.show()