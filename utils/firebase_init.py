import firebase_admin
from firebase_admin import credentials, db

# Firebase 서비스 계정 키 경로
SERVICE_ACCOUNT_PATH = "config_secret/firebase_key.json"

# Firebase 초기화
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://<your-database-name>.firebaseio.com"  # Firebase DB URL
})

# Firebase 데이터베이스 참조 반환 함수
def get_db_reference(path: str):
    """Returns a Firebase Database reference for the given path."""
    return db.reference(path)
