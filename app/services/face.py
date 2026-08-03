import os
import uuid

from deepface import DeepFace


UPLOAD_FOLDER = "uploads/faces"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def save_face(image_bytes: bytes):

    filename = f"{uuid.uuid4()}.jpg"

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename,
    )

    with open(filepath, "wb") as file:
        file.write(image_bytes)

    return filepath


def verify_face(
    registered_image: str,
    uploaded_image: bytes,
):

    temp_image = os.path.join(
        UPLOAD_FOLDER,
        "temp_verify.jpg"
    )

    with open(temp_image, "wb") as file:
        file.write(uploaded_image)

    try:

        result = DeepFace.verify(
            img1_path=registered_image,
            img2_path=temp_image,
            model_name="Facenet512",
            detector_backend="retinaface",
            enforce_detection=True,
        )

        return {
            "matched": bool(result["verified"]),
            "distance": float(result["distance"]),
            "threshold": float(result["threshold"]),
        }

    finally:

        if os.path.exists(temp_image):
            os.remove(temp_image)