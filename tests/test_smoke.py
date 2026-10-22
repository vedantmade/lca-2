import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from fastapi.testclient import TestClient  # noqa: E402
from main import app  # noqa: E402

client = TestClient(app)


def test_frontend_served():
    r = client.get("/")
    assert r.status_code == 200
    assert "html" in r.text.lower()


def test_openapi_available():
    r = client.get("/openapi.json")
    assert r.status_code == 200
