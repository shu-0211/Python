# Recovery AI — 운동 회복 점수 예측

## 현재 실행 방법

`team` 폴더에서 아래 명령으로 FastAPI를 실행하고 [예측 화면](http://127.0.0.1:8000/)을 엽니다. 필요한 패키지가 없다면 먼저 `python -m pip install -r teamteam/backend/requirements.txt`를 실행하세요.

```powershell
python teamteam/backend/AppStart.py
```

화면에서 **예시 입력**을 누른 뒤 **회복 점수 예측하기**를 누르면 `POST /api/predict`가 `team.py`의 Ridge 모델로 회복 점수를 계산합니다. 모델은 `day16/model.pkl`에서 읽습니다. 이 경로는 `team` 폴더 기준 `../model.pkl`입니다. 이미 모델이 있다면 학습 명령은 필요하지 않습니다.

API는 최초 예측 요청에서 `team.py`와 같은 분할로 `athlete_recovery_synthetic.csv`의 테스트 데이터를 구성해 저장된 모델의 R²와 MAE를 계산합니다. 이후에는 메모리에 올린 모델과 평가 결과를 재사용합니다. 재학습한 모델을 반영하려면 서버를 다시 시작합니다. 요청 형식은 [Swagger](http://127.0.0.1:8000/docs)에서 확인할 수 있습니다.

입력 8개가 모두 필요합니다. 서버는 성별 `Male`과 `Female`을 각각 0과 1로, 스트레스 수준 `Low`, `Medium`, `High`를 각각 1, 2, 3으로 변환합니다. 학습에 사용한 범주와 입력 순서에 맞춘 뒤 저장된 Pipeline에 전달합니다.

<details>
<summary>받은 프로젝트의 기존 모델 설명과 발표 자료</summary>

## 발표용 코드 해설 — 먼저 읽기

이번 정리는 `day16/AppStart.py`, `day16/Controller.py`, `day16/Service.py`의 파일 분리와 서비스 객체 호출 방식을 기준으로 했습니다. 학습 부분은 `day15/s-08.py`의 ColumnTransformer·Pipeline, `practiceFile/mpractice3.py`의 Ridge·GridSearchCV 흐름을 참고합니다. 수업 원본은 수정하지 않았습니다.

### 1. 발표에서 먼저 보여줄 전체 흐름

```text
[사전 학습: 모델을 준비할 때 실행]
CSV → X/Y 분리 → 선수별 훈련/테스트 분리 → 전처리 + Ridge
    → GridSearchCV → 테스트 평가 → Pipeline과 평가 지표 저장

[서비스 실행: 사용자가 예측할 때마다 실행]
HTML 입력 → app.js의 Axios POST → AppStart의 라우터
    → Controller 입력 검증 → Service에서 DataFrame 생성
    → 저장 Pipeline.predict() → JSON 응답 → 화면에 점수 표시
```

발표 멘트: “학습과 예측을 분리했습니다. 학습은 train_model.py에서 미리 수행하고, 웹 요청에서는 저장된 모델을 불러와 예측만 합니다.”

### 2. AppStart.py — 서버 생성과 라우터 연결

```python
app = FastAPI(title="Recovery AI", version="2.0.0")
app.include_router(Controller.router)

if __name__ == "__main__":
    uvicorn.run("AppStart:app", host="127.0.0.1", port=8000, reload=True)
```

- `FastAPI()`는 요청을 받을 서버 객체를 만듭니다.
- `Controller.router`는 Controller.py에 있는 router 변수입니다.
- `include_router()`는 해당 라우터를 서버에 연결합니다.
- `__name__ == "__main__"`은 이 파일을 직접 실행했는지 확인합니다. 다른 파일에서 import할 때 서버가 다시 시작되지 않게 합니다.
- `AppStart:app`은 “AppStart.py에 있는 app 객체를 서버로 실행하라”는 뜻입니다.
- `host`는 접속 주소, `port`는 포트 번호입니다. `reload=True`는 소스 수정 시 서버를 자동 재시작하는 개발 옵션입니다.

CORS는 5500번 프론트와 8000번 백엔드처럼 출처가 다른 브라우저 요청을 허용하는 설정입니다. 모델의 예측 계산에는 관여하지 않습니다. CORS가 회원 인증을 대신하는 것도 아닙니다.

발표 멘트: “AppStart는 서버 설정만 담당하고, 실제 API 함수는 Controller에 분리했습니다.”

### 3. Controller.py — 주소, 입력 검사, Service 호출

```python
router = APIRouter(prefix="/api")

@router.post("/predict")
def predict(data: PredictRequest):
    # 실제 파일에서는 이 흐름을 try/except로 감싸 오류도 처리합니다.
    request_data = data.model_dump()
    result = recovery_service.predict(request_data)
    return result
```

`prefix="/api"`와 `"/predict"`가 합쳐져 `POST /api/predict` 주소가 됩니다. `data`는 브라우저에서 보낸 JSON을 검증해 담은 객체입니다. `model_dump()`는 이를 일반 딕셔너리로 바꿉니다. 그 딕셔너리를 Service에 전달하고, 반환된 딕셔너리를 그대로 응답하면 FastAPI가 JSON으로 변환합니다.

수업의 `item_service.save(item)`을 프로젝트의 `recovery_service.predict(request_data)`로 연결한 구조라고 설명하면 됩니다.

```python
Age: int | None = Field(default=None, ge=1)
Training_Duration_Min: int = Field(ge=1)
Training_Intensity: float | None = Field(default=None, ge=1, le=10)
```

- `int`는 정수, `float`는 실수입니다.
- `| None`은 미입력을 허용합니다. 요청 JSON의 `null`이 파이썬에서는 `None`이 됩니다.
- `default=None`이면 필드를 생략해도 미입력으로 처리합니다.
- `ge=1`은 1 이상, `le=10`은 10 이하입니다.
- 운동 시간에는 기본값을 주지 않아 필수값으로 만듭니다.
- `Literal`은 성별·스트레스처럼 정해진 문자열만 받게 합니다.
- `strict=True`는 숫자 문자열과 bool의 자동 숫자 변환을 막습니다.

Pydantic·HTTPException·로깅·검증 오류 응답은 프로젝트 요구사항을 만족하기 위한 보완 코드입니다. 수업에서 사용한 기본 dict 예제와 완전히 같은 코드라고 설명하지 않습니다. `def`로 작성한 동기 API는 FastAPI의 작업 스레드에서 실행되며, `async`를 붙이는 것만으로 모델 계산이 빨라지는 것은 아닙니다.

발표 멘트: “Controller는 입력값을 확인하고 Service에 전달합니다. 모델의 계산 로직은 Controller에 넣지 않았습니다.”

### 4. Service.py — 클래스, 생성자, self

```python
class RecoveryService:
    def __init__(self):
        self.model = None
        self.metrics = None

recovery_service = RecoveryService()
```

`class`는 서비스 객체의 설계도입니다. `RecoveryService()`로 객체를 만들면 생성자 `__init__()`가 실행됩니다. `self`는 현재 객체를 가리키며, `self.model`은 같은 객체의 메서드들이 함께 사용하는 변수입니다. 마지막 줄에서 만든 `recovery_service`를 Controller가 import합니다. 수업의 `ItemService`와 `item_service` 관계와 같습니다.

```python
if self.model is None:
    self.load_model()
```

첫 요청에서는 `joblib.load()`로 저장된 모델과 지표를 읽습니다. 이후에는 로드한 객체를 재사용합니다. 모델 파일이 없으면 503을 반환하며, 다른 모델이나 임의 점수로 대신하지 않습니다.

### 5. Service.py — 딕셔너리를 DataFrame으로 변경

```python
row = {}
for column in self.columns:
    value = data.get(column)
    if value is None:
        row[column] = np.nan
    else:
        row[column] = value

df = pd.DataFrame([row], columns=self.columns)
```

`data.get(column)`은 딕셔너리에서 해당 컬럼의 값을 읽습니다. `row`는 입력 한 건이며 `[row]`는 한 행을 담은 리스트입니다. `columns`는 학습할 때 사용한 8개 컬럼 이름과 순서를 고정합니다. `np.nan`은 모델 전처리기가 인식하는 결측값입니다.

`if value is None`으로 검사하므로 카페인 0은 그대로 남습니다. `if not value`로 검사하면 0도 빈 값처럼 취급할 수 있으므로 사용하지 않습니다. Service는 결측값을 표시만 하고, 실제 중앙값·최빈값 대체는 학습된 Pipeline이 수행합니다.

### 6. Service.py — 예측 결과와 점수 보정

```python
predictions = self.model.predict(df)
raw_prediction = float(predictions[0])

score = raw_prediction
if score < 0:
    score = 0.0
elif score > 100:
    score = 100.0
```

`predict(df)`는 행별 예측값을 반환합니다. 입력이 한 행이므로 첫 번째 값 `[0]`을 읽고 파이썬 `float`로 바꿉니다. 회귀 모델은 0~100 밖의 값을 낼 수 있어 화면 표시 점수만 제한합니다. 원본값은 `raw_prediction`, 보정 여부는 `score_was_clipped`로 따로 응답합니다. R²와 MAE는 보정 전 원본 예측값으로 평가한 수치입니다.

### 7. train_model.py — X/Y 분리와 데이터 분할

```python
X = df[columns]
Y = df["Recovery_Score"]
groups = df["Athlete_ID"]
```

X는 문제지인 8개 입력 특성, Y는 정답지인 회복 점수입니다. `Athlete_ID`는 X에 넣지 않고 분할에만 씁니다.

일반적인 `train_test_split`은 행을 나눕니다. 이 CSV에는 같은 선수의 다른 날 기록이 있으므로 `GroupShuffleSplit`으로 선수를 묶어서 나눕니다. 선수 240명의 6,705행은 훈련, 다른 선수 60명의 1,674행은 테스트로 사용합니다. 두 집합의 선수 ID는 겹치지 않습니다. `iloc`은 분할로 얻은 정수 위치의 행을 선택하는 Pandas 문법입니다.

그룹 분할은 이 데이터의 반복 기록 때문에 필요한 보완입니다. 발표에서는 “수업의 훈련/테스트 분리 원칙을 유지하면서 선수 중복에 의한 정보 누수를 줄였습니다”라고 설명합니다.

### 8. 전처리와 Pipeline

```python
num_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])
cat_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
])
pp = ColumnTransformer(transformers=[
    ("num", num_pipe, num_features),
    ("cat", cat_pipe, cat_features),
])
pipe = Pipeline([("pp", pp), ("model", Ridge())])
```

수치형 6개에는 결측값 대체와 표준화를 적용합니다. `StandardScaler`는 훈련 데이터의 평균·표준편차를 학습해 단위 차이를 줄이며, 무조건 0~1로 바꾸는 것은 아닙니다. 범주형 2개에는 최빈값 대체와 원-핫 인코딩을 적용합니다. `ColumnTransformer`는 컬럼 종류별로 다른 처리를 적용합니다.

Pipeline은 전처리부터 예측까지 순서대로 묶은 객체입니다. 훈련 데이터에 `fit()`할 때 중앙값·스케일·회귀 계수를 학습하고, 테스트나 API에서 `predict()`할 때는 이미 학습한 규칙을 적용합니다. API 입력으로 전처리기를 다시 `fit()`하지 않습니다.

### 9. Ridge와 GridSearchCV

```python
param_grid = {"model__alpha": [0.01, 0.1, 1.0, 10.0, 100.0]}
grid = GridSearchCV(pipe, param_grid, cv=cv, scoring="r2", n_jobs=1, error_score="raise")
grid.fit(X_train, Y_train, groups=train_groups)
best_model = grid.best_estimator_
```

Ridge는 계수의 크기에 L2 규제를 적용하는 회귀 모델입니다. alpha는 규제 강도이며, 크다고 항상 성능이 좋은 것은 아닙니다. `model__alpha`의 `model`은 Pipeline의 단계 이름, `alpha`는 그 단계의 매개변수입니다. 두 밑줄로 연결합니다.

GridSearchCV는 훈련 데이터 안에서 5개 후보를 5분할 검증합니다. 내부 검증도 `GroupKFold`로 선수를 나눕니다. 전처리를 Pipeline 안에 두어 각 검증의 훈련 부분에서만 전처리 규칙을 배웁니다. `best_estimator_`는 선택된 alpha로 전체 훈련 데이터에 다시 학습된 Pipeline입니다. 최종 테스트 데이터는 alpha 선택에 사용하지 않습니다.

### 10. 모델 평가와 저장

```python
Y_pred = best_model.predict(X_test)
test_r2 = float(r2_score(Y_test, Y_pred))
test_mae = float(mean_absolute_error(Y_test, Y_pred))
```

R²는 상수 예측을 기준으로 모델이 변동을 얼마나 설명하는지 평가합니다. 현재 별도 테스트 R²는 약 0.6436이며, “정확도 64.36%”라는 뜻이 아닙니다. R²는 음수가 될 수도 있습니다. MAE 약 13.05점은 이 테스트 집합에서 실제값과 예측값의 절대 차이가 평균 약 13.05점이라는 뜻입니다. 개인마다 오차가 항상 13.05점 이하라는 뜻은 아닙니다.

`joblib.dump(best_model, file)`은 전처리를 포함한 Pipeline 전체를 파일로 저장합니다. 지표도 별도 파일에 저장하고 Service가 읽습니다. `xb` 모드와 기존 파일 검사는 학습 결과를 실수로 덮어쓰지 않기 위한 보완입니다. 경로 처리, 데이터 해시, 버전 기록도 실행·재현을 위한 보조 코드이므로 발표에서는 핵심 학습 흐름을 먼저 설명하면 됩니다.

### 11. 약 3분 발표 대본

“저희는 운동과 생활습관 정보를 입력하면 회복 점수를 예측하는 Recovery AI를 만들었습니다. 교육용 합성 데이터를 사용하며 의료 진단을 제공하지는 않습니다.

코드는 수업에서 배운 방식으로 AppStart, Controller, Service로 분리했습니다. AppStart는 FastAPI 객체를 만들고 Controller의 router를 연결합니다. 사용자가 예측 버튼을 누르면 JavaScript가 8개 입력값을 읽고 Axios로 POST /api/predict에 JSON을 전송합니다.

Controller는 자료형과 범위를 검사합니다. 운동 시간만 필수이고 나머지는 미입력을 허용합니다. 검증된 데이터를 딕셔너리로 바꾼 다음 Service 객체의 predict 메서드를 호출합니다.

Service는 저장된 Pipeline을 읽고 입력 딕셔너리를 한 행짜리 DataFrame으로 변환합니다. 비어 있는 값은 결측값으로 표시합니다. 카페인 0mg은 정상 값이므로 그대로 보존합니다. 결측값 대체와 표준화, 인코딩은 학습된 Pipeline 안에서 동일하게 처리합니다.

모델 학습은 웹 요청과 분리했습니다. 8개 입력을 X, Recovery_Score를 Y로 정하고 같은 선수의 기록이 훈련과 테스트에 섞이지 않도록 분리했습니다. 숫자는 중앙값 대체와 표준화, 문자는 최빈값 대체와 원-핫 인코딩을 적용했습니다. 이후 Ridge를 연결하고 GridSearchCV로 alpha를 선택했습니다.

별도 테스트 R²는 약 0.6436, MAE는 약 13.05점이었습니다. R²를 개인별 예측의 정확도 퍼센트로 해석하지 않았습니다. 최적 Pipeline과 실제 평가 지표를 저장하고, API에서는 예측 결과와 이 지표를 반환합니다.

프론트는 응답을 받은 후 점수와 게이지를 표시합니다. 요청 중에는 버튼을 잠그고, 입력이 바뀌면 이전 결과를 지워 잘못된 결과로 오해하지 않도록 했습니다.”

### 12. 예상 질문에 대한 짧은 답변

| 질문 | 답변 |
| --- | --- |
| Controller와 Service를 왜 나눴나요? | HTTP 요청·응답 처리와 실제 예측 로직의 역할을 구분하기 위해서입니다. |
| 왜 API 요청 때 학습하지 않나요? | 학습은 사전에 끝내고 저장 모델로 추론만 해야 불필요한 재학습을 피할 수 있기 때문입니다. |
| 미입력을 왜 0으로 보내지 않나요? | 0mg처럼 실제 의미가 있는 값과 비어 있는 값을 구분해야 하기 때문입니다. |
| 성별·스트레스는 왜 인코딩하나요? | Ridge가 처리할 수 있도록 문자열 범주를 숫자 열로 바꾸기 위해서입니다. |
| 선수 단위로 나눈 이유는 무엇인가요? | 같은 선수의 반복 기록이 테스트에 섞여 평가가 낙관적으로 되는 것을 줄이기 위해서입니다. |
| 59.39점은 정답인가요? | 저장된 모델의 추정값이며 실제 회복 상태를 보장하는 진단값은 아닙니다. |
| R²와 MAE를 요청마다 계산하나요? | 아닙니다. 사전에 별도 테스트 데이터로 평가해 저장한 값을 함께 반환합니다. |
| 100점 밖으로 예측되면 어떻게 하나요? | 표시 점수만 제한하고 원본 예측값과 보정 여부를 구분해 응답합니다. |

프론트엔드 코드의 세부 해설은 `../frontend/README.md`의 발표용 코드 해설에 이어집니다.

기존 team 프로젝트를 운동·생활습관 8개 입력으로 회복 점수를 예측하도록 수정했습니다. AppStart → Controller → Service 구조와 HTML/CSS/Vanilla JavaScript/Axios를 유지했습니다. 새 소스 파일·폴더·패키지는 추가하지 않았습니다. 파일명 변경도 없습니다.

사용자 승인에 따라 기존 models 폴더에 recovery_model.pkl, recovery_metrics.pkl 두 학습 결과물만 추가했습니다. 이전 calories_model.pkl과 metrics.pkl은 보존하며 현재 API에서는 읽지 않습니다. 원본 CSV와 team 외부 수업 파일은 수정하지 않았습니다.

## 파일 역할과 호출 흐름

| 기존 파일 | 역할 |
| --- | --- |
| AppStart.py | Recovery AI FastAPI 생성, CORS, Controller 라우터, Uvicorn |
| Controller.py | Pydantic으로 8개 입력 검증, POST /api/predict, 안전한 오류 응답 |
| Service.py | 회복 Pipeline과 지표 로드, 원본 DataFrame 생성, 추론, 범위 경고 |
| train_model.py | CSV 읽기, 선수 단위 분할, 전처리·Ridge·GridSearchCV, 모델·지표 저장 |
| test_backend.py | 실제 저장 모델 및 입력·오류·분할·보정 검증 |
| ../frontend/index.html | 8개 입력과 회복 점수 결과 화면 |
| ../frontend/style.css | 기존 네이비·민트 디자인과 반응형 레이아웃 |
| ../frontend/app.js | null·0·소수 변환, 요청 잠금, Axios 요청, 실제 결과 표시 |

브라우저 입력 → Controller의 PredictRequest 검증 → recovery_service.predict() → 8개 컬럼의 DataFrame → 저장된 Pipeline.predict() → JSON → 결과 카드 순서입니다. API 요청 중 학습하지 않습니다. 모델은 최초 요청에 로드하고 재사용하며, 모델 교체 후 서버를 재시작해야 합니다.

## 실행 방법

아래 명령은 프로젝트 최상위 python 폴더에서 각각 별도 터미널로 실행합니다.

```powershell
.\.venv\Scripts\python.exe team/backend/AppStart.py
```

```powershell
.\.venv\Scripts\python.exe -m http.server 5500 --bind 127.0.0.1 --directory team/frontend
```

화면: http://127.0.0.1:5500/  
Swagger: http://127.0.0.1:8000/docs

화면에서 예시 입력 → 회복 점수 예측하기를 누릅니다. 예시 버튼 자체는 요청하지 않습니다. 같은 포트에 서버가 있으면 중복 실행하지 않습니다. 종료는 각 터미널에서 Ctrl+C입니다. VS Code에서는 .venv 인터프리터를 선택하고 기존 AppStart.py를 실행해도 됩니다. 루트 / 화면은 없으므로 백엔드의 / 경로 404는 정상입니다.

자동 재시작 기능의 Windows 프로세스 통신이 제한되는 환경에서는 다음 명령을 사용합니다. 이 모드에서는 수정 후 직접 재시작합니다.

```powershell
.\.venv\Scripts\python.exe -B -m uvicorn AppStart:app --app-dir team/backend --host 127.0.0.1 --port 8000
```

기존 가상환경에 필요한 패키지가 있어 새 패키지는 설치하지 않았습니다. 다른 PC에서는 학습 당시와 같은 버전의 기존 requirements.txt를 확인해 준비하세요. 직렬화된 모델은 신뢰하는 팀원의 파일만 읽어야 합니다.

## 실제 데이터 확인

team/athlete_recovery_synthetic.csv: **8,379행, 19개 컬럼**, 선수 300명. 같은 선수의 일별 기록이 반복되며 Athlete_ID의 중복 기록은 8,079행입니다.

| 컬럼 | 타입 | 결측 수 | 최솟값~최댓값 또는 고유 범주 |
| --- | --- | --- | --- |
| Athlete_ID | 정수 | 0 | 1000~1299 |
| Day | 정수 | 0 | 1~28 |
| Day_of_Week | 정수 | 0 | 1~7 |
| Week | 정수 | 0 | 1~4 |
| Age | 정수 | 0 | 18~41 |
| Gender | 문자열 | 0 | Male, Female, Non-binary |
| Sport_Type | 문자열 | 0 | Team Sport, Endurance, Strength, Combat, Mixed |
| Training_Type | 문자열 | 0 | HIIT, Cardio, Yoga, Strength, Rest |
| Training_Duration_Min | 정수 | 0 | 10~115 |
| Training_Intensity | 실수 | 1 | 1~10 |
| Sleep_Duration_Hours | 실수 | 604 | 5~9.5 |
| Caffeine_Intake_mg | 정수 | 0 | 0~400 |
| Stress_Level | 문자열 | 0 | Low, Medium, High |
| Resting_Heart_Rate | 정수 | 0 | 38~81 |
| HRV_ms | 정수 | 0 | 22~115 |
| Mood_Score | 실수 | 0 | 1~9.5 |
| Muscle_Soreness | 실수 | 0 | 1~10 |
| Energy_Level | 실수 | 0 | 1~10 |
| Recovery_Score | 실수 | 0 | 0~100 |

최솟값과 최댓값은 결측값을 제외하고 확인했습니다. 출처는 사용자가 제공한 Athlete Recovery & Biometric Performance Dataset이며, 로컬 CSV만 조사했습니다. 원본 자료의 추가 컬럼은 보존하고 확정된 8개만 모델 X로 사용합니다.

## 입력 규격

| 입력 | 논리적 허용 범위 | CSV 관측 범위 |
| --- | --- | --- |
| Age | 1 이상 정수 또는 null | 18~41 |
| Gender | Male / Female / Non-binary 또는 null | 동일 |
| Training_Duration_Min | 필수, 1 이상 정수 | 10~115 |
| Training_Intensity | 1~10 실수 또는 null | 1~10 |
| Sleep_Duration_Hours | 0~24 실수 또는 null | 5~9.5 |
| Stress_Level | Low / Medium / High 또는 null | 동일 |
| Caffeine_Intake_mg | 0 이상 정수 또는 null | 0~400 |
| Muscle_Soreness | 1~10 실수 또는 null | 1~10 |

운동 시간을 제외한 7개는 생략해도 null로 처리합니다. 숫자 문자열, bool, 비정상 수치, 소수로 전달한 정수 필드, 잘못된 범주, 추가 입력 필드는 422입니다. 운동 시간 60.5분은 정수 규격에 맞지 않습니다. 강도 7.5와 근육통 4.5는 그대로 허용합니다. 카페인 0mg과 null은 다른 값입니다.

나이 45, 운동 시간 9분 또는 116분, 수면 4시간, 카페인 401mg은 관측 범위 밖 경고를 주되 요청을 허용합니다. 음수 나이·카페인, 강도·근육통의 1~10 위반, 하루 24시간을 넘는 수면은 거절합니다. 선택 항목 7개 중 4개 이상이 비어 있으면 신뢰도가 낮아질 수 있음을 안내합니다. 입력이 많다는 이유로 특정 신뢰도 숫자를 만들어내지 않습니다.

## 학습과 결측값 처리

별도 train_model.py는 확정된 8개 X와 Recovery_Score Y를 사용합니다.

- 수치형 6개: Age, Training_Duration_Min, Training_Intensity, Sleep_Duration_Hours, Caffeine_Intake_mg, Muscle_Soreness
- 범주형 2개: Gender, Stress_Level

숫자는 SimpleImputer(median) → StandardScaler, 범주는 SimpleImputer(most_frequent) → OneHotEncoder(handle_unknown="ignore")로 처리합니다. 두 전처리를 ColumnTransformer로 묶고 Ridge와 함께 하나의 Pipeline으로 저장합니다. 중앙값·최빈값·스케일은 훈련 데이터에서만 학습합니다. Service는 null을 np.nan으로 바꾸고 컬럼 순서를 맞출 뿐, 대체값을 직접 계산하지 않습니다.

GroupShuffleSplit(random_state=42, test_size=0.2)로 선수 240명의 6,705행을 훈련, 다른 선수 60명의 1,674행을 테스트로 나눴습니다. 선수 ID의 교집합은 없습니다. Athlete_ID는 분할에만 쓰고 예측 입력에는 포함하지 않습니다.

GridSearchCV의 내부 검증도 GroupKFold(5분할)로 선수 단위를 유지합니다. alpha 후보는 0.01, 0.1, 1.0, 10.0, 100.0이며 n_jobs=1입니다.

| 실제 평가 항목 | 결과 |
| --- | --- |
| 최적 alpha | 10.0 |
| 내부 교차 검증 R² | 0.676657127593894 |
| 별도 테스트 R² | 0.643623974517451 |
| 별도 테스트 MAE | 13.050389989305797점 |

R²와 MAE는 **원본 모델 예측값**으로 계산했습니다. API에는 별도 테스트 점수를 반환합니다. 이 점수는 개인의 회복 상태에 대한 신뢰도나 의료 정확도가 아니며, 입력을 비운 경우의 성능을 별도로 평가한 수치도 아닙니다.

회복 모델 파일이 없는 새 환경에서만 다음 명령을 실행합니다.

```powershell
.\.venv\Scripts\python.exe -B team/backend/train_model.py
```

두 회복 결과 파일 중 하나라도 있으면 덮어쓰지 않고 FileExistsError로 중단합니다. 재학습 전에는 두 파일을 함께 보관하고 서버를 종료한 상태에서 진행하세요. 이전 칼로리 모델과 지표는 이 과정에서 사용하거나 변경하지 않습니다.

## API와 실제 응답

POST http://127.0.0.1:8000/api/predict  
Content-Type: application/json

```json
{
  "Age": 25,
  "Gender": "Male",
  "Training_Duration_Min": 60,
  "Training_Intensity": 7.5,
  "Sleep_Duration_Hours": 7.5,
  "Stress_Level": "Medium",
  "Caffeine_Intake_mg": 150,
  "Muscle_Soreness": 4.5
}
```

저장된 회복 모델의 실제 응답:

```json
{
  "predicted_recovery_score": 59.388869693520164,
  "raw_prediction": 59.388869693520164,
  "score_was_clipped": false,
  "r2_score": 0.643623974517451,
  "mae": 13.050389989305797,
  "warnings": []
}
```

기본 응답 키는 predicted_recovery_score와 r2_score이며, 나머지는 추가 설명 필드입니다. 프론트에는 59.39 / 100점, R² 0.6436으로 표시됩니다. 숫자는 응답 예시 문서일 뿐 코드의 반환값으로 하드코딩하지 않습니다.

Training_Duration_Min에 60만 입력한 실제 예측은 47.00089426473618점이었습니다. 나머지 7개 값은 null로 전송되고 학습된 Pipeline이 처리합니다.

회귀 원본 예측값은 0~100 밖으로 나갈 수 있습니다. Service는 min(100, max(0, raw_prediction))으로 **표시 점수만 제한**하며, raw_prediction을 보존하고 score_was_clipped로 보정 여부를 알립니다. 프론트는 보정된 경우 원본값과 범위를 제한했다는 문구를 표시합니다. 유한하지 않은 예측은 오류로 처리합니다. 가짜 예측값을 대신 만들지 않습니다.

## 오류와 CORS

| 상황 | 상태 |
| --- | --- |
| 필수 운동 시간 누락, 잘못된 타입·범주·논리적 범위 | 422 |
| 유한하지 않은 모델 예측 | 422 |
| 회복 모델 또는 지표 없음 | 503 |
| 모델 컬럼·타깃·지표 불일치, 결측값 처리 실패 등 | 500 |

오류 사유는 detail로 반환합니다. 내부 경로·스택은 응답에 포함하지 않고 서버 로그에 남깁니다. 회복 모델이 없으면 이전 모델로 대체하거나 API에서 학습하지 않습니다.

허용 출처는 http://127.0.0.1:5500 과 http://localhost:5500 입니다. 다른 포트에서 실행하면 AppStart.py의 allow_origins를 실제 주소에 맞추세요. POST 및 Content-Type을 허용하며 OPTIONS는 CORSMiddleware가 처리합니다.

## 검증

```powershell
.\.venv\Scripts\python.exe -B team/backend/test_backend.py
```

16개 테스트가 통과했습니다. 실제 Pipeline 직접 추론과 API 일치, null 처리, 소수·0·모든 범주, 범위 경고, 잘못된 입력, 모델 누락·컬럼·타깃 불일치, 내부 오류 은닉, 보정 시 원본값 보존, CORS, 선수 분리와 테스트 평가값 재계산, 덮어쓰기 방지를 확인합니다. 오류 분기 검증만 메모리 객체를 잠시 대체하며, 실제 모델 파일은 이동·삭제하지 않습니다.

실제 Chrome에서도 Axios CDN → FastAPI → 회복 Pipeline → 결과 카드 흐름을 확인했습니다. 예시 입력, 7개 null, 카페인 0, 소수 보존, 중복 요청 방지, 결과 초기화, 관측 범위 경고, 전체 초기화가 통과했습니다. API 요청 차단을 통한 연결 실패 안내도 검사했습니다. 1280·768·390·320px에서 가로 넘침과 PC/모바일 배치를 검사했습니다. Swagger Try it out → Execute는 실제 회복 점수·R²와 함께 HTTP 200을 반환했고 처리되지 않은 JavaScript 예외는 없었습니다.

TestClient는 현재 환경에서 httpx 관련 폐기 예정 경고를 표시하지만 테스트는 통과합니다. 새 패키지는 설치하지 않았습니다. 배포와 다른 팀원 PC의 환경 검증은 수행하지 않았습니다.

본 서비스는 교육용 합성 데이터를 기반으로 한 예측 모델이며, 실제 건강 상태에 대한 의학적 판단을 제공하지 않습니다.

</details>
