"""
CleanLoop Database Reset Script
Drops public schema and re-initializes clean database structure.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sqlalchemy import text
from backend.app.database import engine
from database.scripts.init_db import init_db

def reset_db():
    print("==========================================")
    print("        CleanLoop Database Reset          ")
    print("==========================================")

    with engine.connect() as conn:
        print("[!] Dropping existing schema CASCADE...")
        conn.execute(text("DROP SCHEMA public CASCADE;"))
        conn.execute(text("CREATE SCHEMA public;"))
        conn.execute(text("GRANT ALL ON SCHEMA public TO public;"))
        conn.commit()

    print("[✓] Schema reset complete. Re-initializing database...")
    init_db()

if __name__ == "__main__":
    reset_db()
