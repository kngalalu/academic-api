from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.crud import create_institution, get_institutions, create_student, get_students_for_institution
from app.deps import get_session, get_current_user
from app.schemas import AcademicInstitutionCreate, AcademicInstitutionRead, StudentCreate, StudentRead
from app.models import AcademicInstitution, Student, User

# All academic routes live under /academic_institutions
router = APIRouter(prefix="/academic_institutions", tags=["academic"])

@router.post("",response_model=AcademicInstitutionRead)
def create_inst(inst: AcademicInstitutionCreate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    # Creating institutions is restricted to authenticated users
    # The actual DB insert logic is handled in the CRUD layer
    return create_institution(session, inst.name)

@router.get("", response_model=list[AcademicInstitutionRead])
def get_insts(session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    # Simple listing endpoint used by clients to fetch all institutions
    return get_institutions(session)

@router.post("/{institution_id}/students", response_model=StudentRead)
def create_stud(institution_id: int, student: StudentCreate, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    # Students are always created in the context of an institution
    return create_student(session, student.name, institution_id)

@router.get("/{institution_id}/students", response_model=list[StudentRead])
def get_studs(institution_id: int, session: Session = Depends(get_session), current_user=Depends(get_current_user)):
    # Returns all students that belong to a specific institution
    return get_students_for_institution(session, institution_id)

@router.get("/{institution_id}/students/{student_id}", response_model=StudentRead)
def get_student_for_institution(
    institution_id: int,
    student_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    # Check institution exists
    institution = session.get(AcademicInstitution, institution_id)
    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")

    # Fetch the student only if it belongs to this institution
    student = session.exec(
        select(Student)
        .where(Student.id == student_id)
        .where(Student.institution_id == institution_id)
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student
