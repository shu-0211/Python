import pandas as pd
url = 'https://raw.githubusercontent.com/rashida048/Datasets/master/USA_cars_datasets.csv'
df = pd.read_csv(url)

df = df[df['price'] > 0]
num_cols = ['year', 'mileage']                                      # 수치형
cat_cols = ['brand', 'model', 'title_status', 'color', 'state']     # 범주형
# 만야게 모델 성능 햐상 하기 위해 도메인 지식의 (계산식)특성 축성 추가 하면 좋음

# 범주형 자료들을 원핫인코딩이 아닌 판다스'카테고리' 타입 변경 # lightGBM내장 원핫 인코딩 사용목적

for col in cat_cols: 
    df[col] = df[col].astype('category')

X = df[num_cols + cat_cols]
Y = df['price']
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# ====================================================

# 1) 프레임워크이기 때문에 설치를 해야함 
# 튜닝 -> optuna
# 1. optuna 설치 :  $env:PYYAML_FORCE_LIBYAML = "0"  pip install optuna shap
import numpy as np
import optuna
from lightgbm import LGBMRegressor, early_stopping
optuna.logging.set_verbosity(optuna.logging.WARNING)

# 4) 목적함수 만들기
def objective( trial ) :
    # 4-1 교차 검증 KFold
    from sklearn.model_selection import KFold
    cv = KFold( n_splits= 5 , shuffle=True , random_state=42) 
    cv_r2_scores = []               # 각 폴더별 검증 점수
    best_iterations = []            # 각 폴더별 최적 트리 번호
    for train_idx , val_idx in cv.split( X_train , Y_train )     : 
        # k번째 폴드의 훈련용/검증용 인덱스 반환
        # 훈련 데이터 세트 내부에서 훈련용 / 검증용 분할 수행 , k=5 , 5개 폴드 , 각각 한번씩 검증용
        X_tr , X_val = X_train.iloc[ train_idx ] , X_train.iloc[ val_idx ]
        Y_tr , Y_val = Y_train.iloc[ train_idx ] , Y_train.iloc[ val_idx ]

        # k폴드에서 분할한 훈련용 모델 만들기
        model = LGBMRegressor(
            n_estimators=1000 , 
            learning_rate= trial.suggest_float('learning_rate' , 0.01 , 0.1 ),   # 학습률
            num_leaves=trial.suggest_int( 'num_leaves' , 10 , 30 ),
            max_depth=trial.suggest_int( 'max_depth' , 3 , 10 ),
            min_child_samples=trial.suggest_int('min_child_samples' , 10 , 50),
            subsample= trial.suggest_float( 'subsample' , 0.6 , 1.0),
            subsample_freq=1    , verbose = -1 , random_state=42 , n_jobs=-1 ,
            colsample_bytree =trial.suggest_float('colsample_bytree' , 0.6 , 1.0),
            # class_weight 회귀모델이므로 생략
            
        )

        # 4-2 교차별 학습 모델                                                                                            
        # 폴드별 훈련용/검증용 으로 학습
        model.fit( X_tr, Y_tr , eval_set=[ (X_val , Y_val)] ,
                  callbacks = [ early_stopping(stopping_rounds=50 , verbose=False)]) 



        # 4-3 교차별 학습 성능 저장
        # K폴드별 검증 평가 r2 
        r2 = model.score( X_val , Y_val )
        cv_r2_scores.append( r2 )                           # k 폴드별 평가 점수 저장
        best_iterations.append(model.best_iteration_)       # k 폴드별 최적 트리 번호
    # k 폴드에서 산출된 최적 트리 개수의 평균값을 trial의 속성으로 저장
    trial.set_user_attr('best_n_estimators' , int(np.mean(best_iterations)))

    return np.mean( cv_r2_scores )




# 3) study = optuna.create_study(direction='maximize'/'minimize' , sampler= sampler)
# 현재 실습은 회귀모델이며 r2 결정계수 평가지표 사용할 예정
sampler = optuna.samplers.TPESampler( seed = 42 )
study = optuna.create_study(direction='maximize' , sampler= sampler)    # 평가지표가 높은걸 원하면 max , 낮은건 min
# study.optimize( 목적함수 , n_trials=반복수)
study.optimize( objective , n_trials=20)     # 목적함수가 반복수만큼 실행됨. 목적함수에 소괄화를 안쓰는 이유는 함수 자체를 부르기 위해(콜백함수)
# 실무에서는 100단위로 작성


# 5) 최적 모델 
print( '최적 하이퍼파라미터 : ' , study.best_params )
optimal_model = study.best_trial.user_attrs['best_n_estimators']
print( '최적 트리 : ' , optimal_model)


# 6) 최적 파라미터로 모델 학습
final_model = LGBMRegressor(
    random_state=42 , verbose = -1 , n_jobs=-1 , 
    **study.best_params,        # 최적 파라미터 포함 # **리스트  # ** 전개연산자 , ** 딕셔너리
    n_estimators=optimal_model
)
final_model.fit( X_train , Y_train )
print( 'train r2 : ' , final_model.score(X_train , Y_train))
print( 'test r2 : ' , final_model.score(X_test , Y_test))
print( final_model.feature_name_ )
print( final_model.feature_importances_ )

# train r2 :  0.8463612233053909
# test r2 :  0.7246531097735276
# ['year', 'mileage', 'brand', 'model', 'title_status', 'color', 'state']
# [ 696 2819  247  448   49  307  594]


# # 7) joblib 저장 / 로드 
import joblib 
joblib.dump( final_model , './day18/gbm_model.pkl')     # 1)
# 다른 .py 파일 또는 메소드 가정
model = joblib.load ( './day18/gbm_model.pkl')


# 8) 예측
new_cars = pd.DataFrame([
    {'year': 2019, 'mileage': 25000, 'brand': 'ford',   'model': 'f-150',  'title_status': 'clean vehicle',     'color': 'white', 'state': 'texas'},
    {'year': 2014, 'mileage': 85000, 'brand': 'nissan', 'model': 'altima', 'title_status': 'salvage insurance', 'color': 'black', 'state': 'california'}
])
for col in cat_cols:
    new_cars[col] = new_cars[col].astype('category')

### 
preds = model.predict(new_cars)
print( '서빙모델 예측 (1번차량) 가격 : ' , preds[0] )
print( '서빙모델 예측 (1번차량) 가격 : ' , preds[0] )

# 서빙모델 예측 (1번차량) 가격 : 27983.4777071311
# 서빙모델 예측 (2번차량) 가격 : 635.4763331040908
