# Evidence Pins — Design Spec

## Overview

Add an evidence layer to the Biblical Kingdoms Map showing 200+ archaeological discoveries, cross-cultural records, and inscriptions/artifacts plotted at their geographic locations. Pins radiate connection lines to the biblical event they confirm when clicked. Integrated with the era slider and filterable by category.

## Pin Categories

### Archaeological (amber pins)
~40-50 entries. Physical discoveries confirming biblical accounts.
Examples: Dead Sea Scrolls, Cyrus Cylinder, Merneptah Stele, Tel Dan Stele, walls of Jericho, Hezekiah's Tunnel, Pilate Stone, Pool of Siloam, Tall el-Hammam (Sodom), Noah's Ark site (Ararat).

### Cross-Cultural Records (teal pins)
~100-135 entries. Ancient texts from non-Israelite nations corroborating biblical events.

**Flood narratives (~50-60):** Chinese (Nu Wa), Sumerian (Gilgamesh/Ziusudra), Hindu (Manu), Greek (Deucalion), Aboriginal Australian, Native American (Hopi, Cree, Aztec, Inca, etc.), African (Yoruba, Maasai), Pacific Islander (Hawaiian, Maori), Mesopotamian, Egyptian, Persian, and dozens more.

**Creation narratives (~15-20):** Egyptian (Atum/Ptah), Sumerian (Enuma Elish), Chinese (Pan Gu), Hindu (Brahma), Norse (Ymir), Mayan (Popol Vuh), Polynesian, Aboriginal Dreamtime, Yoruba, Aztec — many share a single creator, primordial void, creation by word/speech.

**Tower of Babel / Language dispersion (~10-15):** Sumerian "Enmerkar and the Lord of Aratta," Mayan Popol Vuh (language confusion), Australian Aboriginal, African Wa-Sania, Greek Hermes myth, Hindu Vedic traditions.

**Plague/Exodus parallels (~5-8):** Ipuwer Papyrus, Ahmose Tempest Stele, El Arish Shrine text, Manetho's account, Hecataeus of Abdera's account.

**Destruction by fire from heaven (~5-8):** Sodom parallels in Sumerian texts, Tall el-Hammam airburst evidence, Greek Phaethon myth, Hindu Mahabharata descriptions.

**Patriarch/long lifespan traditions (~5-8):** Sumerian King List (pre-flood kings with impossibly long reigns matching Genesis 5 pattern), Chinese legendary emperors, Hindu Yugas with declining lifespans.

**Solar/cosmic events (~5-8):** Chinese records of Joshua's long day (~1400 BC), Mesoamerican "long night" accounts, Egyptian eclipse records, Roman historians on crucifixion darkness (Thallus, Phlegon).

**Messianic/divine sacrifice traditions (~5-8):** Hindu Prajapati (self-sacrificing creator), Aztec Quetzalcoatl (promised return), Chinese ShangDi (supreme deity with lamb sacrifice), Egyptian Osiris resurrection motif.

### Inscriptions & Artifacts (green pins)
~30-40 entries. Specific objects with text/imagery confirming scripture.
Examples: Moabite Stone (Mesha Stele), Black Obelisk of Shalmaneser, Siloam Inscription, Nazareth Inscription, James Ossuary, Pontius Pilate ring, Ketef Hinnom silver scrolls, Lachish Letters, LMLK seals, Nebo-Sarsekim tablet.

## Data Structure

New file: `backend/data/evidence.json`

