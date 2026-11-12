// AppStart.py에서 화면과 API를 같은 주소로 제공합니다.
const API_URL = "/api/predict";

const form = document.getElementById("prediction-form");
const inputFields = document.getElementById("input-fields");
const fieldNames = [
  "Age", "Gender", "Training_Duration_Min", "Training_Intensity",
  "Sleep_Duration_Hours", "Stress_Level", "Caffeine_Intake_mg", "Muscle_Soreness"
];
// 실제 CSV를 확인한 관측 범위입니다. 범위 밖 경고와 잘못된 입력 차단은 구분합니다.
const observedRanges = {
  Age: { label: "나이", min: 18, max: 41 },
  Training_Duration_Min: { label: "운동 시간", min: 10, max: 115 },
  Training_Intensity: { label: "운동 강도", min: 1, max: 10 },
  Sleep_Duration_Hours: { label: "수면 시간", min: 5, max: 9.5 },
  Caffeine_Intake_mg: { label: "카페인 섭취량", min: 0, max: 400 },
  Muscle_Soreness: { label: "근육통 정도", min: 1, max: 10 }
};
const errorMessage = document.getElementById("error-message");
const predictButton = document.getElementById("predict-button");
const exampleButton = document.getElementById("example-button");
const resetButton = document.getElementById("reset-button");
const resultPanel = document.getElementById("result-panel");
const resultBadge = document.getElementById("result-badge");
const resultDescription = document.getElementById("result-description");
let isLoading = false;  // 요청 중이면 true: 예측 버튼의 중복 실행을 막습니다.
let hasResult = false;  // 예측이 완료되면 true: 입력 변경 시 이전 결과를 지웁니다.

// CSV 컬럼명으로 요청 객체를 만듭니다. 숫자 입력은 0과 소수값을 보존합니다.
function getRequestData() {
  const data = {};
  for (const name of fieldNames) {
    const field = document.getElementById(name);
    data[name] = field.type === "number" ? field.valueAsNumber : field.value;
  }
  return data;
}

// CSV 관측 범위 밖은 경고만 표시하고, 논리적 범위는 HTML min/max/step으로 검사합니다.
function updateInputDisplay() {
  const messages = [];
  for (const name in observedRanges) {
    const field = document.getElementById(name);
    const value = field.valueAsNumber;
    const range = observedRanges[name];
    if (field.validity.valid && (value < range.min || value > range.max)) {
      messages.push(`${range.label}의 관측 범위(${range.min}~${range.max})를 벗어났습니다.`);
    }
  }
  const rangeWarning = document.getElementById("range-warning");
  rangeWarning.hidden = messages.length === 0;
  rangeWarning.textContent = messages.join(" ") + " 예측의 신뢰도가 낮아질 수 있습니다.";
}

// 입력 변경 시 이전 예측값을 지워 다른 입력의 결과로 오해하지 않게 합니다.
function clearResult(message = "운동·생활습관 정보를 입력하고 예측을 시작해 보세요.") {
  hasResult = false;
  document.getElementById("recovery-value").textContent = "—";
  document.getElementById("r2-value").textContent = "—";
  document.getElementById("mae-value").textContent = "—";
  document.getElementById("mae-row").hidden = true;
  document.getElementById("recovery-gauge").style.width = "0%";
  document.getElementById("clipping-note").hidden = true;
  document.getElementById("server-warning").hidden = true;
  resultBadge.textContent = "입력 대기";
  resultPanel.dataset.state = "empty";
  resultDescription.textContent = message;
}

function handleInputChange() {
  if (hasResult) {
    clearResult("입력 정보가 변경됐어요. 다시 예측해 주세요.");
  } else {
    clearResult();
  }
  errorMessage.hidden = true;
  updateInputDisplay();
}

// 요청 중 입력과 버튼을 잠가 중복 요청 및 응답과 입력값의 불일치를 막습니다.
function setLoading(loading) {
  isLoading = loading;
  inputFields.disabled = loading;
  predictButton.disabled = loading;
  exampleButton.disabled = loading;
  resetButton.disabled = loading;
  resultPanel.setAttribute("aria-busy", String(loading));
  document.getElementById("button-label").textContent = loading ? "예측 중…" : "회복 점수 예측하기";
  document.getElementById("button-icon").textContent = loading ? "…" : "↗";
  if (loading) {
    resultBadge.textContent = "분석 중";
    resultDescription.textContent = "AI 모델의 응답을 기다리고 있어요.";
  }
}

// 음수 R²도 유효한 평가값입니다. 응답에 없는 값이나 문자열을 숫자로 꾸미지 않습니다.
function isValidResponse(data) {
  if (data === null || typeof data !== "object") {
    return false;
  }
  if (!Number.isFinite(data.predicted_recovery_score)) {
    return false;
  }
  if (data.predicted_recovery_score < 0 || data.predicted_recovery_score > 100) {
    return false;
  }
  if (!Number.isFinite(data.r2_score) || data.r2_score > 1) {
    return false;
  }
  return true;
}

