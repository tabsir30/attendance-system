from geopy.distance import geodesic

from app.core.config import (
    SCHOOL_LAT,
    SCHOOL_LON,
    SCHOOL_RADIUS,
)


def is_inside_school(latitude: float, longitude: float):

    school_location = (
        SCHOOL_LAT,
        SCHOOL_LON,
    )

    teacher_location = (
        latitude,
        longitude,
    )

    distance = geodesic(
        school_location,
        teacher_location,
    ).meters

    return distance <= SCHOOL_RADIUS