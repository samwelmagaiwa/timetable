from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.staff import Staff, StaffCreate, StaffUpdate
from app.services.staff_service import StaffService

router = APIRouter()

@router.get("/", response_model=List[Staff])
async def list_staff(db: Session = Depends(get_db)):
    return StaffService(db).get_all()

@router.post("/", response_model=Staff)
async def create_staff(staff: StaffCreate, db: Session = Depends(get_db)):
    return StaffService(db).create(staff)

@router.get("/{staff_id}", response_model=Staff)
async def get_staff(staff_id: int, db: Session = Depends(get_db)):
    return StaffService(db).get_by_id(staff_id)

@router.put("/{staff_id}", response_model=Staff)
async def update_staff(staff_id: int, staff: StaffUpdate, db: Session = Depends(get_db)):
    return StaffService(db).update(staff_id, staff)

@router.delete("/{staff_id}")
async def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    StaffService(db).delete(staff_id)
    return {"message": "Staff deleted"}
