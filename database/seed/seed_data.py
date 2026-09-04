"""
Development Seed Data Script for CleanLoop Phase 1
Creates fake test users and sample garbage reports (including spatial near-duplicates within 20m).
"""

from sqlalchemy.orm import Session
from geoalchemy2.elements import WKTElement
from database.models import User, GarbageReport, UserRole, WasteCategory, VolumeTier, ReportStatus

SEED_USERS = [
    {"username": "demo_commander", "email": "commander@cleanloop.local", "role": UserRole.COMMANDER},
    {"username": "dispatcher_alex", "email": "alex@cleanloop.local", "role": UserRole.DISPATCHER},
    {"username": "citizen_reporter_01", "email": "reporter01@cleanloop.local", "role": UserRole.CITIZEN},
    {"username": "citizen_reporter_02", "email": "reporter02@cleanloop.local", "role": UserRole.CITIZEN},
]

# Sample garbage reports with coordinates around central urban area (Bangalore coordinates 12.9716, 77.5946)
SEED_REPORTS = [
    {
        "description": "Accumulated plastic bottles and packaging near park entrance",
        "latitude": 12.971598,
        "longitude": 77.594562,
        "category": WasteCategory.DRY,
        "volume_tier": VolumeTier.MODERATE,
        "status": ReportStatus.REPORTED,
        "image_url": "storage/uploads/demo_dry_waste_01.jpg",
    },
    {
        # Geographically close report (~ 15 meters away from Report 1 for 20m spatial deduplication testing)
        "description": "Overflowing plastic container dump near park entrance corner",
        "latitude": 12.971610,
        "longitude": 77.594570,
        "category": WasteCategory.DRY,
        "volume_tier": VolumeTier.MINOR,
        "status": ReportStatus.REPORTED,
        "image_url": "storage/uploads/demo_dry_waste_02.jpg",
    },
    {
        "description": "Discarded electronic parts and old cables on sidewalk",
        "latitude": 12.975000,
        "longitude": 77.598000,
        "category": WasteCategory.ELECTRONIC,
        "volume_tier": VolumeTier.MINOR,
        "status": ReportStatus.UNDER_REVIEW,
        "image_url": "storage/uploads/demo_ewaste_01.jpg",
    },
    {
        "description": "Major dumping pile of organic food waste and mixed debris behind market",
        "latitude": 12.980000,
        "longitude": 77.600000,
        "category": WasteCategory.MIXED,
        "volume_tier": VolumeTier.BULK,
        "status": ReportStatus.APPROVED,
        "image_url": "storage/uploads/demo_bulk_mixed_01.jpg",
    },
]

def seed_database(db_session: Session):
    """Seed initial development users and garbage reports into database."""
    print("[+] Seeding development users...")
    user_instances = {}
    for user_data in SEED_USERS:
        existing = db_session.query(User).filter_by(username=user_data["username"]).first()
        if not existing:
            user = User(**user_data)
            db_session.add(user)
            db_session.flush()
            user_instances[user_data["username"]] = user
        else:
            user_instances[user_data["username"]] = existing

    print("[+] Seeding sample garbage reports...")
    reporter = user_instances.get("citizen_reporter_01")
    reporter_id = reporter.id if reporter else None

    for report_data in SEED_REPORTS:
        lat = report_data["latitude"]
        lon = report_data["longitude"]
        point_wkt = f"POINT({lon} {lat})"

        report = GarbageReport(
            reporter_id=reporter_id,
            description=report_data["description"],
            latitude=lat,
            longitude=lon,
            location=WKTElement(point_wkt, srid=4326),
            category=report_data["category"],
            volume_tier=report_data["volume_tier"],
            status=report_data["status"],
            image_url=report_data["image_url"],
        )
        db_session.add(report)

    db_session.commit()
    print("[✓] Seed data inserted successfully.")
