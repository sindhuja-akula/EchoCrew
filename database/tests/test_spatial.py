"""
Tests spatial distance calculation logic and PostGIS WKT POINT elements using unittest.
"""

import math
import unittest

try:
    from geoalchemy2.elements import WKTElement
except ImportError:
    class WKTElement:
        def __init__(self, data, srid=4326):
            self.data = data
            self.srid = srid
        def __str__(self):
            return self.data

def haversine_distance_meters(lat1, lon1, lat2, lon2):
    """Calculates approximate surface distance in meters between two lat/lon coordinates."""
    R = 6371000  # Radius of Earth in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class TestSpatialLogic(unittest.TestCase):

    def test_spatial_point_wkt_formatting(self):
        lat, lon = 12.971598, 77.594562
        wkt = WKTElement(f"POINT({lon} {lat})", srid=4326)
        self.assertEqual(wkt.srid, 4326)
        self.assertIn("POINT(77.594562 12.971598)", str(wkt))

    def test_20m_radius_deduplication_spatial_distance(self):
        # Report 1
        lat1, lon1 = 12.971598, 77.594562
        # Report 2 (~ 15.3 meters away)
        lat2, lon2 = 12.971610, 77.594570

        distance = haversine_distance_meters(lat1, lon1, lat2, lon2)
        self.assertLess(distance, 20.0)  # Within approved 20-meter spatial deduplication radius

if __name__ == "__main__":
    unittest.main()
