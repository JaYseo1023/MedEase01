from google.cloud import firestore


# Firebase 서비스 계정 키 경로
SERVICE_ACCOUNT_PATH = "config_secret/firebase_key.json"

# Firebase 프로젝트 ID 설정
project_id = "medease01-21e2d"  # 자신의 프로젝트 ID로 변경

# Firestore 클라이언트 생성
db = firestore.Client.from_service_account_json(SERVICE_ACCOUNT_PATH)  # JSON 키 파일 경로 설정

# 컬렉션 참조
collection_ref = db.collection("your_collection_name")  # 컬렉션 이름 설정

# 문서 추가
doc_ref = collection_ref.document()
doc_ref.set({"field1": "value1", "field2": "value2"})

# 문서 가져오기
doc = collection_ref.document("document_id").get()
if doc.exists:
    print(f"Document data: {doc.to_dict()}")
else:
    print("No such document!")

# 문서 업데이트
collection_ref.document("document_id").update({"field1": "new_value"})

# 문서 삭제
collection_ref.document("document_id").delete()



