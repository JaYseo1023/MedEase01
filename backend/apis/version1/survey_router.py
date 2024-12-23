from fastapi import APIRouter

router = APIRouter()

@router.post("/create_user")
async def create_user(username: str, email: str):
    return {"message": f"User {username} created!"}