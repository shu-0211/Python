# [역할] 서버 실행 파일: FastAPI 생성 → CORS 설정 → Controller 연결 → Uvicorn 실행
# 수업 참고: day16/AppStart.py
from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import Controller

# FastAPI 클래스로 HTTP 요청을 받을 서버 객체를 생성합니다.
app = FastAPI(title="Recovery AI", version="2.0.0")

# 별도로 Live Server를 사용할 때도 기존 로컬 주소에서 요청할 수 있습니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

# 2. Controller.py에서 만든 router를 app에 연결합니다.
# Controller의 /api + 함수의 /predict가 합쳐져 /api/predict가 됩니다.
app.include_router(Controller.router)


@app.exception_handler(RequestValidationError)
async def validation_error(request, error):
    # [입력 검증 보완] 아래는 예측 로직이 아니라 잘못된 입력의 응답을 만드는 부분입니다.
    # NaN/Infinity 같은 잘못된 원본 값은 응답에 복사하지 않습니다.
    # 입력 위치와 사유만 반환하여 항상 유효한 JSON으로 안내합니다.
    details = []
    for item in error.errors():
        details.append({
            "loc": item["loc"],
            "msg": item["msg"],
            "type": item["type"],
        })
    return JSONResponse(status_code=422, content={"detail": details})


# API와 Swagger 라우트 뒤에 등록하여 같은 서버에서 HTML과 정적 파일을 제공합니다.
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")


# 3. 이 파일을 직접 실행했을 때만 서버를 시작합니다. import할 때는 실행하지 않습니다.
# AppStart는 파일명, app은 위에서 만든 FastAPI 객체명입니다.
if __name__ == "__main__":
    uvicorn.run("AppStart:app", host="127.0.0.1", port=8000, reload=True)
