"""Map service for Biblical Kingdoms map tab."""
import json
from pathlib import Path
from backend.config import DATA_DIR


class MapService:

    def __init__(self):
        self._kingdoms_data = None
        self._peoples_data = None
        self._geojson_cache = {}

    def _load_data(self):
        """Load kingdom and peoples metadata from JSON files. Lazy-loaded on first access."""
        if self._kingdoms_data is None:
            kingdoms_file = DATA_DIR / "kingdoms.json"
            if kingdoms_file.exists():
                with open(kingdoms_file, "r", encoding="utf-8") as f:
                    self._kingdoms_data = json.load(f)
            else:
                self._kingdoms_data = {"eras": [], "kingdoms": [], "cities": []}

        if self._peoples_data is None:
            peoples_file = DATA_DIR / "peoples.json"
            if peoples_file.exists():
                with open(peoples_file, "r", encoding="utf-8") as f:
                    self._peoples_data = json.load(f)
            else:
                self._peoples_data = {"peoples": []}

    def _load_geojson(self, filename: str) -> dict | None:
        """Load a GeoJSON file from disk, with caching."""
        if filename in self._geojson_cache:
            return self._geojson_cache[filename]
        geojson_path = DATA_DIR / "map" / "geojson" / filename
        if not geojson_path.exists():
            return None
        with open(geojson_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._geojson_cache[filename] = data
        return data

    def get_eras(self) -> list:
        """Return all era definitions for the slider."""
        self._load_data()
        return self._kingdoms_data["eras"]

    def get_kingdoms(self) -> list:
        """Return all kingdom metadata without GeoJSON geometry."""
        self._load_data()
        return self._kingdoms_data["kingdoms"]

    def get_era(self, era_id: str) -> dict:
        """Return kingdoms and cities active in a specific era, with GeoJSON loaded."""
        self._load_data()
        era = next((e for e in self._kingdoms_data["eras"] if e["id"] == era_id), None)
        if not era:
            return {"era": None, "kingdoms": [], "cities": []}

        active_kingdoms = []
        for k in self._kingdoms_data["kingdoms"]:
            boundary = self._find_boundary_for_era(k, era_id)
            if boundary:
                kingdom_copy = {key: val for key, val in k.items() if key != "boundaries"}
                kingdom_copy["geojson"] = self._load_geojson(boundary["geojson_file"])
                kingdom_copy["boundary_era_start"] = boundary["era_start"]
                kingdom_copy["boundary_era_end"] = boundary["era_end"]
                active_kingdoms.append(kingdom_copy)

        active_cities = self._get_cities_for_era(era_id)

        return {"era": era, "kingdoms": active_kingdoms, "cities": active_cities}

    def _find_boundary_for_era(self, kingdom: dict, era_id: str) -> dict | None:
        """Find the boundary entry that covers the given era."""
        era_order = [e["id"] for e in self._kingdoms_data["eras"]]
        try:
            era_idx = era_order.index(era_id)
        except ValueError:
            return None
        for b in kingdom.get("boundaries", []):
            try:
                start_idx = era_order.index(b["era_start"])
                end_idx = era_order.index(b["era_end"])
            except ValueError:
                continue
            if start_idx <= era_idx <= end_idx:
                return b
        return None

    def _get_cities_for_era(self, era_id: str) -> list:
        """Get all cities active in a given era with their current kingdom association."""
        era_order = [e["id"] for e in self._kingdoms_data["eras"]]
        try:
            era_idx = era_order.index(era_id)
        except ValueError:
            return []
        active_cities = []
        for c in self._kingdoms_data["cities"]:
            for assoc in c.get("kingdom_associations", []):
                try:
                    start_idx = era_order.index(assoc["era_start"])
                    end_idx = era_order.index(assoc["era_end"])
                except ValueError:
                    continue
                if start_idx <= era_idx <= end_idx:
                    city_copy = dict(c)
                    city_copy["current_kingdom_id"] = assoc["kingdom_id"]
                    city_copy["role"] = assoc.get("role", "")
                    active_cities.append(city_copy)
                    break
        return active_cities

    def get_kingdom(self, kingdom_id: str, era_id: str | None = None) -> dict | None:
        """Return full detail for one kingdom including cities."""
        self._load_data()
        kingdom = next((k for k in self._kingdoms_data["kingdoms"] if k["id"] == kingdom_id), None)
        if not kingdom:
            return None
        cities = []
        era_order = [e["id"] for e in self._kingdoms_data["eras"]]
        for c in self._kingdoms_data["cities"]:
            for assoc in c.get("kingdom_associations", []):
                if assoc["kingdom_id"] == kingdom_id:
                    if era_id is None:
                        cities.append(dict(c))
                        break
                    else:
                        try:
                            start_idx = era_order.index(assoc["era_start"])
                            end_idx = era_order.index(assoc["era_end"])
                            era_idx = era_order.index(era_id)
                        except ValueError:
                            continue
                        if start_idx <= era_idx <= end_idx:
                            cities.append(dict(c))
                            break
        return {"kingdom": kingdom, "cities": cities}

    def get_kingdom_geojson(self, kingdom_id: str, era_id: str) -> dict | None:
        """Return GeoJSON for a specific kingdom in a specific era."""
        self._load_data()
        kingdom = next((k for k in self._kingdoms_data["kingdoms"] if k["id"] == kingdom_id), None)
        if not kingdom:
            return None
        boundary = self._find_boundary_for_era(kingdom, era_id)
        if not boundary:
            return None
        return self._load_geojson(boundary["geojson_file"])

    def get_peoples(self) -> list:
        """Return all peoples for the filter list."""
        self._load_data()
        return self._peoples_data["peoples"]

    def get_people(self, people_id: int) -> dict | None:
        """Return full detail for one people group."""
        self._load_data()
        return next((p for p in self._peoples_data["peoples"] if p["id"] == people_id), None)

    def search(self, query: str) -> dict:
        """Search kingdoms, cities, and peoples by name."""
        self._load_data()
        q = query.lower()
        kingdoms = [
            k for k in self._kingdoms_data["kingdoms"]
            if q in k["name"].lower()
            or any(q in alias.lower() for alias in k.get("aliases", []))
        ]
        cities = [
            c for c in self._kingdoms_data["cities"]
            if q in c["name"].lower()
        ]
        peoples = [
            p for p in self._peoples_data["peoples"]
            if q in p["modern_name"].lower()
            or q in p["biblical_ancestor"].lower()
        ]
        return {"kingdoms": kingdoms[:10], "cities": cities[:10], "peoples": peoples[:10]}

    async def get_cross_references(self, db, kingdom_name: str, aliases: list) -> dict:
        """Find prophecies and lineage persons related to a kingdom."""
        search_terms = [kingdom_name] + (aliases or [])

        # Search prophecies
        like_parts = []
        params = []
        for term in search_terms:
            t = f"%{term.lower()}%"
            like_parts.append("(LOWER(prophecy_text) LIKE ? OR LOWER(fulfillment_text) LIKE ? OR LOWER(title) LIKE ?)")
            params.extend([t, t, t])
        where_clause = " OR ".join(like_parts)

        prophecies = await db.execute(
            f"SELECT id, title, category, status, summary FROM prophecies WHERE {where_clause} LIMIT 10",
            tuple(params)
        )

        # Search lineage persons via modern_connections
        mc_parts = []
        mc_params = []
        for term in search_terms:
            mc_parts.append("LOWER(mc.region) LIKE ?")
            mc_params.append(f"%{term.lower()}%")
        mc_where = " OR ".join(mc_parts)

        persons = await db.execute(
            f"""SELECT DISTINCT p.id, p.name_english FROM persons p
                JOIN modern_connections mc ON mc.person_id = p.id
                WHERE {mc_where} LIMIT 10""",
            tuple(mc_params)
        )

        return {
            "prophecies": [dict(r) for r in prophecies],
            "persons": [dict(r) for r in persons],
        }


map_service = MapService()
