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
import optuna
optuna.logging.set_verbosity(optuna.logging.WARNING)

# 4) 목적함수 만들기
def objective( trail ) :
    pass

# 3) study = optuna.create_study(direction='maximize'/'minimize' , sampler= sampler)
# 현재 실습은 회귀모델이며 r2 결정계수 평가지표 사용할 예정
sampler = optuna.samplers.TPESampler( seed = 42 )
study = optuna.create_study(direction='maximize' , sampler= sampler)    # 평가지표가 높은걸 원하면 max , 낮은건 min
# study.optimize( 목적함수 , n_trials=반복수)
study.optimize( objective , n_trials=20)     # 목적함수가 반복수만큼 실행됨. 목적함수에 소괄화를 안쓰는 이유는 함수 자체를 부르기 위해(콜백함수)
# 실무에서는 100단위로 작성
