from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login():
    return {"access_token": "token_example", "token_type": "bearer"}

@router.post("/register")
def register():
    return {"message": "User registered successfully"}
