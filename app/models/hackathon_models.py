from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean

from app.database.database import Base


class HackStudent(Base):
    __tablename__ = "hack_students"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    roll_number = Column(
        String,
        unique=True,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )

    department = Column(
        String,
        default="CSE"
    )

    semester = Column(
        String,
        default="4"
    )

    section = Column(
        String,
        default="B"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class HackSession(Base):
    __tablename__ = "hack_sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    teacher_id = Column(
        Integer,
        ForeignKey("teachers.id"),
        nullable=False
    )

    subject = Column(
        String,
        nullable=False
    )

    class_name = Column(
        String,
        nullable=False
    )

    start_time = Column(
        DateTime,
        default=datetime.utcnow
    )

    end_time = Column(
        DateTime,
        nullable=True
    )

    expires_at = Column(
        DateTime,
        nullable=False
    )

    active = Column(
        Boolean,
        default=True
    )

    current_qr = Column(
        String,
        nullable=True
    )

    qr_expires_at = Column(
        DateTime,
        nullable=True
    )


class HackAttendance(Base):
    __tablename__ = "hack_attendance"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    session_id = Column(
        Integer,
        ForeignKey("hack_sessions.id"),
        nullable=False
    )

    student_id = Column(
        Integer,
        ForeignKey("hack_students.id"),
        nullable=False
    )

    latitude = Column(Float)

    longitude = Column(Float)

    check_in = Column(
        DateTime,
        default=datetime.utcnow
    )

    status = Column(
        String,
        default="Present"
    )