from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import Teacher
from app.schemas.schemas import TeacherCreate, TeacherLogin
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(user: TeacherCreate, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(
        Teacher.email == user.email
    ).first()

    if teacher:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    new_teacher = Teacher(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        department=user.department,
    )

    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    return {"message": "Teacher Registered Successfully"}


@router.post("/login")
def login(user: TeacherLogin, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(
        Teacher.email == user.email
    ).first()

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found",
        )

    if not verify_password(user.password, teacher.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid Password",
        )

    token = create_access_token(
        {
            "teacher_id": teacher.id,
            "email": teacher.email,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "teacher": {
            "id": teacher.id,
            "name": teacher.name,
            "email": teacher.email,
            "department": teacher.department,
        },
    }