# Recovery AI — 나의 운동 회복 점수 예측

## 현재 실행 방법

`team` 폴더에서 `python teamteam/backend/AppStart.py`를 실행하고 [예측 화면](http://127.0.0.1:8000/)을 엽니다. FastAPI가 화면과 API를 함께 제공합니다.

8개 항목을 입력하거나 **예시 입력**을 누른 뒤 **회복 점수 예측하기**를 누릅니다. 화면은 브라우저의 `fetch`로 JSON을 전송하고 응답에서 예측 점수와 테스트 R²·MAE를 읽어 표시합니다. 입력을 바꾸면 이전 결과가 지워집니다.

<details>
<summary>받은 프로젝트의 기존 화면 설명과 발표 자료</summary>

## 발표용 코드 해설 — 화면에서 API까지

### 1. HTML, CSS, JavaScript의 역할

HTML은 입력 폼·버튼·결과 영역의 구조, CSS는 색상·간격·PC/모바일 배치, JavaScript는 입력값 변환·이벤트·API 통신·결과 표시를 담당합니다. 파일을 나눠 각 역할을 쉽게 찾도록 했습니다. 기존 디자인과 8개 입력 항목은 변경하지 않았습니다.

```html
<input id="Training_Duration_Min" name="Training_Duration_Min"
       type="number" min="1" step="1" required placeholder="미입력">
```

`id`는 JavaScript가 해당 요소를 찾는 이름입니다. `type="number"`는 숫자 입력, `min="1"`은 최솟값, `step="1"`은 정수 단위, `required`는 필수 입력입니다. 미입력을 알리는 placeholder는 실제 입력값이 아니므로 서버로 보내지 않습니다. 강도와 근육통은 `step="any"`로 소수를 허용합니다. 입력값 검사는 브라우저뿐 아니라 백엔드에서도 수행합니다.

CSS의 `.workspace`는 PC에서 grid 2열로 배치하고, `@media (max-width: 620px)`에서는 1열로 바꿉니다. JavaScript로 화면 크기를 계산하는 대신 CSS 반응형 규칙을 사용합니다.

### 2. DOM 조회와 상태 변수

```javascript
const form = document.getElementById("prediction-form");
let isLoading = false;
let hasResult = false;
```

`document`는 현재 HTML 문서, `getElementById()`는 id가 같은 요소를 찾는 메서드입니다. const에는 조회한 요소를 보관하고, 바뀌는 상태에는 let을 사용합니다. `isLoading`은 요청 중인지, `hasResult`는 표시된 예측 결과가 있는지 나타냅니다. React 상태 관리가 아니라 일반 JavaScript 변수입니다.

### 3. 빈 값과 숫자 0을 구분하는 함수

```javascript
function getNumberOrNull(id) {
  const value = document.getElementById(id).value.trim();
  if (value === "") {
    return null;
  }
  return Number(value);
}
```

숫자 입력창의 value도 문자열입니다. trim()으로 앞뒤 공백을 없앤 뒤 빈 문자열이면 null을 반환합니다. 값이 있으면 Number()로 숫자로 바꿉니다. 빈 문자열부터 검사하지 않으면 Number("")가 0이 됩니다. 이 함수에서는 미입력이 null, 문자열 "0"은 숫자 0, 문자열 "7.5"는 숫자 7.5가 됩니다. parseInt()를 사용하지 않아 소수값을 자르지 않습니다.

발표 멘트: “카페인 0mg은 실제 입력값이므로 미입력과 구분했습니다.”

### 4. 요청 객체 생성

```javascript
const data = {};
for (const name of fieldNames) {
  // 실제 함수에서는 문자열 선택값과 숫자 입력값을 나누어 처리합니다.
  // data[name]에 변환한 값을 저장합니다.
}
```

fieldNames에는 CSV와 같은 8개 키가 들어 있습니다. for문으로 각 입력값을 읽고 객체에 저장합니다. `data[name]`은 name 변수에 담긴 문자열을 키로 사용합니다. 예를 들어 name이 Age일 때 data[name]은 data.Age에 해당합니다. 성별·스트레스는 원본 범주 문자열을 유지하고, 숫자는 getNumberOrNull()로 변환합니다. 이때 실제 중앙값을 채우지 않습니다.

### 5. submit 이벤트와 유효성 검사

```javascript
form.addEventListener("submit", async function (event) {
  event.preventDefault();
  if (isLoading) {
    return;
  }
  if (!form.reportValidity()) {
    return;
  }
  // 실제 파일에서는 여기서 입력을 읽고 Axios 요청을 보냅니다.
});
```

addEventListener()는 이벤트가 발생했을 때 실행할 함수를 등록합니다. submit을 사용하면 버튼 클릭과 Enter 제출을 함께 처리합니다. preventDefault()는 기본 폼 제출로 페이지가 새로고침되는 것을 막습니다. return은 현재 함수의 실행을 중단합니다. reportValidity()는 HTML의 required·min·max·step 조건을 확인하고 오류를 안내합니다. 요청 중에는 입력과 버튼을 disabled로 잠가 중복 요청과 입력·결과 불일치를 줄입니다.

### 6. Axios POST와 async/await

```javascript
const response = await axios.post(API_URL, requestData, {
  headers: { "Content-Type": "application/json" },
  timeout: 15000
});
showResult(response.data);
```

첫 번째 인자는 서버 주소, 두 번째는 요청 본문에 넣을 객체, 세 번째는 요청 설정입니다. Axios가 객체를 JSON으로 전송합니다. timeout은 15초이며 응답을 무한히 기다리지 않게 합니다.

async 함수 안의 await는 요청이 완료된 뒤 다음 줄을 실행하도록 합니다. 기다리는 동안 브라우저 화면 전체가 멈추는 것은 아닙니다. response는 Axios 응답 전체이고 response.data는 서버에서 받은 JSON 본문입니다. 실제 파일에서는 응답 숫자의 자료형과 범위를 확인한 뒤 showResult()를 호출합니다.

### 7. 결과 DOM 변경과 게이지

```javascript
document.getElementById("recovery-value").textContent =
  data.predicted_recovery_score.toLocaleString("ko-KR", { maximumFractionDigits: 2 });
document.getElementById("recovery-gauge").style.width =
  `${data.predicted_recovery_score}%`;
```

textContent는 결과 영역의 글자를 바꿉니다. maximumFractionDigits는 화면 표시 자릿수이며 원본 모델 값을 다시 학습하거나 변경하는 것이 아닙니다. 0~100 점수를 CSS의 0~100% 너비와 연결해 게이지를 만듭니다. 게이지는 점수의 시각화이며 개인별 예측 신뢰도 퍼센트가 아닙니다.

서버가 0~100 범위로 점수를 보정했다면 원본값과 보정 사실도 표시합니다. R²는 같은 요청에서 계산한 개인 평가가 아니라 저장된 모델의 테스트 지표입니다.

### 8. try/catch/finally

- try: Axios 요청과 정상 응답 처리를 실행합니다.
- catch: 연결 실패, 서버 오류, 올바르지 않은 응답을 안내합니다.
- finally: 성공·실패에 관계없이 버튼과 입력 잠금을 해제합니다.

서버가 오류 JSON을 응답한 경우와 응답 자체를 받지 못한 경우는 구분합니다. 실패할 때 이전 결과를 지우고 가짜 점수를 보여주지 않습니다. 서버 내부 경로나 스택은 화면에 표시하지 않습니다.

### 9. 입력 변경, 예시, 초기화

```javascript
document.getElementById(name).addEventListener("input", handleInputChange);
```

함수명 뒤에 괄호를 쓰지 않는 이유는 지금 실행하는 것이 아니라 이벤트 발생 때 실행할 함수를 전달하기 때문입니다. 입력을 바꾸면 기존 결과를 지우고 범위·결측값 안내를 갱신합니다.

예시 버튼은 8개 값을 채울 뿐 자동 요청하지 않습니다. 전체 초기화 버튼은 form.reset()과 clearResult()로 입력·점수·게이지·경고를 초기화합니다. 관측 범위 밖 경고와 논리적으로 잘못된 값의 차단은 구분합니다. 나이 45세는 경고 후 요청할 수 있지만 음수 나이는 거절합니다.

### 10. 화면 시연 순서와 발표 멘트

1. 빈 화면: “모든 입력은 미입력이며 서버 응답 전에는 점수를 표시하지 않습니다.”
2. 예시 입력: “숫자와 선택값을 채웁니다. 아직 API 요청은 보내지 않았습니다.”
3. 예측 버튼: “JSON으로 전송하고, 서버의 실제 응답을 받아 약 59.39점을 표시합니다.”
4. 입력 변경: “이전 입력에 대한 결과가 남지 않도록 초기화합니다.”
5. 전체 초기화 후 운동 시간 60분만 입력: “나머지 7개를 null로 보내고 학습된 Pipeline이 처리합니다.”
6. 카페인 0mg: “숫자 0은 결측값과 구분합니다.”

백엔드 README의 약 3분 발표 대본과 이어서 사용하면 됩니다. 실제 수업 예제를 그대로 사용한 부분과 프로젝트 입력 검사·오류 처리에 필요한 보완 부분은 구분해서 설명하세요.

기존 프론트엔드를 운동·생활습관 8개 입력의 회복 점수 서비스로 수정했습니다. 기존 네이비·민트 디자인, PC 2열·모바일 1열 배치, 기본 이벤트 흐름을 유지합니다. HTML5·CSS3·Vanilla JavaScript·Axios CDN을 사용하며 React·빌드·추가 패키지는 필요하지 않습니다. 회원가입·DB·인증·기록 저장 기능은 없습니다.

## 기존 파일 역할

| 파일 | 역할 |
| --- | --- |
| index.html | 정확히 8개 입력 폼, 회복 점수·R²·게이지, 교육용 안내 |
| style.css | 기존 반응형 레이아웃과 디자인 |
| app.js | 입력 검사, null·0·소수 변환, Axios 요청, 실제 응답 표시 |
| README.md | 실행 및 백엔드 연결 안내 |

새 프론트 소스 파일이나 폴더를 만들지 않았고 이름도 변경하지 않았습니다.

## 실행

프로젝트 최상위 python 폴더에서 실행합니다.

```powershell
python -m http.server 5500 --bind 127.0.0.1 --directory team/frontend
```

http://127.0.0.1:5500/ 에 접속합니다. 종료는 Ctrl+C입니다. VS Code Live Server가 이미 있다면 index.html을 우클릭 → Open with Live Server도 가능합니다. 실제 포트가 다르면 백엔드 CORS의 허용 출처를 맞춰야 합니다. Axios는 CDN을 사용하므로 인터넷 연결이 필요합니다.

백엔드는 별도 터미널에서 실행합니다.

```powershell
.\.venv\Scripts\python.exe team/backend/AppStart.py
```

이미 서버가 있다면 같은 포트로 중복 실행하지 않습니다. 백엔드 또는 회복 모델이 없으면 실제 예측은 동작하지 않고 오류를 안내합니다. 임의 점수나 가짜 R²로 대체하지 않습니다.

## 8개 입력 항목

| 키 | 화면 | 허용 값 |
| --- | --- | --- |
| Age | 나이 | 1 이상 정수 또는 null |
| Gender | 성별 | Male / Female / Non-binary 또는 null |
| Training_Duration_Min | 운동 시간(분) | 필수, 1 이상 정수 |
| Training_Intensity | 운동 강도 | 1~10 실수 또는 null |
| Sleep_Duration_Hours | 수면 시간 | 0~24 실수 또는 null |
| Stress_Level | 스트레스 수준 | Low / Medium / High 또는 null |
| Caffeine_Intake_mg | 카페인 섭취량 | 0 이상 정수 또는 null |
| Muscle_Soreness | 근육통 정도 | 1~10 실수 또는 null |

성별 라벨은 남성·여성·논바이너리, 스트레스 라벨은 낮음·보통·높음이며 원본 CSV의 대소문자를 구분해 전송합니다. 강도 7.5, 근육통 4.5를 정수로 바꾸지 않습니다. 카페인 0은 정상 값이며 빈 값만 null입니다. 모든 초기 입력은 비어 있고 placeholder 또는 미선택 옵션으로 ‘미입력’을 표시합니다. 예시 버튼은 폼만 채웁니다.

실제 CSV의 관측 범위는 나이 18~41, 운동 시간 10~115분, 강도·근육통 1~10, 수면 5~9.5시간, 카페인 0~400mg입니다. 관측 범위를 벗어났지만 논리적으로 가능한 입력은 경고 후 요청을 허용합니다. 음수 등 논리적으로 잘못된 값은 HTML min/max/step과 백엔드 검증으로 차단합니다. 선택 항목 7개 중 4개 이상을 비우면 신뢰도가 낮아질 수 있다고 안내합니다.

미입력을 프론트에서 평균·중앙값으로 바꾸지 않습니다. 백엔드의 학습된 Pipeline이 숫자는 훈련 중앙값, 범주는 훈련 최빈값으로 처리합니다. 세부 학습 방식과 CSV 분석은 ../backend/README.md에 정리했습니다.

## API

app.js 상단에서 서버 주소를 관리합니다.

```javascript
const API_URL = "http://127.0.0.1:8000/api/predict";
```

POST /api/predict, Content-Type: application/json

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

실제 저장 모델의 예시 응답:

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

기본 필드는 predicted_recovery_score와 r2_score입니다. mae·warnings·보정 정보는 반환되면 함께 표시합니다. JSON 숫자만 허용하며 잘못된 응답은 오류로 안내합니다. R²는 음수도 유효하지만 1보다 클 수 없습니다. 칼로리 단위나 이전 입력은 현재 화면·요청에 포함하지 않습니다.

서버는 원본 회귀 예측이 0~100 밖이면 표시 점수만 제한합니다. raw_prediction과 score_was_clipped로 원본값과 보정 여부를 구분하며, 보정된 경우 화면에도 알립니다. R²·MAE는 보정 전 원본 예측으로 평가한 실제 별도 테스트 지표입니다.

예상 운동 회복 점수는 요청 전 — / 100점, 모델 R²는 —로 표시합니다. 요청 중 입력과 버튼을 잠그며 결과를 받은 뒤 입력을 바꾸면 이전 점수를 지웁니다. 예측 결과 안내는 “입력한 운동 및 생활습관 정보를 바탕으로 예측한 회복 점수입니다.”입니다.

## 연결과 확인

백엔드 허용 출처는 http://127.0.0.1:5500 과 http://localhost:5500 입니다. 포트나 호스트가 달라지면 ../backend/AppStart.py의 allow_origins를 변경하세요. 백엔드 주소가 달라지면 API_URL도 맞춥니다. 전체 초기화는 입력·결과·경고를 초기 상태로 되돌립니다.

실제 Chrome에서 확인한 항목:

- 8개 빈 초기값과 — 결과, 필수 운동 시간 검사
- 예시 버튼이 요청하지 않음, 실제 Axios 예측 결과 59.39점·R² 0.6436
- 운동 시간 60분만 입력하면 나머지 7개 null 전송, 실제 결과 47.00점
- 0mg·소수 입력 보존, 중복 요청 방지, 요청 중 잠금
- 입력 변경 시 이전 결과 초기화, 학습 범위 경고, 전체 초기화
- API 요청을 차단했을 때 연결 오류 안내 및 버튼 복구
- 1280·768·390·320px에서 가로 넘침 없는 반응형 배치
- Swagger 실제 API 실행 HTTP 200, 처리되지 않은 JavaScript 예외 없음

숫자는 실제 모델 검증 기록이며 화면에 하드코딩된 기본값이 아닙니다. 배포·다른 PC 환경은 별도 확인이 필요합니다.

본 서비스는 교육용 합성 데이터를 기반으로 한 예측 모델이며, 실제 건강 상태에 대한 의학적 판단을 제공하지 않습니다.

</details>
