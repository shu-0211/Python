# 지도학습      : x구성(독립) 과 Y 타깃(종속) 모델에 대해 학습하여 예측, 댈 r2, 유일하게 f1-점수 평가지도
# 비지도 학습   : x치수(독립) 모델 이요하여 거리/밀집 군집/클러스터/그룹 , 해적k(sse , 밖)

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
from sklearn.metrics import silhouette_score
sse_list = [ ]
sil_list = [ ]
for k in range( 2 , 20 ) : # range( 시작값 : 끝값 -1 )
    k_temp = KMeans( n_clusters=k , random_state=42)
    preds = k_temp.fit_predict( X_train_scaled )        # 모델 학습/추론 동시에 , fit + predict
    sse_list.append( k_temp.inertia_ )                  # 군집 결과에 각 샘플과 중심점 거리 제곱의 합 저장
    sil_list.append( silhouette_score( X_train , preds ) )  # 실루엣 점수를 저장

plt.plot( range(2,20) , sse_list , marker='o')
plt.show()

plt.plot( range(2,20) , sil_list , marker='o')
plt.show()

#=============================================

# 1행 2열의 서브플롯 생성 (전체 가로 12, 세로 4 크기)
fig, axs = plt.subplots(1, 2, figsize=(12, 4))

# 첫 번째 그래프 (왼쪽): Elbow (SSE / Inertia)
axs[0].plot(range(2, 20), sse_list, marker='o')
axs[0].set_title('Elbow Method (SSE)')
axs[0].set_xlabel('k')
axs[0].set_ylabel('SSE (Inertia)')

# 두 번째 그래프 (오른쪽): Silhouette Score
axs[1].plot(range(2, 20), sil_list, marker='o', color='orange')
axs[1].set_title('Silhouette Score')
axs[1].set_xlabel('k')
axs[1].set_ylabel('Silhouette')

plt.tight_layout() # 그래프 간격 자동 조절
plt.show()

#=============================================


# sse : 엘보우지점 ( 기울기가 완만하게 꺾이는 변곡점 ) , 오차 제곱합 ( 꺾임 정도가 가장 큰)
# 실루엣 : 높은 값일 수록 이상적.
# 두 차트 해석하여 최적의 k 해석 ,
# 최적 k 군집 하기 
best_model = KMeans( n_clusters=5 )
pred = best_model.fit_predict(X_train_scaled)
print(pred[ : 10])



# 5) HDBSCAN # K-Mean와 다르게ㅣ상치를 자동 분리함
from sklearn.cluster import HDBSCAN
# HDBSCAN( min_cluster_size=군집하기 위한 최소 데이터 수  , min_samples=군집판별할 떄 계수)
model = HDBSCAN( min_cluster_size=30 , min_samples=10)
pred = model.fit_predict(X_train_scaled)
print( pred )       # 군집 / 그룹 4개 , # 이상치 1개 (-1)

X_train['hdb_cluster'] = pred       # 군집 결과 판다스 열에 추가 
print(X_train['hdb_cluster'].value_counts())


# 6) 시각화 : 
nosie_mask = (X_train['hdb_cluster'] == -1 )
plt.scatter(    X_train.loc[~nosie_mask , 'G3'],
                X_train.loc[~nosie_mask , 'absences'],
                c=X_train.loc[~nosie_mask,'hdb_cluster'])
plt.scatter( X_train.loc[nosie_mask,'G3'],
            X_train.loc[nosie_mask,'absences'] , 
            c='red' , marker='*')
plt.show()

# 7) PCA(주성분 분석) 고차원데이터의 분산을 저차원으로 축소하여 주 성분/특성만듬
# 고차원이란? 다수의 특성들의 가중치/기울기 표현
# 상관계수란 A특성과 B 특성의 관계성( A가 변경되면 B 얼마나 변하는지관계성을 수치로 나타냄)
from sklearn.decomposition import PCA
# PCA(n_components = 차원수 )

pca = PCA( n_components=2 ) # 시각화(2D)하기위한 2차원 축소
X_train_pca = pca.fit_transform( X_train_scaled )
print( X_train_pca ) # 행 마다의 가중치 
print( pca.components_.T ) # 주 특성별 가중치


#    주성분 1      주성분 2
# [[ 0.13219328 -0.61408979]            공부시간
#  [-0.00599139  0.78051288]            결석일수
#  [ 0.56213845  0.00343157]            1학기성적
#  [ 0.58342273  0.03443535]            2학기성적
#  [ 0.57105808  0.11178463]]           3학기성적

pca_hdb = HDBSCAN( min_cluster_size=30 , min_samples=5 )



# 주성분1 에서 강한(+) ? 1학기 성적/ 2학기 성적 / 3학기 성적
# 5차원에서 2차원으로 축소 한 PCA 학습
pca_pred = pca_hdb.fit_predict(X_train_pca)
X_train['PC1'] = X_train_pca[ : , 0]
X_train['PC2'] = X_train_pca[ : , 1]
X_train['PCA_cluster'] = pca_pred
print(X_train[ ['PC1' , 'PC2' , 'PCA_cluster']].head(10))


#           PC1       PC2  PCA_cluster
# 316 -2.221877 -0.804689           -1
# 116  0.808827 -0.220407            2
# 9    1.758814 -0.368879            2
# 209 -1.525153 -0.789537           -1
# 323  1.417209 -1.011025           -1
# 393  0.000504  0.206730            0
# 258  1.644120  0.375856           -1
# 155 -0.714701 -0.412403            1
# 124 -1.381884 -0.619013           -1
# 272  0.124762 -0.311819            1


# 7) 이상치 제외한 G3 평균 계산
normal_clusters = X_train[ X_train['PCA_cluster'] != -1 ]       # 이상치 제외 
# pd.groupby('성별')['국어점수'].mean() : 성별/열 그룹끼리 국어점수/특정 열에 펴균 집계
cluster_means = normal_clusters.groupby('PCA_cluster')['G3'].mean()
sorted_cluster = cluster_means.sort_values( ascending = True ) # True 오름차순 False 내림차순
print( sorted_cluster )

# PCA_cluster
# 1     9.873239
# 0    12.513514
# 2    13.641509
# Name: G3, dtype: float64

# 8) 라벨링 
# enumerate( )   # range( ) 
labels = { }
for idx , cluster_id in enumerate( sorted_cluster.index , start=1 ) : 
    labels[ cluster_id ] = f'Level{idx}'

labels[-1] = 'Outlier'      # 이상치는 리스트 가장 뒤에
# {1: 'Level1' , 0: 'Level2' , 2: 'Level3' , -1 : 'Outlier'}
X_train['pca_cluster_label'] = X_train['PCA_cluster'].replace( labels)
print( X_train)         # 군집화한 결과 가지고 추후에 지도 학습
# 지도 학습에서 성능 향상 하기 위한 방법 : 0) 전처리 1) 하이퍼파라미터 2) 파생변수
# 자바 활용방법 : 관리자 페이지 해당 회원이 위험군/VIP


# 9) 시각화 
for lbl in list( labels.values() ) : 
    sub = X_train[X_train['pca_cluster_label'] == lbl]
    if lbl == 'Outlier' : 
        plt.scatter( sub['PC1'] , sub['PC2'] , c='red' , marker='*' , label=lbl)
    else :
        plt.scatter(sub['PC1'] , sub['PC2'] , marker='o' , label = lbl)
plt.legend()
plt.show()