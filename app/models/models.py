from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime, date

from app.database.database import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    password = Column(String, nullable=False)

    department = Column(String)

    # Path of the registered face image
    face_image = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    attendance = relationship(
        "Attendance",
        back_populates="teacher"
    )


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)

    teacher_id = Column(
        Integer,
        ForeignKey("teachers.id")
    )

    attendance_date = Column(
        Date,
        default=date.today
    )

    check_in = Column(
        DateTime,
        default=datetime.utcnow
    )

    check_out = Column(
        DateTime,
        nullable=True
    )

    latitude = Column(Float)

    longitude = Column(Float)

    status = Column(String)

    teacher = relationship(
        "Teacher",
        back_populates="attendance"
    )