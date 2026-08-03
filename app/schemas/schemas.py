from pydantic import BaseModel, EmailStr


class TeacherCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    department: str


class TeacherLogin(BaseModel):
    email: EmailStr
    password: str


class AttendanceCreate(BaseModel):
    latitude: float
    longitude: float


class Token(BaseModel):
    access_token: str
    token_type: str