"""Martyrs service for Biblical Kingdoms map martyrs layer."""
import json
from pathlib import Path
from backend.config import DATA_DIR


class MartyrsService:

    def __init__(self):
        self._data = None

    def _load_data(self):
        if self._data is not None:
            return
        martyrs_file = DATA_DIR / "martyrs.json"
        if martyrs_file.exists():
            with open(martyrs_file, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        else:
            self._data = {"martyrs": []}

    def _get_era_order(self):
        """Get era ordering from kingdoms.json for range comparisons."""
        kingdoms_file = DATA_DIR / "kingdoms.json"
        if not kingdoms_file.exists():
            return []
        with open(kingdoms_file, "r", encoding="utf-8") as f:
            kdata = json.load(f)
        return [e["id"] for e in kdata["eras"]]

    def get_martyrs_summary(self, era: str = None) -> list:
        """Lightweight list for pin rendering."""
        self._load_data()
        era_order = self._get_era_order() if era else []
        era_idx = None
        if era and era_order:
            try:
                era_idx = era_order.index(era)
            except ValueError:
                pass

        results = []
        for m in self._data["martyrs"]:
            if era and era_order and era_idx is not None:
                try:
                    m_era_idx = era_order.index(m["era_id"])
                except ValueError:
                    continue
                if m_era_idx != era_idx:
                    continue
            results.append({
                "id": m["id"],
                "name": m["name"],
                "title": m.get("title", ""),
                "lat": m["lat"],
                "lng": m["lng"],
                "location": m.get("location", ""),
                "year_of_death": m.get("year_of_death"),
                "era_id": m["era_id"],
                "method": m.get("method", ""),
                "recognized_by": m.get("recognized_by", ""),
            })
        return results

    def get_martyr(self, martyr_id: str) -> dict | None:
        """Full detail for one martyr."""
        self._load_data()
        return next((m for m in self._data["martyrs"] if m["id"] == martyr_id), None)

    def search(self, query: str) -> list:
        """Search martyrs by name, title, location."""
        self._load_data()
        q = query.lower()
        return [
            {"id": m["id"], "name": m["name"], "title": m.get("title", ""),
             "location": m.get("location", ""), "recognized_by": m.get("recognized_by", "")}
            for m in self._data["martyrs"]
            if q in m["name"].lower()
            or q in m.get("title", "").lower()
            or q in m.get("location", "").lower()
            or q in m.get("description", "").lower()
        ][:15]


martyrs_service = MartyrsService()
