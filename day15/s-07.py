import pandas as pd
fish = pd.read_csv("day13/Fish.csv")

# 1) 다중 분류 실습 하기 위한 특성 / 타깃(여러개 어종) 구분
X = fish.drop( columns=['Species'])
Y = fish['Species']

# 2) 분리 
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train , Y_test = train_test_split(X,Y,test_size=0.2,random_state=42,stratify=Y)

# 3) 다항 위한 스케일링 
from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
X_train_scaled =  ss.fit_transform( X_train )      # fit + transfrom
X_test_scaled =  ss.transform( X_test )


# 4)  로지스틱 회귀 = 이진  또는 다중 자동 선택된다. 
# L2 규제(릿지)  자동 포함 . 손실 ( 오차) 함수 계산 한다. c = 1.0 기본값 / 하이퍼파라미터 
# 계산 반복수 ( 경사하강법 ) : 가중치 / 기울기 찾기 위한 반복수 , 기본값 100 / 권장 1000 ~ 3000
# 경사하강법 : 기울기 ( 가중치 ) 변경하면서 최적의 기울기 / 가중치 오차 찾는 과정
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(C=1.0 , max_iter=1000 , random_state=42)
model.fit( X_train_scaled , Y_train)
Y_pred = model.predict(X_test_scaled)
print( Y_pred[:3])
Y_pred_proba = model.predict_proba( X_test_scaled )
import numpy as np
print( np.round(Y_pred_proba[ : 3 ] , 3) )
print( model.classes_)



# 평가 지표 
# average="macro" : 클래스마다 개수 다 다르므로 산술평균 값으로 계산
# 1) 정확도 : 전체 예측 건수 중 맞힌 정답의 비율 
from sklearn.metrics import accuracy_score, classification_report, precision_score , recall_score , f1_score
print( accuracy_score(Y_test , Y_pred ))    # 0.8125

# 2) 정밀도 : 예측 한 것 중 실제로 맞힌 비율
print( precision_score(Y_test , Y_pred , average="macro"))      # 0.6309523809523808

# 3) 재현율 : 실제 정답인 것 중에 모델이 놓치지 않고 찾아낸 비율        
print( recall_score( Y_test , Y_pred , average="macro"))        # 0.7012987012987013

# 4) f1 점수/표준 : 정밀도와 재현율 간의 조화 조정하기 위한 조화평균
print( f1_score( Y_test , Y_pred , average="macro" ) )          # 0.6609105180533751



## 4대 평가지표는 혼동행렬 이용하여 계산한다. 
# 혼동행렬 시각화
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay
# ConfusionMatrixDisplay.from_predictions( 정답지 , 예측값 )
ConfusionMatrixDisplay.from_predictions( Y_test , Y_pred )
plt.show()

## 리포트 ( 평가 지도 보고서 )
print( classification_report( Y_test , Y_pred ))


# 파이프라인 구성 
from sklearn.pipeline import Pipeline
pipe = Pipeline([
    ('caler' , StandardScaler()),
    ('model' , LogisticRegression(max_iter=1000 , random_state=42))
])

# 하이퍼 파라미터 후보군 , 식별자_매개변수명 : [ 후보값 , 후보값 ]
param_grid = {"model__C" : [ 0.01 , 0.1 , 1.0 , 10.0 , 100.0 ] }

# K폴드 이용한 교차 검증 분할기 ( 다중분류 : StratifiedKFold)
from sklearn.model_selection import KFold , StratifiedKFold
cv = StratifiedKFold(n_splits=5,shuffle=True,random_state=42)

# 그리드서치 
from sklearn.model_selection import GridSearchCV
grid = GridSearchCV( pipe, param_grid , cv=cv , scoring="f1_macro" ,n_jobs=-1)
grid.fit( X_train , Y_train )
print( grid.best_params_ )
print( grid.best_score_ ) # 최고의 f1 점수
best_model = grid.best_estimator_
Y_pred = best_model.predict(X_test )
print( classification_report(Y_test,Y_pred))