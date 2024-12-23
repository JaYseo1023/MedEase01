from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apis.api_base import api_router
import utils.firebase_init
from utils.survey_save import load_and_save_survey_grouped

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
def include_router(app):
    app.include_router(api_router)

def start_application():
    # Firebase 초기화 main.py 실행 시 최초 1회 수행
    utils.firebase_init
    # 엑셀 파일 가져와서 설문 db에 저장
    GITHUB_EXCEL_URL = "https://raw.githubusercontent.com/JaYseo1023/MedEase01/main/survey.xlsx"
    result = load_and_save_survey_grouped(GITHUB_EXCEL_URL)
    print(result)

    app = FastAPI(title="MedEase", version="1.0")
    include_cors(app)
    include_router(app)

    return app

# 어플리케이션 시작
app = start_application()

# 앱 종료 시 추가적인 작업이 필요한 경우 아래와 같이 처리 가능
import atexit

def shutdown_event():
    print("Shutting down application...")

atexit.register(shutdown_event)
