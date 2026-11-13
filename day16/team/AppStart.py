# 파이썬 파일 분리
# AppStart.py : Fast API 실행 파일
# Controller.py: HTTTP REST 파일
# Service.py : 로직 파일
from fastapi import FastAPI
import uvicorn

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("AppStart:app",host="127.0.0.1", port=8001,reload= True)

#[2] 컨트롤러에 라우터 연결
import Controller # import 파일명
# app.include_router(라우터)
app.include_router(Controller.router)

#[3] 테스트 화면(index.html) 제공 + CORS 허용 (html 파일을 직접 열어도 요청 가능)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/", include_in_schema=False)
def index():
    return FileResponse(Path(__file__).parent / "index.html")

# http://127.0.0.1:8001/  -> 테스트 화면

# http://127.0.0.1:8001/docs