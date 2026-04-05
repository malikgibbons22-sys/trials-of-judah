"""Tests for map_service."""


def test_get_eras_returns_16(map_service):
    eras = map_service.get_eras()
    assert len(eras) == 16
    assert eras[0]["name"] == "Table of Nations"


def test_get_kingdoms_returns_all(map_service):
    kingdoms = map_service.get_kingdoms()
    assert len(kingdoms) >= 15
    assert all("name" in k for k in kingdoms)
    assert all("boundaries" in k for k in kingdoms)


def test_get_era_returns_active_kingdoms(map_service):
    result = map_service.get_era("united_kingdom")
    assert result["era"] is not None
    assert result["era"]["name"] == "United Kingdom"
    assert len(result["kingdoms"]) > 0
    assert len(result["cities"]) > 0


def test_get_era_invalid_returns_empty(map_service):
    result = map_service.get_era("nonexistent_era")
    assert result["era"] is None
    assert result["kingdoms"] == []
    assert result["cities"] == []


def test_get_kingdom_by_id(map_service):
    result = map_service.get_kingdom("egypt")
    assert result is not None
    assert result["kingdom"]["name"] == "Egypt"
    assert "cities" in result


def test_get_kingdom_invalid_returns_none(map_service):
    assert map_service.get_kingdom("nonexistent") is None


def test_get_kingdom_geojson(map_service):
    geojson = map_service.get_kingdom_geojson("egypt", "united_kingdom")
    if geojson:
        assert geojson["type"] == "Feature"
        assert "geometry" in geojson


def test_search_kingdoms_by_name(map_service):
    result = map_service.search("Egypt")
    assert len(result["kingdoms"]) > 0
    assert result["kingdoms"][0]["name"] == "Egypt"


def test_search_kingdoms_by_alias(map_service):
    result = map_service.search("Mizraim")
    assert len(result["kingdoms"]) > 0


def test_search_peoples(map_service):
    result = map_service.search("Armenian")
    assert len(result["peoples"]) > 0


def test_search_cities(map_service):
    result = map_service.search("Jerusalem")
    assert len(result["cities"]) > 0


def test_search_case_insensitive(map_service):
    result1 = map_service.search("egypt")
    result2 = map_service.search("EGYPT")
    assert len(result1["kingdoms"]) == len(result2["kingdoms"])


def test_get_peoples_returns_all(map_service):
    peoples = map_service.get_peoples()
    assert len(peoples) >= 10
    assert all("modern_name" in p for p in peoples)
    assert all("era_narratives" in p for p in peoples)


def test_get_people_by_id(map_service):
    people = map_service.get_people(1)
    assert people is not None
    assert "modern_name" in people
    assert "era_narratives" in people


def test_get_people_invalid_returns_none(map_service):
    assert map_service.get_people(9999) is None


def test_era_kingdoms_have_geojson_or_none(map_service):
    result = map_service.get_era("table_of_nations")
    for k in result["kingdoms"]:
        geo = k.get("geojson")
        if geo is not None:
            assert geo["type"] == "Feature"
            assert "geometry" in geo


def test_cities_have_coordinates(map_service):
    kingdoms_data = map_service._kingdoms_data
    for c in kingdoms_data["cities"]:
        assert "lat" in c, f"City {c['name']} missing lat"
        assert "lng" in c, f"City {c['name']} missing lng"
        assert isinstance(c["lat"], (int, float)), f"City {c['name']} lat not numeric"
        assert isinstance(c["lng"], (int, float)), f"City {c['name']} lng not numeric"
