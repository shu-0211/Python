# 파이썬 파일 분리
# AppStart.py       : FastAPI 실행파일
# Controller.py     : HTTP REST 파일
# Service.py        : 로직 파일

# http://127.0.0.1:8000/docs

# 1) 서버 실행 
from fastapi import FastAPI 
import uvicorn
app = FastAPI()
if __name__ == "__main__" :
    uvicorn.run( 'AppStart:app' , host='127.0.0.1' , port=8000 , reload=True)


# [2] 컨트롤러에  라우터 연결 
import Controller # import 파일명 
# app.include_router( 라우터 )  # 파일명.변수명
app.include_router(Controller.router)