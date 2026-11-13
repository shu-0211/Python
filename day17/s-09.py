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
# 성능이 ( 5% ) 떨어짐 