# 파이썬 파일 분리
# AppStart.py       : FastAPI 실행파일
# Controller.py     : HTTP REST 파일
# Service.py        : 로직 파일

# http://127.0.0.1:8000/docs

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn

import Controller

app = FastAPI()
app.include_router(Controller.router)
frontend_dir = Path(__file__).resolve().parent


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(frontend_dir / "index.html")


@app.get("/app.js", include_in_schema=False)
def javascript():
    return FileResponse(frontend_dir / "app.js", media_type="text/javascript")


@app.get("/style.css", include_in_schema=False)
def stylesheet():
    return FileResponse(frontend_dir / "style.css", media_type="text/css")


if __name__ == "__main__":
    uvicorn.run("AppStart:app", host="127.0.0.1", port=8000, reload=True)
