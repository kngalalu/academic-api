from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import List, Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AcademicInstitution(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # 1 institution → many students
    students: List["Student"] = Relationship(back_populates="institution")


class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    enrollment_date: datetime = Field(default_factory=datetime.utcnow)

    institution_id: int = Field(foreign_key="academicinstitution.id")
    institution: Optional[AcademicInstitution] = Relationship(back_populates="students")

Student.institution = Relationship(back_populates="students")
