from geopy.distance import geodesic

# Your School Coordinates
SCHOOL_LAT = 22.573052
SCHOOL_LON = 88.435632

# Allowed distance in meters
RADIUS = 100


def is_inside_school(latitude, longitude):
    school = (SCHOOL_LAT, SCHOOL_LON)
    teacher = (latitude, longitude)

    distance = geodesic(school, teacher).meters

    print(f"Distance from school: {distance:.2f} meters")

    return distance <= RADIUS