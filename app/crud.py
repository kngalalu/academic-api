from sqlmodel import Session, select
from app.models import User, AcademicInstitution, Student
from app.security import get_password_hash

# Users
def create_user(session: Session, email: str, password: str):
    user = User(email=email, hashed_password=get_password_hash(password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_users(session: Session):
    return session.exec(select(User)).all()

# Academic Institutions
def create_institution(session: Session, name: str):
    inst = AcademicInstitution(name=name)
    session.add(inst)
    session.commit()
    session.refresh(inst)
    return inst

def get_institutions(session: Session):
    return session.exec(select(AcademicInstitution)).all()

# Students
def create_student(session: Session, name: str, institution_id: int):
    student = Student(name=name, institution_id=institution_id)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

def get_students_for_institution(session: Session, institution_id: int):
    return session.exec(select(Student).where(Student.institution_id == institution_id)).all()
