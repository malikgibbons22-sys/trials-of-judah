"""Historical events service for contextual inline links."""
import json
from pathlib import Path
from backend.config import DATA_DIR


class EventsService:

    def __init__(self):
        self._data = None

    def _load_data(self):
        if self._data is not None:
            return
        events_file = DATA_DIR / "historical_events.json"
        if events_file.exists():
            with open(events_file, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        else:
            self._data = {"events": []}

    def get_all_events(self) -> list:
        """Return all events (for frontend to cache)."""
        self._load_data()
        return self._data["events"]

    def get_event(self, event_id: str) -> dict | None:
        """Return single event by ID."""
        self._load_data()
        return next((e for e in self._data["events"] if e["id"] == event_id), None)

    def search(self, query: str) -> list:
        """Search events by name or summary."""
        self._load_data()
        q = query.lower()
        return [
            {"id": e["id"], "name": e["name"], "date_range": e["date_range"], "region": e.get("region", "")}
            for e in self._data["events"]
            if q in e["name"].lower() or q in e.get("summary", "").lower()
        ][:10]


events_service = EventsService()
