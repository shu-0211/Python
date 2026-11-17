import joblib
from lightgbm import LGBMClassifier, LGBMRegressor, early_stopping
import numpy as np
import optuna
import pandas as pd
from sklearn.metrics import f1_score
from sklearn.model_selection import KFold, train_test_split
# RangeIndex: 3810 entries, 0 to 3809
# Data columns (total 8 columns):
#  #   Column             Non-Null Count  Dtype  
# ---  ------             --------------  -----  
#  0   Area               3810 non-null   int64         	쌀알이 차지하는 면적
#  1   Perimeter          3810 non-null   float64           쌀알 외곽선의 전체 길이
#  2   Major_Axis_Length  3810 non-null   float64           쌀알의 긴 방향 길이
#  3   Minor_Axis_Length  3810 non-null   float64           쌀알의 짧은 방향 길이
#  4   Eccentricity       3810 non-null   float64           쌀알이 얼마나 길쭉한지 나타내는 값
#  5   Convex_Area        3810 non-null   int64             쌀알의 오목한 부분을 메워 볼록하게 감싼 면적
#  6   Extent             3810 non-null   float64           쌀알을 감싸는 직사각형에서 실제 쌀알이 차지하는 비율
#  7   Class              3810 non-null   str               Cammeo 또는 Osmancik
# dtypes: float64(5), int64(2), str(1)
# memory usage: 238.3 KB


#=============================================================================================================================================================
# 파일 불러오기 + 전처리 
#=============================================================================================================================================================
df = pd.read_csv('day19/Rice_Cammeo_Osmancik.csv')
df.info()

print("전체 결측치:", df.isnull().sum().sum())          # 열마다 결측치를 세고 전체 행 합친결과
# 전체 결측치: 0

# 소수점 3번째까지만 사용 
df = df.round(3)

X = df.drop(columns=['Class'])
Y = df['Class']

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42 , stratify=Y)


#=============================================================================================================================================================
# 모델 학습 및 평가 시킬 함수 정의
#=============================================================================================================================================================
optuna.logging.set_verbosity(optuna.logging.WARNING)
def objective(trial) : 
    cv = KFold( n_splits= 5 , shuffle= True , random_state=42 )
    cv_f1_scores = []                       # 각 폴드에서 계산한 F1 점수를 저장    
    best_iterations = []                    # 각 폴드 학습중 가장 성능이 좋은 반복 횟수를 저장 
    for train_idx , val_idx in cv.split( X_train , Y_train ) : 
        X_tr , X_val = X_train.iloc[ train_idx ] , X_train.iloc[ val_idx ]
        Y_tr , Y_val = Y_train.iloc[ train_idx ] , Y_train.iloc[ val_idx ]

        # 훈련모델 분류이므로 c
        model = LGBMClassifier(
            n_estimators=1000 , 
            learning_rate = trial.suggest_float('learning_rate' , 0.01 , 0.1 ),
            num_leaves=trial.suggest_int('num_leaves' , 3 , 30 ),
            max_depth=trial.suggest_int( 'max_depth' , 3 , 8),
            min_child_samples=trial.suggest_int('min_child_samples' , 10 , 50 ) , 
            subsample=trial.suggest_float('subsample' , 0.6 , 1.0 ),
            subsample_freq=1 , verbose= -1 , random_state=42 , n_jobs=-1 , 
            colsample_bytree=trial.suggest_float('colsample_bytree' , 0.6 , 0.9),
        )

        model.fit(X_tr , Y_tr , eval_set=[(X_val , Y_val )],
                  callbacks=[early_stopping(stopping_rounds=30 , verbose=False)])

         # 예측값으로 두 품종의 F1 점수를 구해 평균을 냄
        Y_pred = model.predict(X_val)
        f1 = f1_score(Y_val, Y_pred, average="macro")

        cv_f1_scores.append(f1)
        best_iterations.append(model.best_iteration_)
    trial.set_user_attr('best_n_estimators' , int(np.mean( best_iterations )))
    return np.mean(cv_f1_scores)    


