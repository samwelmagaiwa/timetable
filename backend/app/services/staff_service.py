from sqlalchemy.orm import Session
from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffUpdate

class StaffService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        return self.db.query(Staff).all()
    
    def get_by_id(self, staff_id: int):
        return self.db.query(Staff).filter(Staff.id == staff_id).first()
    
    def create(self, staff: StaffCreate):
        db_staff = Staff(**staff.model_dump())
        self.db.add(db_staff)
        self.db.commit()
        self.db.refresh(db_staff)
        return db_staff
    
    def update(self, staff_id: int, staff: StaffUpdate):
        db_staff = self.get_by_id(staff_id)
        for key, value in staff.model_dump(exclude_unset=True).items():
            setattr(db_staff, key, value)
        self.db.commit()
        self.db.refresh(db_staff)
        return db_staff
    
    def delete(self, staff_id: int):
        db_staff = self.get_by_id(staff_id)
        self.db.delete(db_staff)
        self.db.commit()
