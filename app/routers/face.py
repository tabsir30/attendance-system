from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import Teacher
from app.services.face import (
    save_face,
    verify_face,
)

router = APIRouter(
    prefix="/face",
    tags=["Face Recognition"],
)


@router.post("/register")
async def register_face(
    teacher_id: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    teacher = db.query(Teacher).filter(
        Teacher.id == teacher_id
    ).first()

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found",
        )

    image_bytes = await image.read()

    image_path = save_face(image_bytes)

    teacher.face_image = image_path

    db.commit()

    return {
        "message": "Face Registered Successfully",
        "image_path": image_path,
    }


@router.post("/verify")
async def verify_teacher_face(
    teacher_id: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    teacher = db.query(Teacher).filter(
        Teacher.id == teacher_id
    ).first()

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found",
        )

    if teacher.face_image is None:
        raise HTTPException(
            status_code=400,
            detail="Face not registered",
        )

    image_bytes = await image.read()

    result = verify_face(
        teacher.face_image,
        image_bytes,
    )

    return result


@router.get("/")
def test():
    return {
        "message": "Face Router Working"
    }