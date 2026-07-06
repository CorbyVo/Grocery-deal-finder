from geopy.distance import geodesic

def calculate_distance_km(user_latitude, user_longitude, store_latitude, store_longitude):
    """
        Calculate distance in kilometers between user and store coordinates.
    """
    return geodesic((user_latitude, user_longitude ), (store_latitude, store_longitude)).km