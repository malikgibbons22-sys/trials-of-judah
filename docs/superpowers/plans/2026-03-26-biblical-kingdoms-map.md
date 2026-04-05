# Biblical Kingdoms Map Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a full interactive map tab to Trials of Judah showing all biblical kingdoms, peoples, and cities across ~16 eras with animated transitions, peoples filter, bidirectional app integration, and unified search.

**Architecture:** Leaflet.js map rendered in a new "Map" tab, backed by a `map_service.py` that serves kingdom/peoples/city data from JSON files. GeoJSON polygon boundaries are split per-era per-kingdom for performance. The frontend is a single-page inline JS/CSS addition to the existing `index.html` monolith. No build tools.

**Tech Stack:** Leaflet.js (CDN), Python/FastAPI backend, aiosqlite, GeoJSON, vanilla JavaScript

**Spec:** `docs/superpowers/specs/2026-03-26-biblical-kingdoms-map-design.md`

---

## File Structure

### New Files
| File | Responsibility |
|------|---------------|
| `backend/services/map_service.py` | Load/query kingdom, peoples, city data; cross-reference with prophecy/lineage |
| `backend/data/kingdoms.json` | Kingdom metadata: names, eras, capitals, scripture refs, boundary file refs |
| `backend/data/peoples.json` | Modern peoples filter data: ancestor, lineage, era narratives, kingdom mappings |
| `backend/data/map/geojson/*.json` | GeoJSON polygon files per kingdom per era |
| `tests/conftest.py` | Shared pytest fixtures (test DB, async client) |
| `tests/test_map_service.py` | Unit tests for map_service |
| `tests/test_map_endpoints.py` | Integration tests for /api/map/* endpoints |

### Modified Files
| File | Changes |
|------|---------|
| `backend/main.py` | Add map endpoints, import map_service, seed map data |
| `backend/services/search_service.py` | Add kingdom/city search to unified search |
| `backend/services/lineage_service.py` | Add map_location to person response |
| `backend/services/prophecy_service.py` | Add map_location to prophecy response |
| `backend/requirements.txt` | Add pytest, pytest-asyncio, httpx[test] |
| `frontend/index.html` | Add Map tab HTML/CSS/JS, Leaflet CDN, mini-map in search, "View on Map" buttons |

---

## Chunk 1: Backend Data & Service Foundation

### Task 1: Create kingdoms.json seed data

**Files:**
- Create: `backend/data/kingdoms.json`

This is the core data file. Start with era definitions and 10-15 major kingdoms to prove the pattern. More kingdoms will be added incrementally.

- [ ] **Step 1: Create the eras array**

Create `backend/data/kingdoms.json` with all 16 era definitions:

```json
{
  "eras": [
    {
      "id": 1, "name": "Table of Nations", "date_approx": "~2200 BC",
      "scripture_ref": "Genesis 10-11",
      "description": "After Babel, Noah's descendants spread across the earth.",
      "sort_order": 1
    },
    {
      "id": 2, "name": "Abraham's Journey", "date_approx": "~2000 BC",
      "scripture_ref": "Genesis 12",
      "description": "Abram journeys from Ur to Canaan by God's command.",
      "sort_order": 2
    },
    {
      "id": 3, "name": "Sojourn in Egypt", "date_approx": "~1876 BC",
      "scripture_ref": "Genesis 46",
      "description": "Jacob's family enters Egypt during the famine.",
      "sort_order": 3
    },
    {
      "id": 4, "name": "Exodus & Wilderness", "date_approx": "~1446 BC",
      "scripture_ref": "Exodus 12-14",
      "description": "God delivers Israel from Egypt through Moses.",
      "sort_order": 4
    },
    {
      "id": 5, "name": "Conquest of Canaan", "date_approx": "~1406 BC",
      "scripture_ref": "Joshua 1-12",
      "description": "Joshua leads Israel into the promised land.",
      "sort_order": 5
    },
    {
      "id": 6, "name": "Period of Judges", "date_approx": "~1380-1050 BC",
      "scripture_ref": "Judges",
      "description": "Tribal territories established, cycles of sin and deliverance.",
      "sort_order": 6
    },
    {
      "id": 7, "name": "United Kingdom", "date_approx": "~1050-930 BC",
      "scripture_ref": "1 Samuel - 1 Kings 11",
      "description": "Saul, David, and Solomon rule a united Israel.",
      "sort_order": 7
    },
    {
      "id": 8, "name": "Divided Kingdom", "date_approx": "~930 BC",
      "scripture_ref": "1 Kings 12",
      "description": "The kingdom splits: Israel (north) and Judah (south).",
      "sort_order": 8
    },
    {
      "id": 9, "name": "Fall of Samaria", "date_approx": "722 BC",
      "scripture_ref": "2 Kings 17",
      "description": "Assyria conquers the northern kingdom; ten tribes scattered.",
      "sort_order": 9
    },
    {
      "id": 10, "name": "Babylonian Exile", "date_approx": "586 BC",
      "scripture_ref": "2 Kings 25",
      "description": "Babylon destroys Jerusalem and the temple; Judah exiled.",
      "sort_order": 10
    },
    {
      "id": 11, "name": "Persian Period", "date_approx": "~539 BC",
      "scripture_ref": "Ezra 1",
      "description": "Cyrus conquers Babylon; remnant returns to rebuild.",
      "sort_order": 11
    },
    {
      "id": 12, "name": "Greek Period", "date_approx": "~330 BC",
      "scripture_ref": "Daniel 8",
      "description": "Alexander conquers Persia; Hellenistic influence spreads.",
      "sort_order": 12
    },
    {
      "id": 13, "name": "Maccabean Period", "date_approx": "~167-63 BC",
      "scripture_ref": "1 Maccabees",
      "description": "Israelite revolt against Greek oppression; temple rededicated.",
      "sort_order": 13
    },
    {
      "id": 14, "name": "Roman Period", "date_approx": "~63 BC",
      "scripture_ref": "Luke 2:1",
      "description": "Rome conquers the region; Herod rules as client king.",
      "sort_order": 14
    },
    {
      "id": 15, "name": "Jesus's Ministry", "date_approx": "~AD 30",
      "scripture_ref": "The Gospels",
      "description": "The Messiah ministers in Galilee, Judea, and surrounding regions.",
      "sort_order": 15
    },
    {
      "id": 16, "name": "Early Church", "date_approx": "~AD 33-65",
      "scripture_ref": "Acts",
      "description": "The gospel spreads from Jerusalem to Rome and beyond.",
      "sort_order": 16
    }
  ],
  "kingdoms": [],
  "cities": []
}
```

- [ ] **Step 2: Add initial kingdom entries (10-15 major kingdoms)**

Add to the `kingdoms` array. Each kingdom has metadata only — no GeoJSON inline. Include: Egypt, Assyria, Babylon, Persia, Greece, Rome, Israel (united), Israel (north), Judah (south), Philistia, Moab, Edom, Aram/Syria, Phoenicia, Cush/Ethiopia.

Example entry pattern:
```json
{
  "id": 1,
  "name": "Egypt",
  "name_hebrew": "Mitzrayim",
  "aliases": ["Mizraim", "Mitzrayim", "land of Egypt", "Pharaoh's kingdom"],
  "ancestor": "Mizraim son of Ham",
  "ancestor_ref": "Genesis 10:6",
  "capital": "Memphis / Thebes",
  "border_accuracy": "documented",
  "modern_region": "Modern Egypt",
  "description": "One of the oldest civilizations, Egypt features prominently throughout scripture from Abraham's sojourn to the Exodus to the flight of Joseph, Mary, and Jesus.",
  "scholarly_context": "Archaeological evidence confirms Egypt as a major power from the Old Kingdom (~2686 BC) through the Ptolemaic period (332-30 BC). The Merneptah Stele (~1208 BC) contains the earliest extrabiblical reference to Israel.",
  "scripture_refs": ["Genesis 12:10", "Genesis 37:28", "Exodus 1:8-14", "Exodus 12:31-42", "Isaiah 19:1", "Hosea 11:1", "Matthew 2:13-15"],
  "boundaries": [
    { "era_start": 1, "era_end": 4, "geojson_file": "egypt_new_kingdom.json" },
    { "era_start": 5, "era_end": 10, "geojson_file": "egypt_late_period.json" },
    { "era_start": 11, "era_end": 12, "geojson_file": "egypt_persian_satrapy.json" },
    { "era_start": 13, "era_end": 16, "geojson_file": "egypt_ptolemaic.json" }
  ]
}
```

Repeat for each initial kingdom with appropriate era ranges, scripture refs, and boundary file references.

- [ ] **Step 3: Add initial city entries (40-50 major cities)**

Add to the `cities` array. Each city needs coordinates, era range, and kingdom associations.

Example:
```json
{
  "id": 1,
  "name": "Jerusalem",
  "name_hebrew": "Yerushalayim",
  "lat": 31.7683,
  "lng": 35.2137,
  "is_capital": true,
  "is_major": true,
  "scripture_refs": ["2 Samuel 5:6-7", "1 Kings 11:36", "Psalm 122:1-3", "Luke 19:41-44"],
  "kingdom_associations": [
    { "kingdom_id": 7, "era_start": 7, "era_end": 7, "role": "capital" },
    { "kingdom_id": 9, "era_start": 8, "era_end": 10, "role": "capital" },
    { "kingdom_id": 5, "era_start": 11, "era_end": 11, "role": "provincial capital" },
    { "kingdom_id": 6, "era_start": 12, "era_end": 13, "role": "contested" },
    { "kingdom_id": 10, "era_start": 14, "era_end": 16, "role": "provincial capital" }
  ]
}
```

Key cities to include: Jerusalem, Babylon, Nineveh, Memphis/Thebes, Ur, Haran, Bethlehem, Nazareth, Capernaum, Damascus, Tyre, Sidon, Samaria, Shechem, Hebron, Jericho, Bethel, Beersheba, Gaza, Ashdod, Petra/Sela, Rome, Athens, Corinth, Ephesus, Antioch, Tarshish, Persepolis, Susa.

- [ ] **Step 4: Commit**

```bash
git add backend/data/kingdoms.json
git commit -m "feat(map): add kingdoms.json with eras, initial kingdoms, and cities"
```

---

### Task 2: Create GeoJSON boundary files

**Files:**
- Create: `backend/data/map/geojson/` directory
- Create: GeoJSON files for each kingdom-era combination

- [ ] **Step 1: Create the geojson directory**

```bash
mkdir -p backend/data/map/geojson
```

- [ ] **Step 2: Create GeoJSON files for documented kingdoms**

Each file is a GeoJSON Feature with polygon coordinates. Use approximate scholarly boundaries. Example for `egypt_new_kingdom.json`:

```json
{
  "type": "Feature",
  "properties": { "kingdom": "Egypt", "era": "New Kingdom" },
  "geometry": {
    "type": "Polygon",
    "coordinates": [[
      [25.0, 31.5], [30.0, 31.5], [34.5, 31.0], [34.5, 29.5],
      [33.0, 28.0], [33.5, 25.0], [33.5, 22.0], [31.0, 22.0],
      [29.0, 24.0], [25.0, 31.5]
    ]]
  }
}
```

Create files for all boundary references in kingdoms.json. Start with the major kingdoms:
- `egypt_new_kingdom.json`, `egypt_late_period.json`, `egypt_persian_satrapy.json`, `egypt_ptolemaic.json`
- `assyria_early.json`, `assyria_peak.json`
- `babylon_empire.json`
- `persia_empire.json`
- `greece_alexander.json`, `greece_seleucid.json`
- `rome_republic.json`, `rome_empire.json`
- `israel_united.json`, `israel_north.json`, `judah_south.json`
- `philistia.json`, `moab.json`, `edom.json`, `aram_syria.json`, `phoenicia.json`
- `cush_ethiopia.json`

Use dotted/approximate boundaries for less-documented kingdoms (indicated by `"border_accuracy": "approximate"` in kingdoms.json).

- [ ] **Step 3: Commit**

```bash
git add backend/data/map/geojson/
git commit -m "feat(map): add GeoJSON boundary files for initial kingdoms"
```

---

### Task 3: Create peoples.json seed data

**Files:**
- Create: `backend/data/peoples.json`

- [ ] **Step 1: Create peoples.json with initial entries**

Populate with modern-day peoples traced to biblical ancestors. Draw from existing `modern_connections` data in `lineage.json` plus additional research.

```json
{
  "peoples": [
    {
      "id": 1,
      "modern_name": "Egyptians",
      "biblical_ancestor": "Mizraim",
      "ancestor_ref": "Genesis 10:6",
      "lineage": "Ham > Mizraim",
      "kingdom_ids": [1],
      "migration_summary": "Settled in the Nile Valley. One of the oldest continuous civilizations.",
      "era_narratives": [
        { "era_id": 1, "text": "Mizraim, son of Ham, settled in the Nile Valley after the dispersion at Babel (Genesis 10:6)." },
        { "era_id": 3, "text": "Egypt hosts Jacob's family during the famine. Joseph rises to second-in-command (Genesis 41-47)." },
        { "era_id": 4, "text": "Pharaoh enslaves the Israelites. God delivers them through Moses with ten plagues (Exodus 1-14)." },
        { "era_id": 10, "text": "Nebuchadnezzar invades Egypt as prophesied by Jeremiah (Jeremiah 43:8-13)." },
        { "era_id": 15, "text": "Joseph, Mary, and Jesus flee to Egypt to escape Herod's massacre, fulfilling Hosea 11:1 (Matthew 2:13-15)." }
      ]
    },
    {
      "id": 2,
      "modern_name": "Armenians",
      "biblical_ancestor": "Togarmah",
      "ancestor_ref": "Genesis 10:3",
      "lineage": "Japheth > Gomer > Togarmah",
      "kingdom_ids": [14],
      "migration_summary": "Settled in eastern Asia Minor and the Caucasus. Armenian tradition claims descent from Togarmah (Torgom).",
      "era_narratives": [
        { "era_id": 1, "text": "Togarmah, son of Gomer, son of Japheth, settled in eastern Asia Minor after Babel (Genesis 10:3)." },
        { "era_id": 8, "text": "The house of Togarmah traded horses and mules with Tyre (Ezekiel 27:14). Beth-Togarmah identified with the Armenian highlands." },
        { "era_id": 12, "text": "Armenia falls under Seleucid, then Parthian influence after Alexander's conquests." }
      ]
    },
    {
      "id": 3,
      "modern_name": "Ethiopians / Cushites",
      "biblical_ancestor": "Cush",
      "ancestor_ref": "Genesis 10:6",
      "lineage": "Ham > Cush",
      "kingdom_ids": [15],
      "migration_summary": "Settled south of Egypt in Nubia and the Horn of Africa. The Kingdom of Kush was a major regional power.",
      "era_narratives": [
        { "era_id": 1, "text": "Cush, son of Ham, settled south of Egypt (Genesis 10:6). Father of Nimrod, the mighty hunter (Genesis 10:8-9)." },
        { "era_id": 7, "text": "The Queen of Sheba visits Solomon (1 Kings 10:1-13). Ethiopian tradition connects Sheba to the Cushite kingdom." },
        { "era_id": 9, "text": "Tirhakah king of Ethiopia (Cush) comes against Sennacherib of Assyria (2 Kings 19:9)." },
        { "era_id": 16, "text": "The Ethiopian eunuch, a minister of Candace queen of Ethiopia, is baptized by Philip (Acts 8:26-39)." }
      ]
    },
    {
      "id": 4,
      "modern_name": "Greeks",
      "biblical_ancestor": "Javan",
      "ancestor_ref": "Genesis 10:2",
      "lineage": "Japheth > Javan",
      "kingdom_ids": [6],
      "migration_summary": "Settled in the Aegean region. Javan is the Hebrew name for Greece (Ionia).",
      "era_narratives": [
        { "era_id": 1, "text": "Javan, son of Japheth, settled in the Aegean (Genesis 10:2). His sons Elishah, Tarshish, Kittim, and Dodanim spread across the Mediterranean." },
        { "era_id": 8, "text": "The isles of the Gentiles (Javan's territory) trade with Tyre (Ezekiel 27:13). Daniel's prophecy of the he-goat from the west (Daniel 8:5-8)." },
        { "era_id": 12, "text": "Alexander of Macedon fulfills Daniel's vision, conquering Persia and establishing Greek rule across the Near East (Daniel 8:5-8, 21)." },
        { "era_id": 16, "text": "Paul brings the gospel to Greece — Philippi, Thessalonica, Athens, Corinth (Acts 16-18)." }
      ]
    },
    {
      "id": 5,
      "modern_name": "Persians / Iranians",
      "biblical_ancestor": "Elam",
      "ancestor_ref": "Genesis 10:22",
      "lineage": "Shem > Elam",
      "kingdom_ids": [5],
      "migration_summary": "Settled in the Iranian plateau. Elam is among the oldest civilizations; Persia arose from the same region.",
      "era_narratives": [
        { "era_id": 1, "text": "Elam, son of Shem, settled east of Mesopotamia (Genesis 10:22). Chedorlaomer king of Elam was among the kings who fought Abraham (Genesis 14:1)." },
        { "era_id": 11, "text": "Cyrus king of Persia conquers Babylon and decrees the return of the Israelite exiles (Ezra 1:1-4). Isaiah named Cyrus by prophecy 150 years before his birth (Isaiah 44:28-45:1)." },
        { "era_id": 13, "text": "The events of Esther occur in the Persian court at Susa. Mordecai and Esther save the Israelites from Haman's plot." }
      ]
    },
    {
      "id": 6,
      "modern_name": "Arabs / Ishmaelites",
      "biblical_ancestor": "Ishmael",
      "ancestor_ref": "Genesis 16:11-12, Genesis 25:12-18",
      "lineage": "Shem > Abraham > Ishmael",
      "kingdom_ids": [],
      "migration_summary": "Settled across the Arabian Peninsula. Ishmael's twelve sons became tribal chiefs across the desert regions.",
      "era_narratives": [
        { "era_id": 2, "text": "Ishmael born to Abraham and Hagar (Genesis 16). God promises to make him a great nation (Genesis 17:20)." },
        { "era_id": 3, "text": "Ishmaelite traders buy Joseph from his brothers and sell him into Egypt (Genesis 37:25-28)." },
        { "era_id": 7, "text": "Arabian traders bring gold, spices, and precious stones to Solomon (1 Kings 10:15, 2 Chronicles 9:14)." }
      ]
    },
    {
      "id": 7,
      "modern_name": "Israelites (Twelve Tribes)",
      "biblical_ancestor": "Jacob/Israel",
      "ancestor_ref": "Genesis 32:28, Genesis 49",
      "lineage": "Shem > Abraham > Isaac > Jacob",
      "kingdom_ids": [7, 8, 9],
      "migration_summary": "The covenant people. Twelve tribes from Jacob's sons. United under David and Solomon, divided into Israel (north) and Judah (south), scattered among all nations after Assyrian and Babylonian conquests and the Roman destruction of AD 70.",
      "era_narratives": [
        { "era_id": 2, "text": "God calls Abraham out of Ur, promises him a great nation and a land (Genesis 12:1-3). The covenant passes through Isaac and Jacob." },
        { "era_id": 3, "text": "Jacob's family of 70 enters Egypt during the famine (Genesis 46:27). They grow into a multitude over 400 years." },
        { "era_id": 4, "text": "God delivers Israel from Egyptian slavery through Moses. The covenant is given at Sinai (Exodus 19-20)." },
        { "era_id": 5, "text": "Joshua leads the conquest of Canaan. The land is divided among the twelve tribes (Joshua 13-21)." },
        { "era_id": 7, "text": "The twelve tribes unite under Saul, then David, then Solomon. Jerusalem becomes the capital and the temple is built." },
        { "era_id": 8, "text": "The kingdom divides after Solomon. Ten tribes form the northern kingdom of Israel; Judah and Benjamin form the south." },
        { "era_id": 9, "text": "Assyria conquers the northern kingdom in 722 BC. The ten tribes are scattered among the nations (2 Kings 17:6-23). The Deuteronomy 28 curses begin their long fulfillment." },
        { "era_id": 10, "text": "Babylon destroys Jerusalem and the temple in 586 BC. Judah is exiled (2 Kings 25)." },
        { "era_id": 14, "text": "Under Roman rule, the land is divided into provinces. After AD 70 and AD 135, the remaining Israelites are scattered worldwide (Luke 21:24). The Deuteronomy 28 curses — slavery by ships, scattering, oppression, becoming a byword — identify where the true Israelites went." },
        { "era_id": 15, "text": "Yeshua (Jesus) the Messiah ministers among His people. 'I am not sent but unto the lost sheep of the house of Israel' (Matthew 15:24)." }
      ]
    },
    {
      "id": 8,
      "modern_name": "Syrians / Arameans",
      "biblical_ancestor": "Aram",
      "ancestor_ref": "Genesis 10:22",
      "lineage": "Shem > Aram",
      "kingdom_ids": [13],
      "migration_summary": "Settled in Syria and upper Mesopotamia. Their language Aramaic became the lingua franca of the ancient Near East.",
      "era_narratives": [
        { "era_id": 1, "text": "Aram, son of Shem, settled in Syria and upper Mesopotamia (Genesis 10:22-23)." },
        { "era_id": 2, "text": "Abraham sends his servant to Aram-naharaim to find a wife for Isaac — Rebekah (Genesis 24). Jacob works for Laban in Paddan-aram (Genesis 29)." },
        { "era_id": 8, "text": "Ben-hadad and Hazael of Damascus war against Israel and Judah (1 Kings 20, 2 Kings 8:7-15). Naaman the Syrian is healed of leprosy by Elisha (2 Kings 5)." },
        { "era_id": 16, "text": "Damascus is where Saul encounters Christ on the road (Acts 9:1-19). Ananias baptizes him there." }
      ]
    }
  ]
}
```

Add additional entries for: Libyans (Put), Lydians (Lud), Scythians/Germanic (Ashkenaz), Canaanites, Hittites (Heth), Philistines (Caphtorim), Moabites (Moab son of Lot), Edomites (Esau), Ammonites (Ben-Ammi son of Lot), Assyrians (Asshur), Babylonians/Chaldeans, Romans/Italians (Kittim), Spaniards (Tarshish).

- [ ] **Step 2: Commit**

```bash
git add backend/data/peoples.json
git commit -m "feat(map): add peoples.json with modern peoples and biblical history"
```

---

### Task 4: Create map_service.py

**Files:**
- Create: `backend/services/map_service.py`

- [ ] **Step 1: Create the service**

```python
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
        """Load kingdom and peoples metadata from JSON files."""
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

    def get_era(self, era_id: int) -> dict:
        """Return kingdoms and cities active in a specific era, with GeoJSON."""
        self._load_data()
        era = next((e for e in self._kingdoms_data["eras"] if e["id"] == era_id), None)
        if not era:
            return {"era": None, "kingdoms": [], "cities": []}

        active_kingdoms = []
        for k in self._kingdoms_data["kingdoms"]:
            # Find boundary for this era
            boundary = None
            for b in k.get("boundaries", []):
                if b["era_start"] <= era_id <= b["era_end"]:
                    boundary = b
                    break
            if boundary:
                kingdom_copy = {key: val for key, val in k.items() if key != "boundaries"}
                kingdom_copy["geojson"] = self._load_geojson(boundary["geojson_file"])
                kingdom_copy["boundary_era_start"] = boundary["era_start"]
                kingdom_copy["boundary_era_end"] = boundary["era_end"]
                active_kingdoms.append(kingdom_copy)

        active_cities = []
        for c in self._kingdoms_data["cities"]:
            for assoc in c.get("kingdom_associations", []):
                if assoc["era_start"] <= era_id <= assoc["era_end"]:
                    city_copy = dict(c)
                    city_copy["current_kingdom_id"] = assoc["kingdom_id"]
                    city_copy["role"] = assoc.get("role", "")
                    active_cities.append(city_copy)
                    break

        return {"era": era, "kingdoms": active_kingdoms, "cities": active_cities}

    def get_kingdom(self, kingdom_id: int, era_id: int | None = None) -> dict | None:
        """Return full detail for one kingdom including cities and cross-refs."""
        self._load_data()
        kingdom = next((k for k in self._kingdoms_data["kingdoms"] if k["id"] == kingdom_id), None)
        if not kingdom:
            return None

        # Get all cities associated with this kingdom
        cities = []
        for c in self._kingdoms_data["cities"]:
            for assoc in c.get("kingdom_associations", []):
                if assoc["kingdom_id"] == kingdom_id:
                    if era_id is None or (assoc["era_start"] <= era_id <= assoc["era_end"]):
                        cities.append(dict(c))
                        break

        return {"kingdom": kingdom, "cities": cities}

    def get_kingdom_geojson(self, kingdom_id: int, era_id: int) -> dict | None:
        """Return GeoJSON for a specific kingdom in a specific era."""
        self._load_data()
        kingdom = next((k for k in self._kingdoms_data["kingdoms"] if k["id"] == kingdom_id), None)
        if not kingdom:
            return None
        for b in kingdom.get("boundaries", []):
            if b["era_start"] <= era_id <= b["era_end"]:
                return self._load_geojson(b["geojson_file"])
        return None

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
        search_terms = [kingdom_name] + aliases
        like_clauses = " OR ".join(
            ["LOWER(prophecy_text) LIKE ? OR LOWER(fulfillment_text) LIKE ? OR LOWER(title) LIKE ?"]
            * len(search_terms)
        )
        params = []
        for term in search_terms:
            t = f"%{term.lower()}%"
            params.extend([t, t, t])

        prophecies = await db.execute(
            f"SELECT id, title, category, status, summary FROM prophecies WHERE {like_clauses} LIMIT 10",
            tuple(params)
        )

        # Find lineage persons via modern_connections
        mc_clauses = " OR ".join(["LOWER(mc.region) LIKE ?"] * len(search_terms))
        mc_params = [f"%{t.lower()}%" for t in search_terms]
        persons = await db.execute(
            f"""SELECT DISTINCT p.id, p.name_english FROM persons p
                JOIN modern_connections mc ON mc.person_id = p.id
                WHERE {mc_clauses} LIMIT 10""",
            tuple(mc_params)
        )

        return {
            "prophecies": [dict(r) for r in prophecies],
            "persons": [dict(r) for r in persons],
        }


map_service = MapService()
```

- [ ] **Step 2: Commit**

```bash
git add backend/services/map_service.py
git commit -m "feat(map): add map_service.py with kingdom, peoples, and search logic"
```

---

### Task 5: Add map API endpoints to main.py

**Files:**
- Modify: `backend/main.py`

- [ ] **Step 1: Add import**

At `backend/main.py` line 17 (after the search_service import), add:

```python
from backend.services.map_service import map_service
```

- [ ] **Step 2: Add map endpoints**

After the lineage endpoints (after line 301), before the Frontend section, add:

```python
# ── Map ────────────────────────────────────────────
@app.get("/api/map/eras")
async def map_eras():
    return {"eras": map_service.get_eras()}

@app.get("/api/map/kingdoms")
async def map_kingdoms():
    return {"kingdoms": map_service.get_kingdoms()}

@app.get("/api/map/era/{era_id}")
async def map_era(era_id: int):
    return map_service.get_era(era_id)

@app.get("/api/map/kingdom/{kingdom_id}")
async def map_kingdom(kingdom_id: int, era: int = None):
    result = map_service.get_kingdom(kingdom_id, era)
    if not result:
        return JSONResponse({"error": "Kingdom not found"}, status_code=404)
    # Add cross-references from DB
    kingdom = result["kingdom"]
    refs = await map_service.get_cross_references(
        db, kingdom["name"], kingdom.get("aliases", [])
    )
    result["related_prophecies"] = refs["prophecies"]
    result["related_persons"] = refs["persons"]
    return result

@app.get("/api/map/kingdom/{kingdom_id}/geojson")
async def map_kingdom_geojson(kingdom_id: int, era: int = Query(...)):
    geojson = map_service.get_kingdom_geojson(kingdom_id, era)
    if not geojson:
        return JSONResponse({"error": "GeoJSON not found"}, status_code=404)
    return geojson

@app.get("/api/map/peoples")
async def map_peoples():
    return {"peoples": map_service.get_peoples()}

@app.get("/api/map/people/{people_id}")
async def map_people(people_id: int):
    result = map_service.get_people(people_id)
    if not result:
        return JSONResponse({"error": "People not found"}, status_code=404)
    return result

@app.get("/api/map/search")
async def map_search(q: str = Query(..., min_length=2)):
    return map_service.search(q)
```

- [ ] **Step 3: Commit**

```bash
git add backend/main.py
git commit -m "feat(map): add /api/map/* endpoints for kingdoms, peoples, eras, search"
```

---

### Task 6: Update unified search to include map results

**Files:**
- Modify: `backend/services/search_service.py`

- [ ] **Step 1: Add map search to SearchService**

Replace the entire `search_service.py`:

```python
"""Unified search across Bible, lineage, prophecies, and map."""
from backend.services.map_service import map_service


class SearchService:

    async def search(self, db, query: str) -> dict:
        """Search across all data types."""
        q = f"%{query.lower()}%"

        bible = await db.execute(
            """SELECT book, chapter, verse, text FROM bible_kjv
               WHERE LOWER(text) LIKE ? LIMIT 10""", (q,))

        persons = await db.execute(
            """SELECT id, name_english, name_hebrew, name_meaning, generation
               FROM persons WHERE LOWER(name_english) LIKE ? LIMIT 10""", (q,))

        prophecies = await db.execute(
            """SELECT id, title, category, summary, status FROM prophecies
               WHERE LOWER(title) LIKE ? OR LOWER(fulfillment_text) LIKE ?
               OR LOWER(prophecy_text) LIKE ? LIMIT 10""", (q, q, q))

        # Map search (kingdoms, cities, peoples)
        map_results = map_service.search(query)

        return {
            "bible_verses": [dict(r) for r in bible],
            "persons": [dict(r) for r in persons],
            "prophecies": [dict(r) for r in prophecies],
            "map_kingdoms": map_results["kingdoms"],
            "map_cities": map_results["cities"],
            "map_peoples": map_results["peoples"],
        }


search_service = SearchService()
```

- [ ] **Step 2: Commit**

```bash
git add backend/services/search_service.py
git commit -m "feat(map): add map kingdoms/cities/peoples to unified search"
```

---

### Task 7: Add map_location to lineage and prophecy responses

**Files:**
- Modify: `backend/services/lineage_service.py`
- Modify: `backend/services/prophecy_service.py`

- [ ] **Step 1: Update lineage person response**

In `backend/services/lineage_service.py`, at the end of the `get_person` method (before the final `return`), add:

```python
        # Map location from modern_connections
        map_location = None
        if mc_rows:
            from backend.services.map_service import map_service
            for mc in mc_rows:
                region = dict(mc).get("region", "")
                if region:
                    results = map_service.search(region.split("(")[0].strip())
                    if results["kingdoms"]:
                        map_location = {
                            "kingdom_id": results["kingdoms"][0]["id"],
                            "kingdom_name": results["kingdoms"][0]["name"],
                        }
                        break
```

And add `"map_location": map_location` to the return dict.

- [ ] **Step 2: Update prophecy detail response**

In `backend/services/prophecy_service.py`, in the `get_prophecy` method, after building the response, add map location resolution by searching prophecy title/text against map kingdoms. Add `"map_location"` to the return dict.

- [ ] **Step 3: Commit**

```bash
git add backend/services/lineage_service.py backend/services/prophecy_service.py
git commit -m "feat(map): add map_location cross-references to lineage and prophecy responses"
```

---

## Chunk 2: Frontend — Map Tab Core

### Task 8: Add Leaflet CDN and Map tab HTML structure

**Files:**
- Modify: `frontend/index.html`

- [ ] **Step 1: Add Leaflet CDN links**

In the `<head>` section (after line 5, the viewport meta tag), add:

```html
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
```

- [ ] **Step 2: Add Map tab button**

At line 952 (after the Prophecy tab button), add:

```html
    <button class="tab-btn" id="tab-map" onclick="switchTab('map')">Map</button>
```

- [ ] **Step 3: Add Map tab content HTML**

After the prophecy tab content `</div>` (before the floating search div), add:

```html
  <!-- Map Tab -->
  <div class="tab-content" id="content-map">
    <div id="map-loading" class="empty-state">Loading map data...</div>
    <div id="map-view" style="display:none; position:relative;">
      <!-- Peoples filter sidebar -->
      <div id="map-peoples-filter" class="map-peoples-filter">
        <div class="map-peoples-header">
          <input class="map-peoples-search" id="map-peoples-search" placeholder="Filter peoples..." oninput="filterPeoplesList()">
        </div>
        <div class="map-peoples-list" id="map-peoples-list"></div>
        <button class="map-peoples-clear" id="map-peoples-clear" style="display:none;" onclick="clearPeoplesFilter()">Clear Filter</button>
      </div>
      <!-- Map container -->
      <div id="map-container" style="height:calc(100vh - 160px); width:100%;"></div>
      <!-- Era slider -->
      <div class="map-era-slider" id="map-era-slider">
        <input type="range" id="map-era-range" min="1" max="16" value="1" oninput="onEraSliderChange(this.value)">
        <div class="map-era-label" id="map-era-label">Table of Nations (~2200 BC)</div>
      </div>
      <!-- Narrative bar (for peoples filter) -->
      <div class="map-narrative" id="map-narrative" style="display:none;"></div>
      <!-- Event toast -->
      <div class="map-toast" id="map-toast" style="display:none;"></div>
      <!-- Legend -->
      <div class="map-legend">
        <div class="map-legend-item"><span class="legend-solid"></span> Documented boundaries</div>
        <div class="map-legend-item"><span class="legend-dotted"></span> Approximate territory</div>
      </div>
      <!-- Kingdom detail panel -->
      <div class="map-detail-panel" id="map-detail-panel" style="display:none;">
        <div id="map-detail-inner"></div>
      </div>
    </div>
  </div>
```

- [ ] **Step 4: Commit**

```bash
git add frontend/index.html
git commit -m "feat(map): add Map tab HTML structure with Leaflet CDN"
```

---

### Task 9: Add Map CSS

**Files:**
- Modify: `frontend/index.html`

- [ ] **Step 1: Add map-specific CSS**

Before the closing `</style>` tag (around line 943), add all map CSS:

```css
    /* ── Map Tab ──────────────────────────────────────── */
    #content-map { padding: 0; }

    .map-peoples-filter {
      position: absolute; top: 10px; left: 10px; z-index: 1000;
      background: rgba(26,15,10,0.95); border: 1px solid rgba(201,168,76,0.2);
      border-radius: 8px; width: 220px; max-height: calc(100vh - 200px);
      display: flex; flex-direction: column; overflow: hidden;
    }
    .map-peoples-header { padding: 8px; }
    .map-peoples-search {
      width: 100%; padding: 6px 10px; border-radius: 6px;
      background: rgba(201,168,76,0.08); border: 1px solid rgba(201,168,76,0.15);
      color: #f5f0e8; font-size: 0.8rem;
    }
    .map-peoples-search::placeholder { color: #6b5d4f; }
    .map-peoples-search:focus { outline: none; border-color: #c9a84c; }
    .map-peoples-list {
      overflow-y: auto; max-height: 300px; padding: 0 8px 8px;
    }
    .map-peoples-item {
      padding: 6px 8px; margin-bottom: 2px; border-radius: 4px; cursor: pointer;
      font-size: 0.78rem; color: #d4c5b0; transition: background 0.2s;
    }
    .map-peoples-item:hover { background: rgba(201,168,76,0.1); }
    .map-peoples-item.active { background: rgba(201,168,76,0.2); color: #c9a84c; }
    .map-peoples-item .peoples-ancestor { font-size: 0.68rem; color: #8a7a60; }
    .map-peoples-clear {
      margin: 8px; padding: 6px; border-radius: 6px; cursor: pointer;
      background: rgba(114,47,55,0.3); border: 1px solid rgba(114,47,55,0.4);
      color: #d4c5b0; font-size: 0.75rem;
    }
    .map-peoples-clear:hover { background: rgba(114,47,55,0.5); }

    .map-era-slider {
      position: absolute; bottom: 20px; left: 240px; right: 20px; z-index: 1000;
      background: rgba(26,15,10,0.9); border: 1px solid rgba(201,168,76,0.2);
      border-radius: 8px; padding: 10px 16px; text-align: center;
    }
    .map-era-slider input[type="range"] {
      width: 100%; accent-color: #c9a84c; cursor: pointer;
    }
    .map-era-label {
      font-size: 0.82rem; color: #c9a84c; margin-top: 4px; font-weight: 600;
    }

    .map-narrative {
      position: absolute; bottom: 80px; left: 240px; right: 20px; z-index: 1000;
      background: rgba(26,15,10,0.92); border: 1px solid rgba(201,168,76,0.2);
      border-radius: 8px; padding: 12px 16px;
      font-size: 0.8rem; color: #d4c5b0; line-height: 1.5;
    }
    .map-narrative strong { color: #c9a84c; }

    .map-toast {
      position: absolute; top: 10px; left: 50%; transform: translateX(-50%);
      z-index: 1001; background: rgba(26,15,10,0.95);
      border: 1px solid rgba(201,168,76,0.3); border-radius: 8px;
      padding: 8px 20px; font-size: 0.82rem; color: #c9a84c;
      font-weight: 600; white-space: nowrap; transition: opacity 0.5s;
    }

    .map-legend {
      position: absolute; bottom: 20px; left: 10px; z-index: 1000;
      background: rgba(26,15,10,0.9); border: 1px solid rgba(201,168,76,0.2);
      border-radius: 8px; padding: 8px 12px; font-size: 0.7rem; color: #8a7a60;
    }
    .map-legend-item { display: flex; align-items: center; gap: 6px; margin-bottom: 3px; }
    .legend-solid {
      display: inline-block; width: 20px; height: 3px;
      background: #c9a84c; border-radius: 2px;
    }
    .legend-dotted {
      display: inline-block; width: 20px; height: 3px;
      border-top: 2px dashed #c9a84c;
    }

    .map-detail-panel {
      position: absolute; top: 10px; right: 10px; z-index: 1000;
      width: 340px; max-height: calc(100vh - 200px); overflow-y: auto;
      background: rgba(26,15,10,0.95); border: 1px solid rgba(201,168,76,0.2);
      border-radius: 8px; padding: 16px;
    }
    .map-detail-panel .panel-close {
      position: absolute; top: 8px; right: 12px; background: none; border: none;
      color: #8a7a60; font-size: 1.2rem; cursor: pointer;
    }
    .map-detail-panel .panel-close:hover { color: #c9a84c; }
    .map-detail-name { font-size: 1.1rem; color: #f5f0e8; font-weight: 700; margin-bottom: 4px; }
    .map-detail-hebrew { font-size: 0.9rem; color: #c9a84c; margin-bottom: 8px; }
    .map-detail-meta { font-size: 0.75rem; color: #8a7a60; margin-bottom: 4px; }
    .map-detail-desc { font-size: 0.82rem; color: #d4c5b0; line-height: 1.5; margin: 10px 0; }
    .map-detail-section { margin-top: 12px; }
    .map-detail-section h4 { font-size: 0.78rem; color: #c9a84c; margin-bottom: 6px; text-transform: uppercase; }
    .map-detail-link {
      display: inline-block; padding: 3px 10px; margin: 2px; border-radius: 12px;
      background: rgba(201,168,76,0.1); border: 1px solid rgba(201,168,76,0.2);
      color: #d4c5b0; font-size: 0.75rem; cursor: pointer; transition: background 0.2s;
    }
    .map-detail-link:hover { background: rgba(201,168,76,0.2); color: #c9a84c; }
    .map-detail-explore {
      display: block; width: 100%; margin-top: 12px; padding: 8px;
      border-radius: 6px; background: rgba(114,47,55,0.3);
      border: 1px solid rgba(114,47,55,0.4); color: #d4c5b0;
      font-size: 0.8rem; cursor: pointer; text-align: center;
    }
    .map-detail-explore:hover { background: rgba(114,47,55,0.5); }
    .map-detail-accuracy {
      display: inline-block; padding: 2px 8px; border-radius: 10px;
      font-size: 0.68rem; margin-bottom: 8px;
    }
    .map-detail-accuracy.documented { background: rgba(201,168,76,0.15); color: #c9a84c; }
    .map-detail-accuracy.approximate { background: rgba(114,47,55,0.2); color: #b0836b; }

    .map-viewon-btn {
      display: inline-flex; align-items: center; gap: 4px; padding: 4px 10px;
      border-radius: 12px; background: rgba(201,168,76,0.1);
      border: 1px solid rgba(201,168,76,0.2); color: #c9a84c;
      font-size: 0.72rem; cursor: pointer; margin-top: 6px;
    }
    .map-viewon-btn:hover { background: rgba(201,168,76,0.2); }

    /* Mini-map in search results */
    .search-minimap {
      width: 100%; height: 250px; border-radius: 6px; margin-top: 8px;
      border: 1px solid rgba(201,168,76,0.15);
    }

    /* Mobile */
    @media (max-width: 768px) {
      .map-peoples-filter {
        position: relative; top: 0; left: 0; width: 100%;
        max-height: none; border-radius: 0; border: none;
        border-bottom: 1px solid rgba(201,168,76,0.2);
      }
      .map-peoples-list { max-height: 120px; }
      .map-era-slider { left: 10px; bottom: 10px; }
      .map-narrative { left: 10px; bottom: 70px; }
      .map-detail-panel {
        position: fixed; top: auto; bottom: 0; left: 0; right: 0;
        width: 100%; max-height: 60vh; border-radius: 16px 16px 0 0;
      }
      .map-legend { bottom: 80px; }
      .map-landscape-hint {
        display: block; text-align: center; padding: 8px;
        background: rgba(201,168,76,0.1); color: #c9a84c;
        font-size: 0.75rem; border-bottom: 1px solid rgba(201,168,76,0.15);
      }
    }
    @media (min-width: 769px) {
      .map-landscape-hint { display: none; }
    }
```

- [ ] **Step 2: Commit**

```bash
git add frontend/index.html
git commit -m "feat(map): add Map tab CSS with dark/gold theme"
```

---

### Task 10: Add Map JavaScript — initialization and era slider

**Files:**
- Modify: `frontend/index.html`

- [ ] **Step 1: Update state object**

At line ~1031, add map state properties to the state object:

```javascript
    mapLoaded: false,
    mapInstance: null,
    mapData: null,
    mapEras: [],
    mapLayers: {},
    mapCityMarkers: [],
    mapGeoJsonCache: {},
    selectedKingdom: null,
    selectedEra: 1,
    selectedPeople: null,
    peoplesData: [],
    miniMap: null,
```

- [ ] **Step 2: Update switchTab() function**

At line ~1076, add `'map'` to the tab list array. Also add map lazy loading and width adjustment:

```javascript
  function switchTab(tab) {
    state.activeTab = tab;
    ['trials', 'guidance', 'ask', 'lineage', 'prophecy', 'map'].forEach(function(t) {
      $('tab-' + t).className = 'tab-btn' + (t === tab ? ' active' : '');
      $('content-' + t).className = 'tab-content' + (t === tab ? ' active' : '');
    });
    if (tab === 'trials') loadCategories('trial');
    if (tab === 'guidance') loadCategories('guidance');
    if (tab === 'lineage' && !state.lineageLoaded) loadLineage();
    if (tab === 'prophecy' && !state.prophecyLoaded) loadProphecyTimeline();
    if (tab === 'map' && !state.mapLoaded) loadMap();
    document.querySelector('.app').style.maxWidth = (tab === 'lineage' || tab === 'prophecy' || tab === 'map') ? '100%' : '900px';
  }
```

- [ ] **Step 3: Add map initialization function**

Add after the prophecy functions, before the `init()` function:

```javascript
  // ── Map Tab ────────────────────────────────────────
  var MAP_TILE_URL = 'https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png';
  var MAP_TILE_ATTR = '&copy; OpenStreetMap contributors &copy; CARTO';

  async function loadMap() {
    try {
      var eraData = await apiFetch('/api/map/eras');
      state.mapEras = eraData.eras || [];

      var peoplesData = await apiFetch('/api/map/peoples');
      state.peoplesData = peoplesData.peoples || [];

      state.mapLoaded = true;
      $('map-loading').style.display = 'none';
      $('map-view').style.display = 'block';

      // Initialize Leaflet
      state.mapInstance = L.map('map-container', {
        center: [31.5, 35.0],
        zoom: 4,
        minZoom: 2,
        maxZoom: 10,
        zoomControl: true,
      });

      L.tileLayer(MAP_TILE_URL, {
        attribution: MAP_TILE_ATTR,
        subdomains: 'abcd',
        maxZoom: 19,
      }).addTo(state.mapInstance);

      // Apply dark/parchment filter to tiles
      var tilePane = state.mapInstance.getPane('tilePane');
      if (tilePane) {
        tilePane.style.filter = 'sepia(40%) saturate(60%) brightness(70%) hue-rotate(10deg)';
      }

      // Setup era slider
      var slider = $('map-era-range');
      slider.max = state.mapEras.length;
      slider.value = 1;
      updateEraLabel(1);

      // Render peoples filter
      renderPeoplesList(state.peoplesData);

      // Load first era
      await loadEra(1);
    } catch (err) {
      $('map-loading').innerHTML = '<div class="empty-state">Failed to load map data. <button onclick="loadMap()">Retry</button></div>';
    }
  }

  function updateEraLabel(eraId) {
    var era = state.mapEras.find(function(e) { return e.id === eraId; });
    if (era) {
      $('map-era-label').textContent = era.name + ' (' + era.date_approx + ')';
    }
  }

  async function onEraSliderChange(value) {
    var eraId = parseInt(value);
    if (eraId === state.selectedEra) return;
    var prevEra = state.selectedEra;
    state.selectedEra = eraId;
    updateEraLabel(eraId);
    await loadEra(eraId, prevEra);
  }
```

- [ ] **Step 4: Commit**

```bash
git add frontend/index.html
git commit -m "feat(map): add Map JS initialization, Leaflet setup, era slider"
```

---

### Task 11: Add Map JavaScript — era loading and kingdom rendering

**Files:**
- Modify: `frontend/index.html`

- [ ] **Step 1: Add era loading and polygon rendering**

Continue adding after the previous map functions:

```javascript
  async function loadEra(eraId, prevEraId) {
    // Check cache
    if (!state.mapGeoJsonCache[eraId]) {
      var data = await apiFetch('/api/map/era/' + eraId);
      state.mapGeoJsonCache[eraId] = data;
    }
    var data = state.mapGeoJsonCache[eraId];

    // Show toast
    if (data.era) {
      showMapToast(data.era.date_approx + ' — ' + data.era.name + ' — ' + data.era.scripture_ref);
    }

    // Clear existing layers
    Object.keys(state.mapLayers).forEach(function(key) {
      state.mapInstance.removeLayer(state.mapLayers[key]);
    });
    state.mapLayers = {};
    state.mapCityMarkers.forEach(function(m) { state.mapInstance.removeLayer(m); });
    state.mapCityMarkers = [];

    // Draw kingdoms
    (data.kingdoms || []).forEach(function(k) {
      if (!k.geojson) return;
      var isDotted = k.border_accuracy === 'approximate';
      var layer = L.geoJSON(k.geojson, {
        style: {
          color: '#c9a84c',
          weight: isDotted ? 1.5 : 2,
          opacity: 0.8,
          fillColor: '#c9a84c',
          fillOpacity: 0.1,
          dashArray: isDotted ? '6 4' : null,
        },
      });
      layer.kingdomId = k.id;
      layer.kingdomData = k;
      layer.on('click', function() { selectKingdom(k.id); });
      layer.bindTooltip(k.name, {
        permanent: false, direction: 'center',
        className: 'map-kingdom-tooltip',
      });
      layer.addTo(state.mapInstance);
      state.mapLayers['kingdom-' + k.id] = layer;
    });

    // Draw major cities
    (data.cities || []).filter(function(c) { return c.is_major; }).forEach(function(c) {
      var marker = L.circleMarker([c.lat, c.lng], {
        radius: c.is_capital ? 6 : 4,
        color: '#f5f0e8',
        fillColor: c.is_capital ? '#c9a84c' : '#8a7a60',
        fillOpacity: 0.9,
        weight: 1,
      });
      marker.bindTooltip(c.name, { permanent: false, direction: 'top', className: 'map-city-tooltip' });
      marker.addTo(state.mapInstance);
      state.mapCityMarkers.push(marker);
    });

    // Apply peoples filter if active
    if (state.selectedPeople) {
      applyPeoplesFilter(state.selectedPeople);
    }

    // Update narrative if peoples filter active
    updateNarrative(eraId);
  }

  function showMapToast(text) {
    var toast = $('map-toast');
    toast.textContent = text;
    toast.style.display = 'block';
    toast.style.opacity = '1';
    setTimeout(function() {
      toast.style.opacity = '0';
      setTimeout(function() { toast.style.display = 'none'; }, 500);
    }, 3000);
  }
```

- [ ] **Step 2: Commit**

```bash
git add frontend/index.html
git commit -m "feat(map): add era loading, kingdom polygon rendering, city markers"
```

---

### Task 12: Add Map JavaScript — kingdom selection and detail panel

**Files:**
- Modify: `frontend/index.html`

- [ ] **Step 1: Add kingdom selection with focus behavior**

```javascript
  async function selectKingdom(kingdomId) {
    state.selectedKingdom = kingdomId;

    // Fade all other kingdoms to 20% opacity
    Object.keys(state.mapLayers).forEach(function(key) {
      var layer = state.mapLayers[key];
      if (layer.kingdomId === kingdomId) {
        layer.setStyle({ fillOpacity: 0.25, opacity: 1, color: '#c9a84c', weight: 3 });
        state.mapInstance.fitBounds(layer.getBounds(), { padding: [50, 50] });
      } else {
        layer.setStyle({ fillOpacity: 0.02, opacity: 0.2 });
      }
    });

    // Show all cities in this kingdom (not just major ones)
    var eraData = state.mapGeoJsonCache[state.selectedEra];
    if (eraData) {
      // Remove old city markers
      state.mapCityMarkers.forEach(function(m) { state.mapInstance.removeLayer(m); });
      state.mapCityMarkers = [];

      (eraData.cities || []).forEach(function(c) {
        if (c.current_kingdom_id === kingdomId || c.is_major) {
          var isThisKingdom = c.current_kingdom_id === kingdomId;
          var marker = L.circleMarker([c.lat, c.lng], {
            radius: c.is_capital ? 6 : 4,
            color: isThisKingdom ? '#f5f0e8' : '#555',
            fillColor: isThisKingdom ? (c.is_capital ? '#c9a84c' : '#8a7a60') : '#444',
            fillOpacity: isThisKingdom ? 0.9 : 0.2,
            weight: 1,
          });
          marker.bindTooltip(c.name, { permanent: isThisKingdom, direction: 'top', className: 'map-city-tooltip' });
          marker.addTo(state.mapInstance);
          state.mapCityMarkers.push(marker);
        }
      });
    }

    // Load detail panel
    await loadKingdomDetail(kingdomId);
  }

  function deselectKingdom() {
    state.selectedKingdom = null;
    $('map-detail-panel').style.display = 'none';
    // Restore all kingdoms to normal opacity
    Object.keys(state.mapLayers).forEach(function(key) {
      var layer = state.mapLayers[key];
      var isDotted = layer.kingdomData && layer.kingdomData.border_accuracy === 'approximate';
      layer.setStyle({
        fillOpacity: 0.1, opacity: 0.8, color: '#c9a84c',
        weight: isDotted ? 1.5 : 2,
      });
    });
    // Reload era to reset city markers
    loadEra(state.selectedEra);
  }

  async function loadKingdomDetail(kingdomId) {
    var panel = $('map-detail-panel');
    var inner = $('map-detail-inner');
    panel.style.display = 'block';
    inner.innerHTML = '<div class="empty-state">Loading...</div>';

    try {
      var data = await apiFetch('/api/map/kingdom/' + kingdomId + '?era=' + state.selectedEra);
      var k = data.kingdom;
      var html = '<button class="panel-close" onclick="deselectKingdom()">&times;</button>';

      html += '<div class="map-detail-name">' + k.name + '</div>';
      if (k.name_hebrew) html += '<div class="map-detail-hebrew">' + k.name_hebrew + '</div>';
      html += '<span class="map-detail-accuracy ' + k.border_accuracy + '">' + k.border_accuracy + ' boundaries</span>';
      html += '<div class="map-detail-meta">Ancestor: ' + (k.ancestor || 'N/A') + ' (' + (k.ancestor_ref || '') + ')</div>';
      html += '<div class="map-detail-meta">Capital: ' + (k.capital || 'N/A') + '</div>';
      html += '<div class="map-detail-meta">Modern region: ' + (k.modern_region || 'N/A') + '</div>';
      html += '<div class="map-detail-desc">' + (k.description || '') + '</div>';

      // Scripture refs
      if (k.scripture_refs && k.scripture_refs.length) {
        html += '<div class="map-detail-section"><h4>Key Scriptures</h4>';
        k.scripture_refs.forEach(function(ref) {
          html += '<span class="map-detail-link">' + ref + '</span>';
        });
        html += '</div>';
      }

      // Related prophecies
      if (data.related_prophecies && data.related_prophecies.length) {
        html += '<div class="map-detail-section"><h4>Related Prophecies</h4>';
        data.related_prophecies.forEach(function(p) {
          html += '<span class="map-detail-link" onclick="switchTab(\'prophecy\')">' + p.title + '</span>';
        });
        html += '</div>';
      }

      // Related lineage persons
      if (data.related_persons && data.related_persons.length) {
        html += '<div class="map-detail-section"><h4>Lineage Connections</h4>';
        data.related_persons.forEach(function(p) {
          html += '<span class="map-detail-link" onclick="switchTab(\'lineage\'); setTimeout(function(){openPersonPanel(' + p.id + ')},500);">' + p.name_english + '</span>';
        });
        html += '</div>';
      }

      // Cities
      if (data.cities && data.cities.length) {
        html += '<div class="map-detail-section"><h4>Cities (' + data.cities.length + ')</h4>';
        data.cities.forEach(function(c) {
          html += '<span class="map-detail-link">' + c.name + '</span>';
        });
        html += '</div>';
      }

      // Scholarly context (explore further)
      if (k.scholarly_context) {
        html += '<button class="map-detail-explore" onclick="this.nextElementSibling.style.display=\'block\'; this.style.display=\'none\';">Explore Further</button>';
        html += '<div style="display:none;"><div class="map-detail-section"><h4>Scholarly Context</h4>';
        html += '<div class="map-detail-desc">' + k.scholarly_context + '</div></div></div>';
      }

      inner.innerHTML = html;
    } catch (err) {
      inner.innerHTML = '<div class="empty-state">Failed to load kingdom details.</div>';
    }
  }
```

- [ ] **Step 2: Commit**

```bash
git add frontend/index.html
git commit -m "feat(map): add kingdom selection, focus/fade behavior, detail panel"
```

---

### Task 13: Add Map JavaScript — peoples filter

**Files:**
- Modify: `frontend/index.html`

- [ ] **Step 1: Add peoples filter functions**

```javascript
  function renderPeoplesList(peoples) {
    var html = '';
    peoples.forEach(function(p) {
      html += '<div class="map-peoples-item" data-id="' + p.id + '" onclick="selectPeople(' + p.id + ')">';
      html += '<div>' + p.modern_name + '</div>';
      html += '<div class="peoples-ancestor">' + p.biblical_ancestor + ' — ' + p.ancestor_ref + '</div>';
      html += '</div>';
    });
    $('map-peoples-list').innerHTML = html;
  }

  function filterPeoplesList() {
    var query = $('map-peoples-search').value.toLowerCase();
    var items = document.querySelectorAll('.map-peoples-item');
    items.forEach(function(item) {
      var text = item.textContent.toLowerCase();
      item.style.display = text.indexOf(query) >= 0 ? 'block' : 'none';
    });
  }

  async function selectPeople(peopleId) {
    var people = state.peoplesData.find(function(p) { return p.id === peopleId; });
    if (!people) return;

    state.selectedPeople = people;
    $('map-peoples-clear').style.display = 'block';

    // Highlight in sidebar
    document.querySelectorAll('.map-peoples-item').forEach(function(item) {
      item.classList.toggle('active', parseInt(item.dataset.id) === peopleId);
    });

    // Apply filter to map
    applyPeoplesFilter(people);
    updateNarrative(state.selectedEra);
  }

  function applyPeoplesFilter(people) {
    var kingdomIds = people.kingdom_ids || [];
    Object.keys(state.mapLayers).forEach(function(key) {
      var layer = state.mapLayers[key];
      if (kingdomIds.indexOf(layer.kingdomId) >= 0) {
        layer.setStyle({ fillOpacity: 0.25, opacity: 1, color: '#c9a84c', weight: 3 });
      } else {
        layer.setStyle({ fillOpacity: 0.02, opacity: 0.2 });
      }
    });
  }

  function updateNarrative(eraId) {
    var narrative = $('map-narrative');
    if (!state.selectedPeople) {
      narrative.style.display = 'none';
      return;
    }
    var people = state.selectedPeople;
    var eraNarrative = (people.era_narratives || []).find(function(n) { return n.era_id === eraId; });
    if (eraNarrative) {
      narrative.innerHTML = '<strong>' + people.modern_name + ' (' + people.biblical_ancestor + ')</strong><br>' + eraNarrative.text;
      narrative.style.display = 'block';
    } else {
      narrative.innerHTML = '<strong>' + people.modern_name + ' (' + people.biblical_ancestor + ')</strong><br><em>No specific narrative for this era.</em>';
      narrative.style.display = 'block';
    }
  }

  function clearPeoplesFilter() {
    state.selectedPeople = null;
    $('map-peoples-clear').style.display = 'none';
    $('map-narrative').style.display = 'none';
    document.querySelectorAll('.map-peoples-item').forEach(function(item) {
      item.classList.remove('active');
    });
    // Restore all kingdoms
    Object.keys(state.mapLayers).forEach(function(key) {
      var layer = state.mapLayers[key];
      var isDotted = layer.kingdomData && layer.kingdomData.border_accuracy === 'approximate';
      layer.setStyle({
        fillOpacity: 0.1, opacity: 0.8, color: '#c9a84c',
        weight: isDotted ? 1.5 : 2,
      });
    });
  }
```

- [ ] **Step 2: Commit**

```bash
git add frontend/index.html
git commit -m "feat(map): add peoples filter with sidebar, narrative bar, highlight behavior"
```

---

## Chunk 3: Integration & Polish

### Task 14: Add mini-map to unified search results

**Files:**
- Modify: `frontend/index.html`

- [ ] **Step 1: Update submitLookup() to render map results**

In the `submitLookup()` function (around line 1630), after the prophecies rendering block, add:

```javascript
      // Map kingdoms from search
      if (data.map_kingdoms && data.map_kingdoms.length) {
        html += '<div style="margin-bottom:12px;">';
        html += '<div style="font-size:0.78rem;color:#8a7a60;font-weight:700;margin-bottom:6px;">MAP — KINGDOMS</div>';
        data.map_kingdoms.forEach(function(k) {
          html += '<span class="panel-link-item" onclick="switchTab(\'map\'); setTimeout(function(){ selectKingdom(' + k.id + '); },800);">' + k.name + '</span>';
        });
        html += '</div>';
      }

      // Map cities from search
      if (data.map_cities && data.map_cities.length) {
        html += '<div style="margin-bottom:12px;">';
        html += '<div style="font-size:0.78rem;color:#8a7a60;font-weight:700;margin-bottom:6px;">MAP — CITIES</div>';
        data.map_cities.forEach(function(c) {
          html += '<span class="panel-link-item" onclick="switchTab(\'map\');">' + c.name + '</span>';
        });
        html += '</div>';
      }

      // Map peoples from search
      if (data.map_peoples && data.map_peoples.length) {
        html += '<div style="margin-bottom:12px;">';
        html += '<div style="font-size:0.78rem;color:#8a7a60;font-weight:700;margin-bottom:6px;">MAP — PEOPLES</div>';
        data.map_peoples.forEach(function(p) {
          html += '<span class="panel-link-item" onclick="switchTab(\'map\'); setTimeout(function(){ selectPeople(' + p.id + '); },800);">' + p.modern_name + ' (' + p.biblical_ancestor + ')</span>';
        });
        html += '</div>';
      }

      // Mini-map for first map result
      if ((data.map_kingdoms && data.map_kingdoms.length) || (data.map_cities && data.map_cities.length)) {
        html += '<div id="search-minimap-container" class="search-minimap"></div>';
        setTimeout(function() {
          var container = document.getElementById('search-minimap-container');
          if (!container) return;
          if (state.miniMap) { state.miniMap.remove(); state.miniMap = null; }
          var firstCity = (data.map_cities && data.map_cities.length) ? data.map_cities[0] : null;
          var center = firstCity ? [firstCity.lat, firstCity.lng] : [31.5, 35.0];
          var zoom = firstCity ? 6 : 4;
          state.miniMap = L.map(container, { center: center, zoom: zoom, zoomControl: false, attributionControl: false });
          L.tileLayer(MAP_TILE_URL, { subdomains: 'abcd' }).addTo(state.miniMap);
          var pane = state.miniMap.getPane('tilePane');
          if (pane) pane.style.filter = 'sepia(40%) saturate(60%) brightness(70%) hue-rotate(10deg)';
          if (firstCity) {
            L.circleMarker([firstCity.lat, firstCity.lng], {
              radius: 8, color: '#c9a84c', fillColor: '#c9a84c', fillOpacity: 0.6,
            }).addTo(state.miniMap).bindTooltip(firstCity.name, { permanent: true, direction: 'top' });
          }
        }, 100);
      }
```

- [ ] **Step 2: Commit**

```bash
git add frontend/index.html
git commit -m "feat(map): add map results and mini-map to unified search"
```

---

### Task 15: Add "View on Map" buttons to lineage and prophecy panels

**Files:**
- Modify: `frontend/index.html`

- [ ] **Step 1: Add "View on Map" to lineage person panel**

In the `openPersonPanel()` function, after the modern_connections rendering (around line 1390), add:

```javascript
      // View on Map button
      if (data.map_location) {
        html += '<div style="margin-top:10px;">';
        html += '<button class="map-viewon-btn" onclick="switchTab(\'map\'); setTimeout(function(){ selectKingdom(' + data.map_location.kingdom_id + '); },800);">View on Map &rarr; ' + data.map_location.kingdom_name + '</button>';
        html += '</div>';
      }
```

- [ ] **Step 2: Add "Show on Map" to prophecy detail**

In the prophecy detail rendering function, add a similar "Show on Map" button when `map_location` is present.

- [ ] **Step 3: Commit**

```bash
git add frontend/index.html
git commit -m "feat(map): add 'View on Map' buttons to lineage and prophecy panels"
```

---

### Task 16: Add tests

**Files:**
- Create: `tests/conftest.py`
- Create: `tests/test_map_service.py`
- Modify: `backend/requirements.txt`

- [ ] **Step 1: Add test dependencies**

Add to `backend/requirements.txt`:
```
pytest
pytest-asyncio
```

- [ ] **Step 2: Create conftest.py**

```python
"""Shared test fixtures."""
import pytest


@pytest.fixture
def map_service():
    from backend.services.map_service import MapService
    svc = MapService()
    svc._load_data()
    return svc
```

- [ ] **Step 3: Create test_map_service.py**

```python
"""Tests for map_service."""


def test_get_eras_returns_16_eras(map_service):
    eras = map_service.get_eras()
    assert len(eras) == 16
    assert eras[0]["name"] == "Table of Nations"
    assert eras[-1]["name"] == "Early Church"


def test_get_kingdoms_returns_list(map_service):
    kingdoms = map_service.get_kingdoms()
    assert len(kingdoms) > 0
    assert all("name" in k for k in kingdoms)
    assert all("boundaries" in k for k in kingdoms)


def test_get_era_filters_active_kingdoms(map_service):
    result = map_service.get_era(7)  # United Kingdom era
    assert result["era"] is not None
    assert result["era"]["name"] == "United Kingdom"
    kingdom_names = [k["name"] for k in result["kingdoms"]]
    assert "Egypt" in kingdom_names  # Egypt exists in all eras


def test_get_era_invalid_returns_empty(map_service):
    result = map_service.get_era(999)
    assert result["era"] is None
    assert result["kingdoms"] == []


def test_search_finds_by_name(map_service):
    result = map_service.search("Egypt")
    assert len(result["kingdoms"]) > 0
    assert result["kingdoms"][0]["name"] == "Egypt"


def test_search_finds_by_alias(map_service):
    result = map_service.search("Mitzrayim")
    assert len(result["kingdoms"]) > 0


def test_search_finds_peoples(map_service):
    result = map_service.search("Armenian")
    assert len(result["peoples"]) > 0


def test_get_peoples_returns_list(map_service):
    peoples = map_service.get_peoples()
    assert len(peoples) > 0
    assert all("modern_name" in p for p in peoples)
    assert all("era_narratives" in p for p in peoples)


def test_get_people_returns_detail(map_service):
    people = map_service.get_people(1)
    assert people is not None
    assert "modern_name" in people
    assert "era_narratives" in people


def test_get_people_invalid_returns_none(map_service):
    assert map_service.get_people(999) is None


def test_get_kingdom_returns_detail(map_service):
    result = map_service.get_kingdom(1)
    assert result is not None
    assert "kingdom" in result
    assert "cities" in result
```

- [ ] **Step 4: Run tests**

```bash
cd C:/AI/MGC_Workbench/apps/trialsofjudah
python -m pytest tests/ -v
```

Expected: All tests PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/ backend/requirements.txt
git commit -m "test(map): add map_service unit tests"
```

---

### Task 17: Final integration test — start the app

- [ ] **Step 1: Delete the database to force full re-seed**

The lineage and prophecy tables were already cleared. Delete the DB entirely to ensure clean state:

```bash
rm backend/data/trialsofjudah.db
```

- [ ] **Step 2: Start the app**

```bash
cd C:/AI/MGC_Workbench/apps/trialsofjudah
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8202 --reload
```

- [ ] **Step 3: Verify in browser**

Open `http://localhost:8202` and test:
1. Map tab loads with Leaflet map
2. Era slider changes kingdom boundaries
3. Clicking a kingdom fades others, shows detail panel
4. Peoples filter highlights specific people's history
5. Search bar returns map results with mini-map
6. Lineage "View on Map" button works
7. Lineage shows full tree from Adam to Jesus (re-seeded)
8. Search bar returns results with LLM commentary (Mixtral)

- [ ] **Step 4: Commit any fixes**

```bash
git add -A
git commit -m "fix(map): integration fixes from manual testing"
```

---

## Task Summary

| Task | Description | Chunk |
|------|-------------|-------|
| 1 | Create kingdoms.json (eras, kingdoms, cities) | 1 |
| 2 | Create GeoJSON boundary files | 1 |
| 3 | Create peoples.json | 1 |
| 4 | Create map_service.py | 1 |
| 5 | Add map API endpoints to main.py | 1 |
| 6 | Update unified search with map results | 1 |
| 7 | Add map_location to lineage/prophecy responses | 1 |
| 8 | Add Leaflet CDN and Map tab HTML | 2 |
| 9 | Add Map CSS | 2 |
| 10 | Add Map JS — init and era slider | 2 |
| 11 | Add Map JS — era loading and rendering | 2 |
| 12 | Add Map JS — kingdom selection and detail panel | 2 |
| 13 | Add Map JS — peoples filter | 2 |
| 14 | Add mini-map to search results | 3 |
| 15 | Add "View on Map" buttons | 3 |
| 16 | Add tests | 3 |
| 17 | Final integration test | 3 |
