from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apis.api_base import api_router
import utils.firebase_init


def include_cors(app):
    # 모든 origin에서 발생하는 요청들을 처리해 줌
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# api에서 라우터를 만들어서 등록한다
def include_router(app) :
    app.include_router(api_router)


def start_application() : 
    app = FastAPI(title="MedEase", version="1.0")
    include_cors(app)
    include_router(app)

    return app 


# 어플리케이션 시작
app =  start_application()
     
@app.on_event("startup")
async def startup_event():
    # Firebase 초기화를 main.py 실행 시 최초 1회 수행
    utils.firebase_init

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down application...")

