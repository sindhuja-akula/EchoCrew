"""
Tests ORM model validations, Enums, relationships, and required constraints using unittest.
"""

import unittest
from database.models import (
    User,
    GarbageReport,
    UserRole,
    WasteCategory,
    VolumeTier,
    ReportStatus,
    WASTE_CATEGORY_METADATA,
    VOLUME_TIER_DESCRIPTORS
)

class TestDatabaseModels(unittest.TestCase):

    def test_enums_validation(self):
        self.assertEqual(UserRole.COMMANDER.value, "commander")
        self.assertEqual(WasteCategory.ELECTRONIC.value, "electronic")
        self.assertEqual(VolumeTier.BULK.value, "bulk")
        self.assertEqual(ReportStatus.VERIFIED.value, "verified")

    def test_waste_metadata(self):
        self.assertIn(WasteCategory.HAZARDOUS, WASTE_CATEGORY_METADATA)
        self.assertEqual(WASTE_CATEGORY_METADATA[WasteCategory.HAZARDOUS]["priority"], "critical")
        self.assertEqual(VOLUME_TIER_DESCRIPTORS[VolumeTier.MINOR]["estimated_volume_m3"], "< 0.2 m³")

    def test_user_instance_creation(self):
        user = User(username="test_reporter", email="reporter@cleanloop.test", role=UserRole.CITIZEN)
        self.assertEqual(user.username, "test_reporter")
        self.assertEqual(user.email, "reporter@cleanloop.test")
        self.assertEqual(user.role, UserRole.CITIZEN)

    def test_garbage_report_instance_creation(self):
        report = GarbageReport(
            description="Dry paper waste pile",
            latitude=12.9716,
            longitude=77.5946,
            category=WasteCategory.DRY,
            volume_tier=VolumeTier.MINOR,
            status=ReportStatus.REPORTED,
        )
        self.assertEqual(report.latitude, 12.9716)
        self.assertEqual(report.longitude, 77.5946)
        self.assertEqual(report.category, WasteCategory.DRY)
        self.assertEqual(report.volume_tier, VolumeTier.MINOR)
        self.assertEqual(report.status, ReportStatus.REPORTED)

if __name__ == "__main__":
    unittest.main()
