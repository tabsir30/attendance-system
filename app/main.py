from fastapi import FastAPI

from app.database.database import Base, engine

# ============================================================
# EXISTING MODELS
# ============================================================

from app.models.models import Teacher, Attendance

# ============================================================
# HACKATHON MODELS
# ============================================================

from app.models.hackathon_models import (
    HackStudent,
    HackSession,
    HackAttendance,
)

# ============================================================
# EXISTING ROUTERS
# ============================================================

from app.routers.auth import router as auth_router
from app.routers.attendance import router as attendance_router
from app.routers.face import router as face_router

# ============================================================
# HACKATHON ROUTER
# ============================================================

from app.routers.hackathon import router as hackathon_router


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="ATTENZO - Smart Classroom Attendance API",
    version="2.0.0",
)


# ============================================================
# EXISTING ATTENZO ROUTERS
# ============================================================

app.include_router(auth_router)

app.include_router(attendance_router)

app.include_router(face_router)


# ============================================================
# HACKATHON ROUTER
# ============================================================

app.include_router(hackathon_router)


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return {
        "message": "ATTENZO Smart Classroom Attendance API Running",
        "version": "2.0.0",
    }