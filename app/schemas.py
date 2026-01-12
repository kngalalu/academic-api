from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime

class UserUpdatePassword(BaseModel):
    password: str

class AcademicInstitutionCreate(BaseModel):
    name: str

class AcademicInstitutionRead(BaseModel):
    id: int
    name: str
    created_at: datetime

class StudentCreate(BaseModel):
    name: str

class StudentRead(BaseModel):
    id: int
    name: str
    enrollment_date: datetime
