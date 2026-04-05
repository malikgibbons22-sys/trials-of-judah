"""Evidence service for Biblical Kingdoms map evidence pins."""
import json
from pathlib import Path
from backend.config import DATA_DIR


class EvidenceService:

    def __init__(self):
        self._data = None

    def _load_data(self):
        if self._data is not None:
            return
        evidence_file = DATA_DIR / "evidence.json"
        if evidence_file.exists():
            with open(evidence_file, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        else:
            self._data = {"biblical_events": [], "evidence": []}

    def _get_era_order(self):
        """Get era ordering from kingdoms.json for range comparisons."""
        kingdoms_file = DATA_DIR / "kingdoms.json"
        if not kingdoms_file.exists():
            return []
        with open(kingdoms_file, "r", encoding="utf-8") as f:
            kdata = json.load(f)
        return [e["id"] for e in kdata["eras"]]

    def get_biblical_events(self) -> list:
        self._load_data()
        return self._data["biblical_events"]

    def get_evidence_summary(self, era: str = None, evidence_type: str = None) -> list:
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
        for e in self._data["evidence"]:
            if evidence_type and e["type"] != evidence_type:
                continue
            if era and era_order and era_idx is not None:
                try:
                    start_idx = era_order.index(e["era_start"])
                    end_idx = era_order.index(e["era_end"])
                except ValueError:
                    continue
                if not (start_idx <= era_idx <= end_idx):
                    continue
            results.append({
                "id": e["id"],
                "name": e["name"],
                "type": e["type"],
                "category": e.get("category", ""),
                "lat": e["lat"],
                "lng": e["lng"],
                "coordinate_type": e.get("coordinate_type", "exact"),
                "era_start": e["era_start"],
                "era_end": e["era_end"],
                "biblical_event_id": e.get("biblical_event_id"),
                "reliability": e.get("reliability", "confirmed"),
            })
        return results

    def get_evidence(self, evidence_id: str) -> dict | None:
        """Full detail for one evidence entry."""
        self._load_data()
        return next((e for e in self._data["evidence"] if e["id"] == evidence_id), None)

    def get_connections(self, biblical_event_id: str) -> dict:
        """All pins + event coordinates for a given biblical event."""
        self._load_data()
        event = next((e for e in self._data["biblical_events"] if e["id"] == biblical_event_id), None)
        if not event:
            return {"event": None, "pins": []}
        pins = [
            {"id": e["id"], "name": e["name"], "lat": e["lat"], "lng": e["lng"],
             "type": e["type"], "culture": e.get("culture", ""), "coordinate_type": e.get("coordinate_type", "exact")}
            for e in self._data["evidence"]
            if e.get("biblical_event_id") == biblical_event_id
        ]
        return {"event": event, "pins": pins}

    def search(self, query: str) -> list:
        """Search evidence by name, culture, description."""
        self._load_data()
        q = query.lower()
        return [
            {"id": e["id"], "name": e["name"], "type": e["type"],
             "culture": e.get("culture", ""), "reliability": e.get("reliability", "")}
            for e in self._data["evidence"]
            if q in e["name"].lower()
            or q in e.get("culture", "").lower()
            or q in e.get("description", "").lower()
        ][:15]


evidence_service = EvidenceService()
