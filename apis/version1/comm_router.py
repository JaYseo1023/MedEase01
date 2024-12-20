from fastapi import APIRouter
from utils.firebase_crud import create_item, read_item, update_item, delete_item, read_all_items, read_items_by_name
from schemas.comm_sch import Item
from typing import List

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "드디어! 시작해보자!"}


@router.post("/items/")
async def create_item_endpoint(item: Item):
    """
    POST 요청을 받아 Firestore에 Item 데이터를 저장.
    """
    try:
        result = create_item(item)
        return result
    except Exception as e:
        return {"error": str(e)}
    
@router.get("items/{item_id}/")
async def read_item_endpoint(item_id: str):
    """
    특정 ID를 가진 아이템을 Firestore에서 조회
    """
    try:
        return read_item(item_id)
    except Exception as e:
        return {"error": str(e)}

@router.put("/items/{item_id}")
async def update_item_endpoint(item_id: str, item: Item):
    """
    특정 ID를 가진 아이템 데이터를 업데이트.
    """
    try:
        return update_item(item_id, item)
    except Exception as e:
        return {"error": str(e)}


@router.delete("/items/{item_id}")
async def delete_item_endpoint(item_id: str):
    """
    특정 ID를 가진 아이템 데이터를 삭제.
    """
    try:
        return delete_item(item_id)
    except Exception as e:
        return {"error": str(e)}


@router.get("/items/")
async def read_all_items_endpoint() -> List[dict]:
    """
    모든 아이템 데이터를 가져옵니다.
    """
    try:
        return read_all_items()
    except Exception as e:
        return {"error": str(e)}

@router.get("/items/by-name/{name}")
async def get_items_by_name(name: str):
    """
    특정 name 값을 가진 문서들을 조회.

    Args:
        name (str): 조회할 name 값

    Returns:
        list: 일치하는 문서들의 데이터 리스트
    """
    try:
        return read_items_by_name(name)
    except Exception as e:
        return {"error": str(e)}
