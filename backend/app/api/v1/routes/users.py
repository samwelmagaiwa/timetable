from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db

router = APIRouter()

@router.post("/login")
async def login():
    return {"message": "Login endpoint"}

@router.get("/me")
async def get_me():
    return {"message": "Current user endpoint"}
