import os
import sys
import unittest
from fastapi.testclient import TestClient

# Ensure root sys.path includes backend and database directories
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.core.database import get_db

client = TestClient(app)
