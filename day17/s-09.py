import pandas as pd

url = 'https://raw.githubusercontent.com/rickiepark/hg-mldl/master/wine.csv'
df = pd.read_csv(url)

# alcohol,sugar,pH,class ( 0:레드 / 1:화이트 )

X = df[ ['alcohol' , 'sugar' , 'pH']]       # 독립변수
Y = df['class']                             # 종속변수

from sklearn.model_selection import train_test_split
X_train , X_test , Y_train , Y_test = train_test_split( X , Y , test_size = 0.2 , random_state = 42 ,stratify=Y)

# 1) 결정트리 모델
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
# 종속/타깃이 범주형이면 XXXXClassifier , 연속형이면 XXXXRegressor

model = DecisionTreeClassifier()
model.fit( X_train , Y_train )
print( "Train Acc : " , model.score(X_train  , Y_train))
print( "Test Acc : " , model.score(X_test  , Y_test))    
# Train Acc :  0.9978833942659227
# Test Acc :  0.8630769230769231   
# 훈련용과 테스트 데이터간의 점수 차이가 10%이상이면 과적합
# -> 과적합이면 규제
# !!! 스케일링 / 표준화 할필요없음 -> 원본 그대로 비교하여 분류

# 2) 시각화 
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
plot_tree( model , max_depth=1 )
plt.show()

# 트리란 ? 전체 적인 의사결정 분기 구조 
# 노드란? 사각형 상자 하나하나를 의미하며 , 최상단 노드를 Root 노드
# 노드 내부 속성 해석
#   X[0] 또는 특성명 <= 값 , 분기 조건 ( T : 왼쪽 / F : 오른쪽 )
#  # gini = 값 , 지니 불순도 ( 0에 가까울수록 순수 , 0.5 혼잡 )
# samples = 값, 해당 노드의 데이터 총개수 
# values <= [개수 , 개수] , 해다 노드에 도달한 특성 값으로 분류한 특성들의 개수 
# ** 지니 불순도 최대한 0 가깝게 가지치기

# ========================================= 
# 3) 규제 : 가지치기 ( 루트 개수 제한 )
model = DecisionTreeClassifier(
    max_depth=3 ,               # 트리의 최대 깊이를 3으로 제한하여 복잡도 낮추기 
    min_samples_leaf=10 ,       # 리프노드가 가져야 할 최소 샘플 수 10개 제한
    criterion="gini"   ,        # 분할 측정 지표 gini vs entropy
    random_state=42 ,           # 난수 시드  
)
model.fit( X_train , Y_train )
print( "Train Acc : " , model.score(X_train  , Y_train))
print( "Test Acc : " , model.score(X_test  , Y_test))    
# Train Acc :  0.8456802001154512
# Test Acc :  0.8407692307692308
# 규제 없을때 12% 차이가 있지만  규제 있을때 0.5% 차이 줄었다. 성능이 좋아졌다.

# 4) 타깃 / 종속 클레스의 불균형 ( 레드 / 화이트와인 개수 / 비율 다르다. )
model = DecisionTreeClassifier(
    max_depth=3 , min_samples_leaf=10 , criterion="gini" , random_state=42, 
    class_weight="balanced", #클래스 빈도에 반비례하여 가중치를 자동 부여하여 불균형 보정
)
model.fit( X_train , Y_train )
print( "Train Acc : " , model.score(X_train  , Y_train))
print( "Test Acc : " , model.score(X_test  , Y_test))  
# Train Acc :  0.787569751779873
# Test Acc :  0.7946153846153846
# 성능이 ( 5% ) 떨어짐  # 과도한 규제 -> 과소 적합

# 5) 특성 중요도 : feature_importances_
print( model.feature_names_in_ )
print( model.feature_importances_ ) # 분류모델에서 예측에 기여한 특성의 중요도 수치 
# ['alcohol' 'sugar' 'pH']
# [0.06047705 0.92312892 0.01639403]


# 6) 앙상블 : 배깅 또는 부스팅 방식으로 복합 모델 구현
# 배깅 앙상블 : 랜덤포레스트 ( 여러 트리모델을 병렬 처리 하여 최적의 모델 찾기 )
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(
    max_depth=3 ,               # 트리의 최대 깊이 ( 과적합 억제 )
    class_weight="balanced",    # 크래스 불균형 해소 ( 과적합 억제 )
    n_estimators=10 ,           # 생성할 결정 트리 개수 기본값 100 , 1000~3000
    max_features='sqrt' ,        # 각 노드에서 분할 시 특성의 최대 개수
    random_state=42,
    n_jobs= -1 , 
)

model.fit( X_train , Y_train )
print( "Train Acc : " , model.score(X_train  , Y_train))
print( "Test Acc : " , model.score(X_test  , Y_test))  
# 트리 개수 100일때
# Train Acc :  0.7852607273426977
# Test Acc :  0.7738461538461539
# 트리 개수 10일때
# Train Acc :  0.817009813353858
# Test Acc :  0.8007692307692308

# max_features = 'sqrt' 사용하는 이유 : 분류에서 샘플을 사용할 때 샘플들을 전체 사용하지 않는다.
# 총 4개인 경우 랜덤으로 4에서 제곱근 하여 2개만 사용한다. # 전체 샘플 사용시 과적합


print( model.feature_names_in_ )
print( model.feature_importances_ )
# 특성 중요도 
# [0.12894291 0.48896704 0.38209005]