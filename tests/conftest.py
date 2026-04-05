"""Shared test fixtures."""
import pytest


@pytest.fixture
def map_service():
    from backend.services.map_service import MapService
    svc = MapService()
    svc._load_data()
    return svc