```json
{
  "biblical_events": [
    {
      "id": "great_flood",
      "name": "The Great Flood",
      "lat": 39.7,
      "lng": 44.3,
      "scripture_refs": ["Genesis 6:5-8:22"],
      "description": "God destroyed the earth with a flood, saving only Noah and his family."
    },
    {
      "id": "creation",
      "name": "Creation",
      "lat": null,
      "lng": null,
      "scripture_refs": ["Genesis 1:1-2:3"],
      "description": "God created the heavens and the earth."
    },
    {
      "id": "tower_of_babel",
      "name": "Tower of Babel",
      "lat": 32.54,
      "lng": 44.42,
      "scripture_refs": ["Genesis 11:1-9"],
      "description": "God confounded the languages and scattered the peoples."
    }
  ],
  "evidence": [
    {
      "id": "gilgamesh_flood",
      "name": "Epic of Gilgamesh — Flood Tablet",
      "type": "cross_cultural",
      "category": "flood",
      "lat": 36.36,
      "lng": 43.15,
      "coordinate_type": "exact",
      "era_start": "table_of_nations",
      "era_end": "table_of_nations",
      "biblical_event_id": "great_flood",
      "scripture_refs": ["Genesis 6:5-8:22"],
      "description": "The eleventh tablet of the Epic of Gilgamesh, discovered at Nineveh, contains a flood narrative remarkably parallel to Genesis: a divine warning, an ark built to specific dimensions, animals taken aboard, a flood that destroys all life, the ark landing on a mountain, and birds sent out to test the waters.",
      "scholarly_detail": "Discovered by Hormuzd Rassam in the library of Ashurbanipal at Nineveh (1853). The flood tablet (Tablet XI) was translated by George Smith in 1872, causing a sensation. The Sumerian original (Ziusudra narrative) predates it by centuries. Housed in the British Museum, London.",
      "reliability": "confirmed",
      "culture": "Sumerian / Babylonian",
      "museum": "British Museum, London",
      "date_discovered": "1853"
    },
    {
      "id": "aboriginal_flood",
      "name": "Aboriginal Australian Flood Narrative",
      "type": "cross_cultural",
      "category": "flood",
      "lat": -25.0,
      "lng": 134.0,
      "coordinate_type": "cultural_region",
      "era_start": "table_of_nations",
      "era_end": "table_of_nations",
      "biblical_event_id": "great_flood",
      "scripture_refs": ["Genesis 6:5-8:22"],
      "description": "Multiple Aboriginal Australian peoples preserve oral traditions of a great flood that covered the land...",
      "scholarly_detail": "Documented by ethnographers in the 19th and 20th centuries...",
      "reliability": "confirmed",
      "culture": "Aboriginal Australian",
      "museum": null,
      "date_discovered": null
    }
  ]
}
```

### Key Data Design Decisions

**String IDs** (`"gilgamesh_flood"`) instead of integers, consistent with kingdoms.json pattern.

**`biblical_event_id`** references entries in the `biblical_events` array — a stable machine-readable key for grouping connections. The `biblical_events` array serves as a lookup table for event names, canonical coordinates, and scripture refs.

**`era_start` / `era_end`** instead of single `era_id` — evidence that spans multiple eras (e.g., Dead Sea Scrolls relevant from Persian through Roman period) uses a range, matching the kingdom boundary pattern.

**`coordinate_type`**: `"exact"` for archaeological sites with precise dig locations, `"cultural_region"` for traditions associated with a people/region rather than a specific site. Cultural region pins render as slightly larger translucent circles (8px, 60% opacity) vs exact pins (5px, 90% opacity) to visually communicate the difference.

**Canonical event coordinates**: The `biblical_events` array stores the "origin point" for connection lines. Events with no specific location (Creation) use `null` coordinates — connection lines for these events radiate from the center of the current map view instead of a fixed point.

**`date_discovered`** is display-only (string), never used for sorting or filtering.

## Connection Lines

When a user clicks a pin:
1. The pin's popup opens with full detail
2. A "Show Connections" button appears (for pins with `biblical_event_id`)
3. Clicking it:
   - Looks up the `biblical_event_id` in the `biblical_events` array for the canonical coordinates
   - Finds all other evidence entries with the same `biblical_event_id`
   - Draws animated dashed lines from the event coordinates to each pin
   - Lines animate outward (radiate) from the event location
   - A count badge shows: "47 cultures recorded this event"
   - For events with `null` coordinates, lines radiate from the center of the current map view
4. Click "Hide Connections" or click elsewhere to clear lines

## Pin Visuals

