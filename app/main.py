from fastapi import FastAPI

from app.database.database import Base, engine

# Import routers
from app.routers.auth import router as auth_router
from app.routers.attendance import router as attendance_router
from app.routers.face import router as face_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="School Attendance API",
    version="1.0.0",
)

# Include all routers
app.include_router(auth_router)
app.include_router(attendance_router)
app.include_router(face_router)

# Home route
@app.get("/")
def home():
    return {
        "message": "School Attendance API Running"
    }