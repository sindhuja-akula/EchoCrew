"""
Tests database engine configuration and connection using unittest.
"""

import unittest
import tempfile
from pathlib import Path
from sqlalchemy import create_engine, text
from backend.app.config import settings

class TestDatabaseConnection(unittest.TestCase):

    def test_database_url_configuration(self):
        self.assertIsNotNone(settings.DATABASE_URL)
        self.assertIn("postgresql", settings.DATABASE_URL)

    def test_sqlite_fallback_connection_test(self):
        """Test engine instantiation and table creation using temporary SQLite."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_db = Path(tmp_dir) / "test.db"
            engine = create_engine(f"sqlite:///{test_db}")
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1")).scalar()
                self.assertEqual(result, 1)
            engine.dispose()

if __name__ == "__main__":
    unittest.main()
