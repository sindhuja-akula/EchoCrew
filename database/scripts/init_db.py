"""
CleanLoop Database Initializer Script
Initializes PostGIS extensions, creates ORM tables, and executes seeding.
"""

import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sqlalchemy import text
from backend.app.database import engine, SessionLocal
from database.models import Base
from database.seed.seed_data import seed_database

def init_db():
    print("==========================================")
    print("      CleanLoop Database Initializer      ")
    print("==========================================")

    with engine.connect() as conn:
        print("[!] Enabling PostGIS extension...")
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
        conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
        conn.commit()

    print("[!] Creating database tables from ORM metadata...")
    Base.metadata.create_all(bind=engine)
    print("[✓] Tables created.")

    print("[!] Running seed data script...")
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

    print("[SUCCESS] Database initialized successfully!")

if __name__ == "__main__":
    init_db()
