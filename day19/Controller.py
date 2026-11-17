from fastapi import APIRouter
router = APIRouter(prefix="/api")

from Service import model_service


# 자바서버에서 받은 값을 서비스 모델에 넘김
@router.post("/check")
async def check( paramete : dict) : 
    return model_service.check(paramete)