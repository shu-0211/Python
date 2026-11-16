import pandas as pd

url = 'https://raw.githubusercontent.com/rickiepark/hg-mldl/master/wine.csv'
df = pd.read_csv(url)

# alcohol,sugar,pH,class ( 0:레드 / 1:화이트 )

X = df[ ['alcohol' , 'sugar' , 'pH']]       # 독립변수
Y = df['class']                             # 종속변수

from sklearn.model_selection import train_test_split
X_train , X_test , Y_train , Y_test = train_test_split( X , Y , test_size = 0.2 , random_state = 42 ,stratify=Y)

## 1) lightGBM : LGBMClassifier 분류모델 , LGBMRegressor 회귀모델
from lightgbm import LGBMClassifier, early_stopping # 0레드 1화이트     와인 종류 분류
model = LGBMClassifier(
    # 다양한 매개변수 ( 파라미터 )  설정 
    n_estimators=1000,            # 1) 추정기 : 모델을 총 몇개를 만들건지 
    learning_rate=0.05,          # 2) 학습률
    num_leaves=15,               # 3) 하나의 트리(모델) 가질 수 있는 최대 리프 노드 수
    max_depth=10,                 # 4) 하나의 트리 최대 깊이 , 기본값 -1 
    min_child_samples=20,        # 5) 리프노드 최소 샘플 수
    subsample=0.8,               # 6) 매 반복마다 랜덤으로 80%만 무작위 샘플링 
    subsample_freq=1,            # 7) 같이 등록된, 매 트리마다 배깅을 활성화
    colsample_bytree=0.8,        # 8) 매 이동마다 무작위로 전체적으로 80%만 이동 선택
    class_weight='balanced',    # 9) * 분류 모델* 에서 타깃/종속에 균형이 맞지 않음/완화
    random_state=42 , n_jobs=-1 , verbose=-1, # 매 학습마다 로그 숨김 
)



# =  ========== 
# 2) 모델 학습 수행 , 
# eval_set=[ ( X_test , Y_test ) ] : 조기 종료 하기 위한 ( 성능 ) 검증용 데이터 셋 포함
# # 만약에 여러번 학습 중에 손실함수 결과 오차 /잔차가 최적이 되면 종료 모니터링
# callbacks=[early_stopping(stopping_rounds=50 , verbose=False)] 
# 학습마다 검증 성능이 개선되지 않을때 추가로 기다릴 반복 횟수

model.fit(X_train,Y_train ,
    eval_set=[( X_test , Y_test ) ] ,
    callbacks=[early_stopping(stopping_rounds=50 , verbose=False)]          
) 


# 3) 주요 속성 확인 
print(model.best_iteration_)        # 최적의 트리 반복 수 / 번호 # 310 
print( model.feature_name_)         # 각 특성의 이름      / ['alcohol', 'sugar', 'pH']
print( model.feature_importances_)  # 각 트성의 중요도    / [ 579 2284 1447]


# 4) 평가지표
from sklearn.metrics import f1_score
Y_pred = model.predict(X_test)
print( model.score(X_train , Y_train) )
print( model.score(X_test, Y_test))
print( f1_score( Y_test, Y_pred , average="macro"))
# 0.8845487781412353
# 0.8523076923076923
# 0.8192436040044494

# 깊이 10
# 0.8864729651722147
# 0.8530769230769231
# 0.8197484027443542


# 5) 예측하기
new_wine = pd.DataFrame([[11.5 , 2.3, 3.1] , [13.8 , 11.2 , 3.3 ] ] )
new_pred = model.predict(new_wine)
print( '예측 1 : ' , new_pred[0] )  #  0.0
print( '예측 2 : ' , new_pred[1])   #  1.0