# 부스팅 앙상블 
# 설치 : pip install lightgbm xgboost catboost
import pandas as pd

url = 'https://raw.githubusercontent.com/rickiepark/hg-mldl/master/wine.csv'
df = pd.read_csv(url)

# alcohol,sugar,pH,class ( 0:레드 / 1:화이트 )

X = df[ ['alcohol' , 'sugar' , 'pH']]       # 독립변수
Y = df['class']                             # 종속변수

from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
X_train , X_test , Y_train , Y_test = train_test_split( X , Y , test_size = 0.2 , random_state = 42 ,stratify=Y)


# 3가지 부스팅 앙상블 사용 
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier

# 1) 모델 비교   
# n_estimators : 부스팅 사용할 트리 개수 기본값 100 , 권장 1000~3000( 최적 몯레 ㅍㅅ]맣ㅎ)
models = {
    "XGBoost" : XGBClassifier( n_estimators = 1000 ,  learning_rate=0.05 , max_depth=4 ,random_state= 42) ,
    "LightGCb": LGBMClassifier( n_estimators = 1000 , learning_rate=0.05, max_depth=4 ,random_state=42, n_jobs=-1 , verbose=-1 )}


# 2) 반복 이용하여 모델 학습/ 학습 데이터 시간 테스트
import time
for name , model in models.items() :
    start = time.time()
    model.fit( X_train , Y_train )
    end = time.time() - start
    Y_pred = model.predict(X_test)  # 예측

    print('============ 모델명 : ' , name )
    print('============ 학습모델명 : ' ,)
    print("> train acc : " , model.score(X_train , Y_train ) )
    print("> test acc : " , model.score(X_test , Y_test))
    print('> f1 score : ' , f1_score(Y_test , Y_pred , average="macro")) 
