from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
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


# ===========================
# MARK ATTENDANCE
# ===========================

@router.post("/mark")
async def mark_attendance(
    request: Request,
    data: AttendanceCreate,
    db: Session = Depends(get_db),
):

    auth = request.headers.get("Authorization")

    if auth is None:
        raise HTTPException(
            status_code=401,
            detail="Authorization Header Missing",
        )

    if not auth.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization Header",
        )

    token = auth.replace("Bearer ", "")

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token",
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
        check_in=datetime.utcnow() + timedelta(hours=5, minutes=30),
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


# ===========================
# ATTENDANCE HISTORY
# ===========================

@router.get("/history")
async def attendance_history(
    request: Request,
    db: Session = Depends(get_db),
):

    auth = request.headers.get("Authorization")

    if auth is None:
        raise HTTPException(
            status_code=401,
            detail="Authorization Header Missing",
        )

    if not auth.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization Header",
        )

    token = auth.replace("Bearer ", "")

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token",
        )

    teacher_id = payload["teacher_id"]

    attendance = (
        db.query(Attendance)
        .filter(Attendance.teacher_id == teacher_id)
        .order_by(Attendance.attendance_date.desc())
        .all()
    )

    history = []

    for record in attendance:
        history.append(
            {
                "date": str(record.attendance_date),
                "check_in": (
                    record.check_in.strftime("%I:%M %p")
                    if record.check_in
                    else "-"
                ),
                "status": record.status,
                "latitude": record.latitude,
                "longitude": record.longitude,
            }
        )

    return history