#=============================================================================================================================================================
# 베이지안 최적화 수행 + 하이퍼 파라미터 도출
#=============================================================================================================================================================
sampler = optuna.samplers.TPESampler(seed=42)
study = optuna.create_study(direction='maximize' , sampler= sampler)
study.optimize(objective , n_trials=20)

print( '최적 하이퍼파라미터 : ' , study.best_params )
optimal_model = study.best_trial.user_attrs['best_n_estimators']
print( '최적 트리 : ' , optimal_model)
# 최적 하이퍼파라미터 :  {'learning_rate': 0.06381099809299767, 'num_leaves': 28, 'max_depth': 3, 'min_child_samples': 18, 'subsample': 0.6180909155642152, 'colsample_bytree': 0.6975990992289793}
# 최적 트리 :  70

#=============================================================================================================================================================
# 최적의 모델로 학습
#=============================================================================================================================================================
final_model = LGBMClassifier(
    random_state=42 , verbose=-1 , n_jobs=-1 , 
    subsample_freq=1 , 
    **study.best_params, 
    n_estimators=optimal_model
)
# 학습
final_model.fit(X_train , Y_train)

# 성능 확인
train_pred = final_model.predict(X_train)
test_pred = final_model.predict(X_test)

train_f1 = f1_score(Y_train, train_pred, average="macro")
test_f1 = f1_score(Y_test, test_pred, average="macro")

print("Train Macro F1:", train_f1)
print("Test Macro F1:", test_f1)

# Train Macro F1: 0.9329077701959058
# Test Macro F1: 0.9138009049773756


#=============================================================================================================================================================
# 모델 저장
#=============================================================================================================================================================
joblib.dump({ "model" : final_model , "f1_macro" :test_f1 }, './day19/lgbm_insurance_model.pkl' )
saved_data = joblib.load('./day19/lgbm_insurance_model.pkl')
model = saved_data['model']

new_rice = pd.DataFrame([
    {
        "Area": 15231,
        "Perimeter": 525.5789794921875,
        "Major_Axis_Length": 229.7498779296875,
        "Minor_Axis_Length": 85.09378814697266,
        "Eccentricity": 0.9288820028305054,
        "Convex_Area": 15617,
        "Extent": 0.5728955268859863
    },
    {
        "Area": 14656,
        "Perimeter": 494.3110046386719,
        "Major_Axis_Length": 206.0200653076172,
        "Minor_Axis_Length": 91.73097229003906,
        "Eccentricity": 0.8954049944877625,
        "Convex_Area": 15072,
        "Extent": 0.615436315536499
    },
    {
        "Area": 13447,
        "Perimeter": 455.64801025390625,
        "Major_Axis_Length": 183.95758056640625,
        "Minor_Axis_Length": 94.45813751220703,
        "Eccentricity": 0.8581028580665588,
        "Convex_Area": 13867,
        "Extent": 0.6259076595306396
    }
])

new_rice = new_rice.round(3)
# 쌀알 3개 예측
preds = model.predict(new_rice)

print("1번 쌀알 예측 품종:", preds[0])
print("2번 쌀알 예측 품종:", preds[1])
print("3번 쌀알 예측 품종:", preds[2])




#=============================================================================================================================================================
# 여러번의 시도 
#=============================================================================================================================================================
# 1) 소수점 제한 안뒀을때 
# 최적 하이퍼파라미터 :  {'learning_rate': 0.08491983767203796, 'num_leaves': 8, 'max_depth': 4, 'min_child_samples': 17, 'subsample': 0.7216968971838151, 'colsample_bytree': 0.7574269294896714}
# 최적 트리 :  50
# Train Macro F1: 0.9335918776417274
# Test Macro F1: 0.9095613048368953


# 2)        n_estimators=3000 ,   learning_rat = trial.suggest_float('learning_rate' , 0.001 , 0.08 )일때
# 최적 하이퍼파라미터 :  {'learning_rate': 0.06445049087596222, 'num_leaves': 24, 'max_depth': 4, 'min_child_samples': 44, 'subsample': 0.6523866478954822, 'colsample_bytree': 0.6643735324560622}
# 최적 트리 :  43
# Train Macro F1: 0.9332498652181056
# Test Macro F1: 0.9149606299212598

