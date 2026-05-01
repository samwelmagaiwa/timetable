from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db

def get_current_user():
    pass

def get_current_active_user():
    pass
