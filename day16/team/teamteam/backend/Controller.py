# [역할] HTTP 요청 처리 파일: JSON 입력 검증 → Service 호출 → JSON 응답
# 수업 참고: day16/Controller.py의 APIRouter, 서비스 객체 import와 메서드 호출
import logging
from typing import Literal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from Service import recovery_service

# 이 라우터에 등록하는 함수들의 공통 주소입니다.
router = APIRouter(prefix="/api")
logger = logging.getLogger(__name__)


class PredictRequest(BaseModel):
    # [입력 검증 보완] 수업의 dict 입력에 자료형과 범위 검사를 추가한 부분입니다.
    # int: 정수 / float: 실수 / Literal: 정해진 문자열만 허용
    # 숫자 문자열과 bool의 자동 숫자 변환을 막고, 알 수 없는 필드도 검사합니다.
    model_config = ConfigDict(
        strict=True, extra="forbid", allow_inf_nan=False,
        # Swagger에도 프론트엔드의 예시 입력과 같은 JSON을 제공합니다.
        json_schema_extra={"example": {
            "Age": 25, "Gender": "Male", "Training_Duration_Min": 60,
            "Training_Intensity": 7.5, "Sleep_Duration_Hours": 7.5,
            "Stress_Level": "Medium", "Caffeine_Intake_mg": 150, "Muscle_Soreness": 4.5,
        }},
    )

    # 학습 모델에 결측값 대체가 없으므로 8개 값을 모두 받습니다.
    Age: int = Field(ge=1)
    Gender: Literal["Male", "Female"]
    Training_Duration_Min: int = Field(ge=1)
    Training_Intensity: float = Field(ge=1, le=10)
    Sleep_Duration_Hours: float = Field(ge=0, le=24)
    Stress_Level: Literal["Low", "Medium", "High"]
    Caffeine_Intake_mg: int = Field(ge=0)
    Muscle_Soreness: float = Field(ge=1, le=10)


@router.post("/predict")
def predict(data: PredictRequest):
    # 1. 요청: POST /api/predict의 JSON이 검증된 data 객체에 담깁니다.
    # 2. 변환: model_dump()는 Pydantic 객체를 일반 딕셔너리로 바꿉니다.
    # 3. 호출: 수업의 item_service.save(item)처럼 서비스 객체의 메서드를 호출합니다.
    # 4. 반환: 서비스가 반환한 딕셔너리를 FastAPI가 JSON으로 응답합니다.
    # 모델 예측은 동기 작업이므로 def를 사용합니다. FastAPI 작업 스레드에서 실행됩니다.
    try:
        request_data = data.model_dump()
        result = recovery_service.predict(request_data)
        return result
    # [오류 응답 보완] 예측 실패를 구분하고 내부 경로는 서버 로그에만 남깁니다.
    except FileNotFoundError:
        logger.exception("회복 점수 모델 또는 평가용 CSV 파일이 없습니다.")
        raise HTTPException(
            status_code=503,
            detail="회복 점수 모델을 준비하지 못했습니다. day16/model.pkl과 평가용 CSV 파일을 확인해 주세요.",
        ) from None
    except ArithmeticError:
        logger.exception("현재 입력 조합에서 유한한 회복 점수를 얻지 못했습니다.")
        raise HTTPException(
            status_code=422,
            detail="현재 입력 조합에서 유효한 회복 점수를 예측할 수 없습니다. 입력값을 확인해 주세요.",
        ) from None
    except ValueError:
        logger.exception("모델 컬럼, 성능 지표 또는 예측 입력 형식이 일치하지 않습니다.")
        raise HTTPException(
            status_code=500,
            detail="모델 입력 컬럼 또는 모델 설정을 확인해 주세요. 자세한 원인은 서버 로그를 확인해 주세요.",
        ) from None
    except Exception:
        logger.exception("회복 점수 모델 로드 또는 예측 중 오류가 발생했습니다.")
        raise HTTPException(
            status_code=500,
            detail="모델 예측 중 서버 오류가 발생했습니다. 서버 로그를 확인해 주세요.",
        ) from None
