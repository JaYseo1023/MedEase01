from fastapi import APIRouter
from apis.version1 import comm_router
from apis.version1 import survay_router

api_router = APIRouter()

# comm_router의 API를 "/comm" 경로에 포함
api_router.include_router(
    comm_router.router,  # comm_router의 router 객체
    prefix="/comm",  # 모든 경로에 /comm 추가
    tags=["comm"]  # OpenAPI 문서에서 comm 관련 API로 태그
)

# comm_router의 API를 "/comm" 경로에 포함
api_router.include_router(
    survay_router.router,  # comm_router의 router 객체
    prefix="/survay",  # 모든 경로에 /comm 추가
    tags=["survay"]  # OpenAPI 문서에서 comm 관련 API로 태그
)
