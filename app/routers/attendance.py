from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import Attendance
from app.schemas.schemas import AttendanceCreate
from app.services.gps import is_inside_school

from app.core.security import verify_token

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"],
)


@router.post("/mark")
def mark_attendance(
    data: AttendanceCreate,
    token: str,
    db: Session = Depends(get_db),
):

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    teacher_id = payload["teacher_id"]

    inside = is_inside_school(
        data.latitude,
        data.longitude,
    )

    if not inside:
        raise HTTPException(
            status_code=403,
            detail="Outside School Campus",
        )

    already = db.query(Attendance).filter(
        Attendance.teacher_id == teacher_id,
        Attendance.attendance_date == date.today(),
    ).first()

    if already:
        raise HTTPException(
            status_code=400,
            detail="Attendance Already Marked",
        )

    attendance = Attendance(
        teacher_id=teacher_id,
        attendance_date=date.today(),
        check_in=datetime.utcnow(),
        latitude=data.latitude,
        longitude=data.longitude,
        status="Present",
    )

    db.add(attendance)
    db.commit()

    return {
        "message": "Attendance Marked Successfully",
        "teacher_id": teacher_id,
    }