| Type | Color | Shape | Size |
|------|-------|-------|------|
| Archaeological | Amber (#D4880F) | Filled circle | 5px (exact) / 8px (region) |
| Cross-Cultural | Teal (#0097A7) | Filled circle | 5px (exact) / 8px (region) |
| Inscription | Green (#2E7D32) | Filled circle | 5px (exact) / 8px (region) |

- White border (1.5px) for visibility against terrain
- `coordinate_type: "cultural_region"` pins: 8px radius, 60% fill opacity (translucent)
- `coordinate_type: "exact"` pins: 5px radius, 90% fill opacity (solid)
- Relevant to current era: full opacity + subtle CSS pulse animation
- Not relevant to current era (when "show all" is on): 25% opacity
- Connection lines: dashed, colored matching the pin type, 2px weight

## UI Controls

A collapsible control panel on the map (top-right area, below any existing controls):

```
[Evidence ▼]
  [ ] Show All Eras
  [x] Archaeological (42)
  [x] Cross-Cultural (118)
  [x] Inscriptions (35)
```

- Toggle "Show All Eras": off by default (pins filter by era slider)
- Three category checkboxes: all on by default, counts shown per current filter
- Panel collapses to a single "Evidence" button when not in use
- Styled to match existing map UI (dark bg, gold accents)
- Evidence pins are independent of the peoples filter — peoples filter only affects kingdom polygons

## Pin Popup (on click)

Styled Leaflet popup matching the app aesthetic:
- Name (bold)
- Type badge (colored by category)
- Reliability badge: confirmed (green), debated (amber), contested (red)
- Culture of origin (for cross-cultural)
- Description (3-5 sentences)
- Scholarly detail (excavator, date, museum)
- Scripture references
- "Show Connections" button (draws radiating lines to related pins)
- Museum/location where housed (if applicable)

## Backend

### New Data File
`backend/data/evidence.json` — 200+ entries plus biblical_events lookup table

### New Service
`backend/services/evidence_service.py`:
- Load evidence from JSON (lazy, cached — same pattern as MapService)
- `get_evidence_summary(era_start=None, era_end=None, type=None)` → lightweight list (id, name, type, lat, lng, coordinate_type, era_start, era_end, biblical_event_id, reliability) for pin rendering
- `get_evidence(id)` → full detail for popup
- `get_connections(biblical_event_id)` → all pins + event coordinates for connection lines
- `search(query)` → search by name, culture, description

### New Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/map/evidence` | Lightweight summary list for pin rendering. Optional query params: `?era=<era_id>&type=<type>` |
| GET | `/api/map/evidence/{evidence_id}` | Full detail for one evidence entry (loaded on click) |
| GET | `/api/map/evidence/connections?event=<biblical_event_id>` | All pins + event coordinates for a given biblical event (query param, not path param) |

### Updated
- **Unified search** (`search_service.py`): includes evidence results under key `"map_evidence"`, returning `[{id, name, type, culture, reliability}]`
- **Frontend search** (`submitLookup()`): renders evidence results with type-colored badges and click-to-map behavior

## Frontend

### New Components
- Evidence pin rendering (called after kingdom/city rendering in `loadEra()`)
- Evidence control panel HTML + CSS (collapsible, top-right)
- `showEvidencePopup(evidence, marker)` — styled popup with connection button
- `showConnections(biblicalEventId)` — draws radiating animated polylines
- `hideConnections()` — clears polylines
- CSS pulse animation keyframe for era-relevant pins

### Updated
- `state` object: add `evidenceData`, `evidenceLayers`, `evidenceConnectionLines`, `evidenceFilters: {showAll: false, archaeological: true, cross_cultural: true, inscription: true}`
- `loadEra()`: fetch and render evidence pins after kingdoms/cities
- `submitLookup()`: render evidence search results with `map_evidence` key

## Loading Strategy

Evidence summary (lightweight) is fetched once on map init and cached. Full detail is fetched on click per pin. This keeps initial load fast while providing rich detail on demand.

## Error Handling

- If `evidence.json` is missing: evidence features silently disabled, no pins shown, control panel hidden
- If an evidence entry references a nonexistent `era_id`: entry is skipped (not rendered)
- If `biblical_events` entry has null coordinates: connection lines radiate from map center

## Reliability Ratings

- **Confirmed**: Widely accepted by scholars, physical evidence exists, multiple corroborating sources
- **Debated**: Scholarly disagreement on interpretation, but evidence is genuine
- **Contested**: Authenticity or connection to biblical events disputed
