# 1. import 
import uvicorn
from fastapi import FastAPI

# 2. fastapi 객체 
app = FastAPI()

# 3. 서버실행 함수 
if __name__ == "__main__":
    uvicorn.run("f-02:app" ,host="127.0.0.1" , port=8000 , reload=True)

# 4. 서버 실행 : 현재 파일 py 실행 # 여러번 실행 불가 
# 5. REST : 자원 주고 받는 상태 구조 , Rest API : HTTP으로 REST 구현한 것
# 1) FastAPI 객체 내 get/post/put/delete 메소드 지원 
@app.get("/")   # @app.get("/매핑주소")
async def index() : #async def 함수명 () : 비동기 함수 선언
    return "안녕 파이썬 웹" # 반환값 

# 코드 작성 후 서버 재실행 없이 "reload=True" 속성으로 자동 서버 반영
# 2) 쿼리스트링 : HTTP URL 경로 상에 ? 뒤로 정의된 변수들 
@app.get("/user")
async def user(name , age:int)  :
    info = { 'name' : name , 'age' : age , 'msg' : '*쿼리 통신 성공'}
    return info # 딕셔너리가 JSON 타입으로 자동변환
# http://127.0.0.1:8000/docs 또는 TalendAPI 테스트 진행

# 3) 경로파라미터 : HTTP URL 경로 상에 / 구분하여 변수들
@app.get("/item/{name}/{age}")   # /item/유재석/40 -> /item/{변수명}/{변수명}
async def item( name : str , age : int | None = None) :
    return { name : name , age : age , 'msg' : "*경로통신성공"}

# 4) 본문 , HTTP GET / DELETE => 쿼리 / 경로 , HTTP POST/PUT => 쿼리/경로/본문BODY
@app.post("/product")
async def product( product : dict) :  # 전달 받은 body본문(json) 값을 파이선 dict 타입으로 매핑 
    product['msg'] = "*본문통신성공*"
    return product
# 요청/테스트 에서 body(본문)에 {"name" : "유재석" , "age" : 40 } 으로 보내보기 