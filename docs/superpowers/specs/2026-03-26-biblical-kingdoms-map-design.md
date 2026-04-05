# Biblical Kingdoms Map — Design Spec

## Overview

A new "Map" tab in Trials of Judah featuring a full interactive map of the ancient world. Covers all kingdoms, countries, and peoples mentioned in scripture — from Britain (Tarshish) to India, Ethiopia to the Caucasus. An era slider tied to key biblical events animates kingdom boundaries over time. Fully integrated with existing app features (lineage, prophecy, verses, unified search).

## Technology

- **Leaflet.js** for map rendering (zoom, pan, click, polygon overlays)
- **Antique-styled base tiles** (CartoDB Positron or Stamen Watercolor, re-tinted to match the app's dark brown/gold parchment aesthetic)
- **GeoJSON polygons** for kingdom boundaries, stored as separate files per era under `backend/data/map/geojson/`
- **Leaflet CDN** — no additional frontend dependencies

## Map Coverage

### Geographic Extent
Full ancient world — Mediterranean, Near East, North Africa, Central Asia. Extends to:
- **West:** Britain (Tarshish/Tin Isles), Spain
- **South:** Ethiopia/Cush, Libya/Put
- **East:** India, Persia
- **North:** Caucasus (Togarmah/Armenia), Scythian regions (Ashkenaz)

Anywhere scripture or historical evidence places biblical peoples is included.

### People Groups
All nations from Genesis 10 (Table of Nations), plus kingdoms that emerge throughout biblical history. Estimated 70-100+ entries including:
- Major empires: Egypt, Assyria, Babylon, Persia, Greece, Rome
- Israelite kingdoms: United Kingdom, Israel (north), Judah (south)
- Neighboring nations: Philistia, Moab, Edom, Ammon, Aram/Syria, Phoenicia/Sidon/Tyre
- Table of Nations descendants: Cush, Put, Togarmah, Tarshish, Ashkenaz, Javan, Magog, Meshech, Tubal, etc.
- Migration territories based on scripture and scholarly evidence

### Cities
- **Default view (zoomed out):** Capitals + ~40-50 major biblical cities visible as markers (Jerusalem, Babylon, Nineveh, Memphis, Ur, Bethlehem, Damascus, Tyre, etc.)
- **Kingdom selected (zoomed in):** ALL scripture-mentioned cities within that kingdom's borders revealed with markers and labels

## Border Accuracy & Labeling

Two visual tiers with a persistent legend on the map:

| Border Style | Meaning | Examples |
|---|---|---|
| **Solid line** | Documented boundaries from scholarly/archaeological evidence | Egypt, Assyria, Babylon, Persia, Greece, Rome, Israel, Judah |
| **Dotted/soft line** | Approximate territory based on scripture and scholarly estimates | Togarmah, Put, Tarshish, Ophir, Magog |

**Legend** is always visible on the map, clearly explaining:
- "Solid border = documented boundaries from historical/archaeological evidence"
- "Dotted border = approximate territory based on scripture and scholarly estimates"

Each kingdom's detail panel also states its border accuracy classification.

## Era Slider

### Structure
~15-20 event-based stops tied to scripture. Each stop has:
- Title
- Approximate date
- Scripture reference
- Brief description (1-2 sentences)

### Proposed Stops

1. **Table of Nations** — Post-Babel migration (Genesis 10-11)
2. **Abraham's Journey** — Ur to Canaan, ~2000 BC (Genesis 12)
3. **Sojourn in Egypt** — Jacob's family enters Egypt (Genesis 46)
4. **Exodus & Wilderness** — ~1446 BC (Exodus 12-14)
5. **Conquest of Canaan** — Joshua's campaigns (Joshua 1-12)
6. **Period of Judges** — Tribal territories, surrounding threats (Judges)
7. **United Kingdom** — Saul, David, Solomon, ~1050-930 BC (1 Samuel - 1 Kings 11)
8. **Divided Kingdom** — Israel & Judah split, ~930 BC (1 Kings 12)
9. **Fall of Samaria** — Assyrian conquest of northern Israel, 722 BC (2 Kings 17)
10. **Babylonian Exile** — Fall of Jerusalem, 586 BC (2 Kings 25)
11. **Persian Period** — Return under Cyrus, ~539 BC (Ezra 1)
12. **Greek Period** — Alexander's conquest, ~330 BC (Daniel 8)
13. **Maccabean Period** — ~167-63 BC (1 Maccabees)
14. **Roman Period** — ~63 BC onward (Luke 2:1)
15. **Jesus's Ministry** — ~30 AD (Gospels)
16. **Early Church / Apostolic Missions** — ~33-65 AD (Acts)

## Era Transitions (Animated)

When the user moves the slider between eras:

- **New kingdoms** pulse/glow as they appear
- **Fallen kingdoms** fade to ghost outlines (still visible, communicates "this kingdom used to exist here")
- **Changed borders** smoothly animate their boundary shift
- **Event toast** appears at the top of the map: title, date, and scripture reference (e.g., "722 BC — Fall of the Northern Kingdom — 2 Kings 17:6")

## Peoples Filter (Historical Tracking)

A sidebar or collapsible panel lists **modern-day peoples with biblical history** — drawn from the `modern_connections` data in lineage.json and the kingdoms data. Examples: Armenians (Togarmah), Ethiopians (Cush), Egyptians (Mizraim), Greeks (Javan), Persians (Elam), Arabs (Ishmael), Israelites (twelve tribes), etc.

### Behavior
When a user selects a people group from the filter list:

1. **All other kingdoms/peoples fade to ~20% opacity** — same visual treatment as kingdom selection
2. **The selected people's territory highlights across ALL eras** — as the user moves the slider, only that people's boundaries animate and stay prominent. Their origin territory, migration path, kingdom phases, and modern location are all tracked.
3. **Narrative bar** appears at the bottom of the map showing era-specific context for that people group — e.g., "Togarmah — Gen 10:3, descendant of Japheth through Gomer. Settled in eastern Asia Minor." Updates as the slider moves: "Armenian Kingdom — allied with Persia against Rome."
4. **Migration paths** are shown as animated dotted lines connecting their territory across eras, so the user can visually trace where a people moved over time.
5. **Click the highlighted territory** to open the full detail panel (same as normal kingdom selection, but pre-filtered to that people's data).
6. **Clear filter** button returns the map to the default all-kingdoms view.

### Data Source
Each entry in the peoples filter maps to:
- A `modern_connections` entry (linking to a lineage ancestor and modern people group)
- One or more kingdom entries across eras (the territories this people occupied)
- A `peoples.json` data file (or section within `kingdoms.json`) containing: modern name, biblical ancestor, Genesis 10 reference, migration summary, era-to-kingdom mapping, and narrative text per era

### Mobile
On mobile, the peoples filter is a **searchable dropdown** at the top of the map (above the era selector). The narrative bar becomes a **swipeable card** at the bottom.

## Kingdom Selection Behavior

When a user clicks/taps a kingdom:

1. **Selected kingdom** stays full opacity, border highlights in gold
2. **All other kingdoms** fade to ~20% opacity
3. **Map smoothly zooms** into the selected kingdom's bounds
4. **All cities within** that kingdom (for the current era) appear as the zoom completes
5. **Detail panel** opens (side panel on desktop, bottom sheet on mobile)
6. **Click anywhere else** or hit a back/close button to restore full view (all kingdoms return to normal opacity, cities revert to default set)

## Detail Panel

### Compact Card (all kingdoms)
Shown initially when a kingdom is selected:
- Kingdom/people name
- Era range (when it existed)
- Capital city
- Primary scripture reference
- Modern-day location/region
- Border accuracy indicator (documented vs. approximate)

### Expanded Panel (major kingdoms — via "Explore Further" button)
- **Key Scriptures** — Verses mentioning this kingdom, resolved by keyword search of the kingdom name (and known aliases) against the `bible_kjv` table
- **Historical/Scholarly Context** — Archaeological evidence, secular historical records (stored in `kingdoms.json` metadata)
- **Related Prophecies** — Resolved by matching kingdom name and aliases against `prophecy_text`, `fulfillment_text`, and `title` fields in the prophecies table. Cross-links open the Prophecy tab.
- **Lineage Connections** — Resolved by matching the kingdom's `modern_region` against `modern_connections.region` and by matching ancestor name against `persons.name_english`. Cross-links open the Lineage tab.
- **Related Verse Categories** — Resolved by keyword matching against verse category descriptions and verse text
- **All Cities** — Complete list of scripture-mentioned cities within this kingdom (for the current era) with references

Panel styling matches existing app design (dark background, gold accents, scripture panel style).

## App Integration (Bidirectional)

### Map → Other Tabs
- Kingdom detail panels contain clickable links to:
  - Related prophecies → opens Prophecy tab filtered to that prophecy
  - Lineage persons → opens person panel in Lineage tab
  - Verse categories → opens relevant category in Trials/Guidance tab

### Other Tabs → Map
- **Lineage person detail panel:** "View on Map" button → switches to Map tab, highlights the relevant region in the appropriate era
- **Prophecy detail panel:** "Show on Map" button → switches to Map tab, centers on the location in the correct era
- Cross-reference buttons use the existing `switchTab()` pattern

### Unified Search Integration
- Searching a term (e.g., "Babylon") returns map kingdoms/cities alongside existing results (verses, persons, prophecies)
- Map search results include a **mini-map preview** (~250-300px tall) — a single shared Leaflet instance that repositions to show the highlighted location for the focused/hovered search result. Only one mini-map is rendered at a time to avoid performance issues with multiple Leaflet instances.
- Mini-map is large enough to be useful without switching tabs
- Clicking the map result jumps to the Map tab, centered on that location in the relevant era

## Mobile Experience

- **Landscape suggestion:** When the Map tab is active on a portrait mobile device, display a prominent banner: "Rotate your device to landscape for the best map experience." The Screen Orientation API (`screen.orientation.lock('landscape')`) is attempted when available (Android Chrome in fullscreen) but not relied upon, as iOS Safari does not support it.
- **Bottom sheet** for kingdom details — swipe up to expand, swipe down to minimize (like Google Maps)
- **Era slider** becomes a **dropdown selector** on screens < 768px
- Full touch support: pinch-zoom, tap to select kingdom, two-finger pan
- Back button / tap-outside dismisses selection and restores full view

## Loading & Error States

- **Initial load:** A loading spinner overlays the map container while era/kingdom data is fetched. Map tiles load progressively underneath.
- **Era switch:** A brief loading indicator appears if GeoJSON for the new era hasn't been cached yet.
- **Tile CDN failure:** If map tiles fail to load, a parchment-textured fallback background is displayed so kingdom polygons and city markers remain usable.
- **API failure:** Standard app error pattern — `.empty-state` div with "Failed to load map data" message and a retry button.
- **GeoJSON caching:** Once fetched, era GeoJSON is cached in the `state` object so subsequent slider movements to previously-viewed eras are instant.

## Backend

### Data File Structure

Kingdom metadata and GeoJSON geometry are separated for performance:

**`backend/data/kingdoms.json`** — Metadata only (no GeoJSON geometry):

```json
{
  "eras": [
    {
      "id": 1,
      "name": "Table of Nations",
      "date_approx": "~2200 BC",
      "scripture_ref": "Genesis 10-11",
      "description": "After Babel, Noah's descendants spread across the earth.",
      "sort_order": 1
    }
  ],
  "kingdoms": [
    {
      "id": 1,
      "name": "Egypt",
      "name_hebrew": "Mitzrayim",
      "aliases": ["Mizraim", "Mitzrayim", "land of Egypt"],
      "ancestor": "Mizraim son of Ham",
      "ancestor_ref": "Genesis 10:6",
      "capital": "Memphis / Thebes",
      "border_accuracy": "documented",
      "modern_region": "Modern Egypt",
      "description": "...",
      "scholarly_context": "...",
      "scripture_refs": ["Genesis 12:10", "Exodus 1:8"],
      "boundaries": [
        { "era_start": 1, "era_end": 7, "geojson_file": "egypt_early.json" },
        { "era_start": 8, "era_end": 11, "geojson_file": "egypt_late.json" },
        { "era_start": 12, "era_end": 16, "geojson_file": "egypt_ptolemaic.json" }
      ]
    }
  ],
  "cities": [
    {
      "id": 1,
      "name": "Jerusalem",
      "lat": 31.7683,
      "lng": 35.2137,
      "is_capital": true,
      "is_major": true,
      "scripture_refs": ["2 Samuel 5:6", "1 Kings 11:36"],
      "kingdom_associations": [
        { "kingdom_id": 5, "era_start": 7, "era_end": 9 },
        { "kingdom_id": 6, "era_start": 10, "era_end": 11 },
        { "kingdom_id": 7, "era_start": 12, "era_end": 16 }
      ]
    }
  ]
}
```

**`backend/data/map/geojson/`** — Separate GeoJSON files per kingdom per era:
- `egypt_early.json`, `egypt_late.json`, `egypt_ptolemaic.json`
- `assyria_peak.json`, `babylon_empire.json`
- `israel_united.json`, `israel_north.json`, `judah_south.json`
- etc.

This keeps the metadata file small and allows GeoJSON to be loaded on demand per era.

**`backend/data/peoples.json`** — Modern peoples with biblical history for the peoples filter:

```json
{
  "peoples": [
    {
      "id": 1,
      "modern_name": "Armenians",
      "biblical_ancestor": "Togarmah",
      "ancestor_ref": "Genesis 10:3",
      "lineage": "Japheth > Gomer > Togarmah",
      "kingdom_ids": [14, 15],
      "migration_summary": "Settled in eastern Asia Minor and the Caucasus. Armenian tradition claims descent from Togarmah (called Torgom).",
      "era_narratives": [
        { "era_id": 1, "text": "Togarmah, son of Gomer, son of Japheth. Settled in eastern Asia Minor after the dispersion at Babel." },
        { "era_id": 8, "text": "The kingdom of Urartu (Ararat) flourished in the Armenian highlands, trading horses with Tyre (Ezekiel 27:14)." },
        { "era_id": 14, "text": "Armenia became the first nation to adopt Christianity as a state religion (c. AD 301)." }
      ]
    }
  ]
}
```

### New Service: `map_service.py`
Located at `backend/services/map_service.py`. Handles:
- Loading kingdom metadata from `kingdoms.json` at startup
- Loading peoples data from `peoples.json` at startup
- Loading GeoJSON files on demand from `backend/data/map/geojson/`
- Querying kingdoms and cities by era
- Querying peoples and their kingdom associations across eras
- Search across kingdoms, cities, and peoples by name/alias
- Cross-referencing with prophecy and lineage data via keyword matching

### New API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/map/eras` | All era metadata (for slider) |
| `GET` | `/api/map/kingdoms` | All kingdom metadata without geometry (for initial load) |
| `GET` | `/api/map/era/{era_id}` | Kingdoms active in this era with their GeoJSON geometry loaded on demand |
| `GET` | `/api/map/kingdom/{kingdom_id}` | Full detail for one kingdom including all cities (era-filtered) and cross-references |
| `GET` | `/api/map/kingdom/{kingdom_id}/geojson?era={era_id}` | GeoJSON geometry for a specific kingdom in a specific era |
| `GET` | `/api/map/peoples` | All peoples for the filter list (modern name, ancestor, lineage) |
| `GET` | `/api/map/people/{people_id}` | Full detail for one people group including kingdom associations, era narratives, and migration path |
| `GET` | `/api/map/search?q=` | Search kingdoms, cities, and peoples by name |

### Updated Endpoints
- **`POST /api/search`** — Unified search now includes map kingdoms/cities in results
- **`GET /api/lineage/person/{id}`** — Response includes `map_location` field with kingdom_id and era for "View on Map" linking
- **`GET /api/prophecy/{id}`** — Response includes `map_location` field for "Show on Map" linking

### Data Storage
Kingdom metadata is read from `kingdoms.json` at startup and held in memory. GeoJSON geometry files are loaded from disk on demand and cached in memory after first access. No new database tables needed.

## Frontend Changes

### New Components (in `index.html`)
- **Map tab content area** — Full-width Leaflet map container with explicit height: `calc(100vh - 120px)` (Leaflet requires a defined height to render)
- **Era slider** — Horizontal slider with labeled stops (dropdown on mobile)
- **Peoples filter** — Sidebar list on desktop, searchable dropdown on mobile. Lists modern peoples with biblical history.
- **Narrative bar** — Bottom bar showing era-specific context when a people is filtered. Swipeable card on mobile.
- **Kingdom detail panel** — Side panel (desktop) / bottom sheet (mobile)
- **Mini-map component** — Single shared Leaflet instance for search results, repositioned per result
- **Map legend** — Border accuracy explanation, always visible

### Updated Components
- **Tab bar** — Add "Map" tab button
- **`switchTab()` function** — Add `'map'` to the tab list. Map tab triggers `maxWidth: '100%'` (same as lineage/prophecy). Lazy-loads map data on first visit.
- **State object** — Add `mapLoaded`, `mapData`, `selectedKingdom`, `selectedEra`, `selectedPeople`, `mapGeoJsonCache`, `peoplesData`
- **Lineage person panel** — Add "View on Map" button
- **Prophecy detail panel** — Add "Show on Map" button
- **Search results** — Add kingdom/city results with single shared mini-map
- **CSS media query** — Landscape suggestion banner for map tab on mobile

### External Resources (CDN)
- Leaflet.js CSS + JS
- Map tile provider (CartoDB or similar, styled to match app theme)

## Accessibility

- Kingdom detail panel is keyboard-navigable (Tab/Enter to open, Escape to close)
- Era slider supports arrow key navigation
- Detail panel content uses appropriate ARIA labels (`aria-label` on interactive elements, `role="dialog"` on detail panel)
- Screen reader announcements for era changes and kingdom selection via `aria-live` region
