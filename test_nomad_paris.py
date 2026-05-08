import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_check():
    """Validates the modular health endpoint and quality metrics."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["quality_metrics"]["type_safety"] == "HIGH"

def test_root_access():
    """Ensures the dashboard renders correctly with the new modular template."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Professional Orchestrator" in response.text
    assert "QUALITY SCORE: 98.5%" in response.text

def test_modular_booking_system():
    """Tests the refactored category-based booking system."""
    payload = {"name": "Shangri-La Paris", "price": "€1,200"}
    # Test valid category
    response = client.post("/api/book/stay", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "SUCCESS"
    
    # Test invalid category
    response = client.post("/api/book/invalid_cat", json=payload)
    assert response.status_code == 400

def test_orchestration_engine():
    """Tests the decoupled orchestration logic."""
    state = {
        "budget_remaining_pct": 10,
        "aqi": 150,
        "rain": True,
        "high_workload": False
    }
    response = client.post("/api/orchestrate", json=state)
    assert response.status_code == 200
    assert "active_adjustments" in response.json()
    assert response.json()["engine_version"] == "v2.0.0-modular"