function showResult(data) {
  // textContent는 HTML 태그를 실행하지 않고 글자만 바꿉니다.
  // toLocaleString의 maximumFractionDigits는 화면에서 보여줄 소수 자릿수입니다.
  document.getElementById("recovery-value").textContent = data.predicted_recovery_score.toLocaleString("ko-KR", { maximumFractionDigits: 2 });
  document.getElementById("r2-value").textContent = data.r2_score.toLocaleString("ko-KR", { maximumFractionDigits: 4 });
  // 서버가 반환한 0~100점으로 표시합니다. 클라이언트에서 임의 점수를 만들지 않습니다.
  document.getElementById("recovery-gauge").style.width = `${data.predicted_recovery_score}%`;
  if (data.score_was_clipped === true && Number.isFinite(data.raw_prediction)) {
    const note = document.getElementById("clipping-note");
    note.textContent = `원본 모델 예측값 ${data.raw_prediction.toLocaleString("ko-KR", { maximumFractionDigits: 2 })}점을 표시 범위 0~100점으로 제한했습니다.`;
    note.hidden = false;
  }
  if (Array.isArray(data.warnings)) {
    const messages = [];
    for (const value of data.warnings) {
      if (typeof value === "string") {
        messages.push(value);
      }
    }
    document.getElementById("server-warning").textContent = messages.join(" ");
    document.getElementById("server-warning").hidden = messages.length === 0;
  }
  if (Number.isFinite(data.mae) && data.mae >= 0) {
    document.getElementById("mae-value").textContent = `${data.mae.toLocaleString("ko-KR", { maximumFractionDigits: 2 })}점`;
    document.getElementById("mae-row").hidden = false;
  }
  resultBadge.textContent = "예측 완료";
  resultPanel.dataset.state = "success";
  resultDescription.textContent = "입력한 운동 및 생활습관 정보를 바탕으로 예측한 회복 점수입니다.";
  hasResult = true;
}

// 2. 이벤트: submit은 버튼 클릭과 입력창에서 Enter를 누른 경우를 함께 처리합니다.
// 브라우저 기본 검사(required, min, max, step)를 통과한 경우에만 호출됩니다.
form.addEventListener("submit", async function (event) {
  // 기본 폼 제출로 페이지가 새로고침되지 않게 합니다.
  event.preventDefault();
  if (isLoading) {
    return;
  }
  if (!form.reportValidity()) {
    return;
  }
  const requestData = getRequestData();
  clearResult();
  errorMessage.hidden = true;
  setLoading(true);
  try {
    if (window.location.protocol === "file:") {
      throw new Error("예측 서버를 실행하고 http://127.0.0.1:8000/ 에서 화면을 열어 주세요.");
    }
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestData),
      signal: AbortSignal.timeout(15000)
    });
    const data = await response.json();
    if (!response.ok) {
      const detail = typeof data?.detail === "string"
        ? data.detail
        : "서버가 예측 요청을 처리하지 못했습니다. 입력값을 확인해 주세요.";
      throw new Error(`${detail} (HTTP ${response.status})`);
    }
    if (!isValidResponse(data)) {
      throw new Error("서버 응답에 유효한 예측 점수와 R²가 없습니다.");
    }
    showResult(data);
  } catch (error) {
    clearResult("예측을 완료하지 못했어요. 안내를 확인하고 다시 시도해 주세요.");
    resultBadge.textContent = "예측 실패";
    if (error.name === "TimeoutError" || error.name === "AbortError") {
      errorMessage.textContent = "예측 서버의 응답이 지연되고 있습니다. 잠시 후 다시 시도해 주세요.";
    } else if (error instanceof TypeError) {
      errorMessage.textContent = "예측 서버에 연결할 수 없습니다. FastAPI 서버 실행 상태를 확인해 주세요.";
    } else if (error instanceof SyntaxError) {
      errorMessage.textContent = "예측 서버가 올바른 응답을 반환하지 않았습니다.";
    } else {
      errorMessage.textContent = error.message;
    }
    errorMessage.hidden = false;
  } finally {
    // 성공·실패에 관계없이 버튼과 입력창을 다시 사용할 수 있게 합니다.
    setLoading(false);
  }
});

// 4. 입력·초기화·예시 버튼 이벤트를 연결합니다. 함수명 뒤에 ()를 붙이지 않습니다.
// handleInputChange를 전달하면 입력 이벤트가 발생했을 때 브라우저가 호출합니다.
for (const name of fieldNames) {
  document.getElementById(name).addEventListener("input", handleInputChange);
}

resetButton.addEventListener("click", function () {
  form.reset();
  errorMessage.hidden = true;
  clearResult();
  updateInputDisplay();
});

// 예시 버튼은 폼만 채우며 API 요청은 보내지 않습니다.
exampleButton.addEventListener("click", function () {
  const example = {
    Age: 25, Gender: "Male", Training_Duration_Min: 60, Training_Intensity: 7.5,
    Sleep_Duration_Hours: 7.5, Stress_Level: "Medium", Caffeine_Intake_mg: 150, Muscle_Soreness: 4.5
  };
  for (const name of fieldNames) {
    document.getElementById(name).value = example[name];
  }
  clearResult("예시 입력값을 불러왔어요. 예측 버튼을 눌러 결과를 확인하세요.");
  errorMessage.hidden = true;
  updateInputDisplay();
});

// 모든 입력값은 빈 상태로 시작하며, 예시 버튼도 자동 예측을 실행하지 않습니다.
updateInputDisplay();

async function loadSampleItems() {
  const list = document.getElementById("sample-items");
  try {
    const response = await fetch("/api/items");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const items = await response.json();
    const entries = items.map(({ name, price }) => {
      const entry = document.createElement("li");
      entry.textContent = `${name} ${price.toLocaleString("ko-KR")}원`;
      return entry;
    });
    list.replaceChildren(...entries);
  } catch {
    list.firstElementChild.textContent = "상품 목록을 불러오지 못했습니다.";
  }
}

loadSampleItems();
