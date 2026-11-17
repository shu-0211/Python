import json 
from fastapi.responses import StreamingResponse
from fastapi import APIRouter
router = APIRouter(prefix="/api")

from Service import model_service


# 자바서버에서 받은 값을 서비스 모델에 넘김
@router.post("/check")
async def check( paramete : dict) :
    def generate() : 
        result = model_service.check(paramete)
        # SSE
        data = json.dumps({"result" : result } , ensure_ascii=False)
        yield f"data : {data}\n\n"



    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
    )


