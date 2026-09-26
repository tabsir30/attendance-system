from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.hackathon_models import (
    HackStudent,
    HackSession,
    HackAttendance,
)


router = APIRouter(
    prefix="/hack",
    tags=["Hackathon"],
)


# ============================================================
# SCHOOL LOCATION
# ============================================================

# IMPORTANT:
# Replace these with your actual college coordinates.

SCHOOL_LAT = 22.573051
SCHOOL_LON = 88.435630
SCHOOL_RADIUS = 100
# Allowed attendance radius in meters



# ============================================================
# DISTANCE CALCULATION
# ============================================================

def distance_meters(
    lat1,
    lon1,
    lat2,
    lon2,
):
    earth_radius = 6371000

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        +
        cos(radians(lat1))
        *
        cos(radians(lat2))
        *
        sin(dlon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a),
    )

    return earth_radius * c


def inside_school(
    latitude,
    longitude,
):
    distance = distance_meters(
        latitude,
        longitude,
        SCHOOL_LAT,
        SCHOOL_LON,
    )

    return (
        distance <= SCHOOL_RADIUS,
        distance,
    )


# ============================================================
# STUDENT REGISTER
# ============================================================

@router.post("/student/register")
def register_student(
    name: str,
    roll_number: str,
    email: str,
    password: str,
    department: str = "CSE",
    semester: str = "4",
    section: str = "B",
    db: Session = Depends(get_db),
):

    existing = (
        db.query(HackStudent)
        .filter(
            HackStudent.email == email
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Student already exists",
        )

    existing_roll = (
        db.query(HackStudent)
        .filter(
            HackStudent.roll_number
            == roll_number
        )
        .first()
    )

    if existing_roll:
        raise HTTPException(
            status_code=400,
            detail="Roll number already exists",
        )

    student = HackStudent(
        name=name,
        roll_number=roll_number,
        email=email,
        password=password,
        department=department,
        semester=semester,
        section=section,
    )

    db.add(student)

    db.commit()

    db.refresh(student)

    return {
        "message": "Student registered successfully",
        "student_id": student.id,
        "name": student.name,
        "roll_number": student.roll_number,
    }


# ============================================================
# STUDENT LOGIN
# ============================================================

@router.post("/student/login")
def student_login(
    email: str,
    password: str,
    db: Session = Depends(get_db),
):

    student = (
        db.query(HackStudent)
        .filter(
            HackStudent.email == email
        )
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    if student.password != password:
        raise HTTPException(
            status_code=401,
            detail="Invalid password",
        )

    return {
        "message": "Student login successful",
        "student": {
            "id": student.id,
            "name": student.name,
            "roll_number": student.roll_number,
            "email": student.email,
            "department": student.department,
            "semester": student.semester,
            "section": student.section,
        },
    }


# ============================================================
# START CLASS SESSION
# ============================================================

@router.post("/session/start")
def start_session(
    teacher_id: int,
    subject: str,
    class_name: str,
    duration_minutes: int = 60,
    db: Session = Depends(get_db),
):

    teacher_exists = db.execute(
        __import__("sqlalchemy")
        .select(
            __import__(
                "app.models.models",
                fromlist=["Teacher"],
            ).Teacher
        )
        .where(
            __import__(
                "app.models.models",
                fromlist=["Teacher"],
            ).Teacher.id
            == teacher_id
        )
    ).scalar_one_or_none()

    if teacher_exists is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found",
        )

    now = datetime.utcnow()

    session = HackSession(
        teacher_id=teacher_id,
        subject=subject,
        class_name=class_name,
        start_time=now,
        expires_at=now
        + timedelta(
            minutes=duration_minutes
        ),
        active=True,
    )

    session.current_qr = str(uuid4())

    session.qr_expires_at = (
        now + timedelta(seconds=10)
    )

    db.add(session)

    db.commit()

    db.refresh(session)

    return {
        "message": "Attendance session started",
        "session_id": session.id,
        "subject": session.subject,
        "class_name": session.class_name,
        "qr": session.current_qr,
        "expires_at": session.expires_at,
        "qr_expires_at":
            session.qr_expires_at,
    }


# ============================================================
# REFRESH DYNAMIC QR
# ============================================================

@router.get(
    "/session/{session_id}/qr"
)
def get_qr(
    session_id: int,
    db: Session = Depends(get_db),
):

    session = (
        db.query(HackSession)
        .filter(
            HackSession.id == session_id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    now = datetime.utcnow()

    if not session.active:
        raise HTTPException(
            status_code=400,
            detail="Session is closed",
        )

    if now >= session.expires_at:

        session.active = False
        session.end_time = now

        db.commit()

        raise HTTPException(
            status_code=400,
            detail="Session expired",
        )

    # Generate a completely new QR
    session.current_qr = str(uuid4())

    session.qr_expires_at = (
        now + timedelta(seconds=10)
    )

    db.commit()

    return {
        "session_id": session.id,
        "qr": session.current_qr,
        "expires_in": 10,
    }


# ============================================================
# STOP SESSION
# ============================================================

@router.post(
    "/session/{session_id}/stop"
)
def stop_session(
    session_id: int,
    db: Session = Depends(get_db),
):

    session = (
        db.query(HackSession)
        .filter(
            HackSession.id == session_id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    session.active = False

    session.end_time = datetime.utcnow()

    db.commit()

    return {
        "message":
            "Attendance session closed"
    }


# ============================================================
# MARK STUDENT ATTENDANCE
# ============================================================

@router.post("/attendance/mark")
def mark_hack_attendance(
    student_id: int,
    session_id: int,
    qr: str,
    latitude: float,
    longitude: float,
    db: Session = Depends(get_db),
):

    student = (
        db.query(HackStudent)
        .filter(
            HackStudent.id == student_id
        )
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    session = (
        db.query(HackSession)
        .filter(
            HackSession.id == session_id
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    now = datetime.utcnow()

    # Session active?
    if not session.active:
        raise HTTPException(
            status_code=400,
            detail="Attendance session is closed",
        )

    # Session expired?
    if now >= session.expires_at:

        session.active = False

        db.commit()

        raise HTTPException(
            status_code=400,
            detail="Attendance session expired",
        )

    # QR correct?
    if qr != session.current_qr:
        raise HTTPException(
            status_code=400,
            detail="QR expired or invalid",
        )

    # QR still valid?
    if (
        session.qr_expires_at
        and now > session.qr_expires_at
    ):
        raise HTTPException(
            status_code=400,
            detail="QR expired. Scan the latest QR.",
        )

    # ========================================================
    # GPS CHECK
    # ========================================================

    inside, distance = inside_school(
        latitude,
        longitude,
    )

    if not inside:

        raise HTTPException(
            status_code=403,
            detail=(
                f"Attendance blocked. "
                f"You are "
                f"{distance:.0f}m away. "
                f"Allowed radius is "
                f"{SCHOOL_RADIUS}m."
            ),
        )

    # ========================================================
    # DUPLICATE CHECK
    # ========================================================

    existing = (
        db.query(HackAttendance)
        .filter(
            HackAttendance.session_id
            == session_id,
            HackAttendance.student_id
            == student_id,
        )
        .first()
    )

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Attendance already marked",
        )

    # ========================================================
    # SAVE ATTENDANCE
    # ========================================================

    attendance = HackAttendance(
        session_id=session_id,
        student_id=student_id,
        latitude=latitude,
        longitude=longitude,
        status="Present",
    )

    db.add(attendance)

    db.commit()

    db.refresh(attendance)

    return {
        "message":
            "Attendance marked successfully",
        "status": "Present",
        "subject": session.subject,
        "check_in":
            attendance.check_in,
    }


# ============================================================
# STUDENT ATTENDANCE PERCENTAGE
# ============================================================

@router.get(
    "/student/{student_id}/attendance"
)
def student_attendance(
    student_id: int,
    db: Session = Depends(get_db),
):

    sessions = (
        db.query(HackSession)
        .filter(
            HackSession.active == False
        )
        .all()
    )

    result = {}

    for session in sessions:

        subject = session.subject

        if subject not in result:

            result[subject] = {
                "conducted": 0,
                "attended": 0,
            }

        result[subject]["conducted"] += 1

        present = (
            db.query(HackAttendance)
            .filter(
                HackAttendance.session_id
                == session.id,

                HackAttendance.student_id
                == student_id,
            )
            .first()
        )

        if present:

            result[subject]["attended"] += 1

    output = []

    for subject, data in result.items():

        conducted = data["conducted"]

        attended = data["attended"]

        percentage = (
            attended
            / conducted
            * 100
            if conducted > 0
            else 0
        )

        output.append({
            "subject": subject,
            "conducted": conducted,
            "attended": attended,
            "percentage":
                round(
                    percentage,
                    2,
                ),
            "low_attendance":
                percentage < 75,
        })

    return output


# ============================================================
# SESSION ATTENDANCE
# ============================================================

@router.get(
    "/session/{session_id}/attendance"
)
def session_attendance(
    session_id: int,
    db: Session = Depends(get_db),
):

    records = (
        db.query(
            HackAttendance,
            HackStudent,
        )
        .join(
            HackStudent,
            HackStudent.id
            == HackAttendance.student_id,
        )
        .filter(
            HackAttendance.session_id
            == session_id
        )
        .all()
    )

    result = []

    for attendance, student in records:

        result.append({
            "student_id":
                student.id,

            "name":
                student.name,

            "roll_number":
                student.roll_number,

            "status":
                attendance.status,

            "check_in":
                attendance.check_in,
        })

    return result