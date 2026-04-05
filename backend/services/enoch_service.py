"""Enoch study service — loads and queries canon and parallel data."""
import json
from pathlib import Path
from backend.config import DATA_DIR


class EnochService:

    def __init__(self):
        self._canon = None
        self._parallels = None
        self._images = None

    def _load_canon(self):
        if self._canon is not None:
            return
        canon_file = DATA_DIR / "enoch_canon.json"
        if canon_file.exists():
            with open(canon_file, "r", encoding="utf-8") as f:
                self._canon = json.load(f)
        else:
            self._canon = []

    def _load_parallels(self):
        if self._parallels is not None:
            return
        parallels_file = DATA_DIR / "enoch_parallels.json"
        if parallels_file.exists():
            with open(parallels_file, "r", encoding="utf-8") as f:
                self._parallels = json.load(f)
        else:
            self._parallels = []

    def _load_images(self):
        if self._images is not None:
            return
        images_file = DATA_DIR / "enoch_images.json"
        if images_file.exists():
            with open(images_file, "r", encoding="utf-8") as f:
                self._images = json.load(f)
        else:
            self._images = []

    def get_canon(self) -> list:
        """Return all canonicity evidence cards, ordered."""
        self._load_canon()
        return sorted(self._canon, key=lambda c: c.get("order", 0))

    def get_categories(self) -> list:
        """Return the mythology region categories with entry counts."""
        self._load_parallels()
        category_meta = {
            "mesopotamian": {"id": "mesopotamian", "label": "Mesopotamian", "subtitle": "Sumerian & Babylonian"},
            "greek": {"id": "greek", "label": "Greek", "subtitle": "Titans, Olympians & Heroes"},
            "egyptian": {"id": "egyptian", "label": "Egyptian", "subtitle": "The Nile Civilization"},
            "norse": {"id": "norse", "label": "Norse", "subtitle": "The Northern Tradition"},
            "hindu": {"id": "hindu", "label": "Hindu", "subtitle": "Vedic & Puranic"},
            "native_american": {"id": "native_american", "label": "Native American & Mesoamerican", "subtitle": "Traditions of the Americas"},
            "african": {"id": "african", "label": "African", "subtitle": "Oral Traditions of the Continent"},
            "east_asian": {"id": "east_asian", "label": "East Asian", "subtitle": "Chinese, Japanese & Korean"},
        }
        counts = {}
        for entry in self._parallels:
            cat = entry.get("category", "")
            counts[cat] = counts.get(cat, 0) + 1

        result = []
        for cat_id, meta in category_meta.items():
            if counts.get(cat_id, 0) > 0:
                result.append({**meta, "entry_count": counts[cat_id]})
        return result

    def get_parallels(self, category: str = None) -> list:
        """Return parallel entries, optionally filtered by category."""
        self._load_parallels()
        if category:
            return [e for e in self._parallels if e.get("category") == category]
        return self._parallels

    def get_image_manifest(self) -> list:
        """Return the full image manifest."""
        self._load_images()
        return self._images


enoch_service = EnochService()
