from utils.firebase_init import db
from schemas.comm_sch import Item
from fastapi import HTTPException

def create_item(item: Item):
    """Item 데이터를 Firestore에 저장."""
    doc_ref = db.collection("items").document()  # 새 문서 생성
    doc_ref.set(item.model_dump())  # Pydantic 모델 데이터를 Firestore에 저장
    return {"id": doc_ref.id, **item.model_dump()}  # 저장된 문서의 ID와 데이터 반환


def read_item(item_id: str):
    doc_ref = db.collection("items").document(item_id)
    doc = doc_ref.get()
    if doc.exists:
        return {**doc.to_dict(), "id":doc.id}
    else:
        raise HTTPException(status_code=404, detail="item not found")
    
def update_item(item_id: str, item: Item):
    doc_ref = db.collection("items").document(item_id)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.set(item.model_dump())
        return {"id":doc.id, **item.model_dump()}
    else:
        raise HTTPException(status_code=404, detail="item not found")
    
def delete_item(item_id: str):
    doc_ref = db.collection("items").document(item_id)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.delete()
        return {"message": "Item deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="item not found")
    
def read_all_items():
    items = []
    docs = db.collection("items").stream()
    for doc in docs:
        items.append({**doc.to_dict(), "id":doc.id})
    return items

def read_items_by_name(name: str):
    items = []
    docs = db.collection("items").where("name", "==", name).stream()
    for doc in docs:
        items.append({**doc.to_dict(), "id": doc.id})
    
    if not items:
        raise HTTPException(status_code=404, detail="No items found with the specified name")
    
    return items
