import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)

DATABASE_URL = os.getenv("DATABASE_URL")

SCHOOL_NAME = os.getenv("SCHOOL_NAME")

SCHOOL_LAT = float(os.getenv("SCHOOL_LAT"))

SCHOOL_LON = float(os.getenv("SCHOOL_LON"))

SCHOOL_RADIUS = float(os.getenv("SCHOOL_RADIUS"))