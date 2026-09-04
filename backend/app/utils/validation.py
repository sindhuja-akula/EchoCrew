import math
from pathlib import Path
from typing import Tuple

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

def validate_coordinates(latitude: float, longitude: float) -> Tuple[bool, str]:
    """
    Validates WGS 84 geographic coordinates.
    Latitude range: [-90.0, 90.0]
    Longitude range: [-180.0, 180.0]
    """
    if latitude is None or longitude is None:
        return False, "Latitude and longitude must not be null."
    
    if not (-90.0 <= latitude <= 90.0):
        return False, f"Invalid latitude: {latitude}. Must be between -90 and 90 degrees."
    
    if not (-180.0 <= longitude <= 180.0):
        return False, f"Invalid longitude: {longitude}. Must be between -180 and 180 degrees."
    
    return True, "Valid coordinates"

def validate_image_filename(filename: str) -> Tuple[bool, str]:
    """Validates image file extension against allowed types."""
    if not filename:
        return False, "Filename cannot be empty."
    
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return False, f"Unsupported file format '{ext}'. Allowed formats: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
    
    return True, "Valid image extension"

def haversine_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculates surface distance in meters between two lat/lon points on Earth.
    Used for 20-meter spatial deduplication checks.
    """
    R = 6371000.0  # Earth's mean radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c
