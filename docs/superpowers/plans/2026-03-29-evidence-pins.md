# Evidence Pins Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add 200+ evidence pins to the Biblical Kingdoms Map showing archaeological discoveries, cross-cultural records, and inscriptions that confirm scripture, with connection lines radiating from biblical events to every culture that recorded them.

**Architecture:** New `evidence.json` data file with biblical_events lookup table + evidence entries. New `evidence_service.py` backend service (lazy-loaded, cached). New API endpoints under `/api/map/evidence/*`. Frontend adds pin rendering, control panel, popups, and animated connection lines to the existing map tab.

**Tech Stack:** Python/FastAPI, JSON data, Leaflet.js (existing), vanilla JavaScript

**Spec:** `docs/superpowers/specs/2026-03-29-evidence-pins-design.md`

---

## File Structure

### New Files
| File | Responsibility |
|------|---------------|
| `backend/data/evidence.json` | 200+ evidence entries + biblical_events lookup table |
| `backend/services/evidence_service.py` | Load, filter, search evidence data |

### Modified Files
| File | Changes |
|------|---------|
| `backend/main.py` | Add evidence API endpoints |
| `backend/services/search_service.py` | Add evidence to unified search |
| `frontend/index.html` | Evidence pins, control panel, popups, connection lines, CSS |

---

## Task 1: Create evidence.json — biblical_events + archaeological entries

**Files:**
- Create: `backend/data/evidence.json`

- [ ] **Step 1: Create the file with biblical_events lookup table and ~40-50 archaeological entries**

The `biblical_events` array defines the canonical events that evidence confirms. Each has an id, name, coordinates (for connection line origin), and scripture refs.

Start with these biblical events:
- great_flood (39.7, 44.3 — Ararat area)
- creation (null coords)
- tower_of_babel (32.54, 44.42 — Babylon)
- exodus_plagues (30.05, 31.23 — Egypt)
- exodus_red_sea (29.0, 33.0 — Gulf of Suez area)
- conquest_of_jericho (31.87, 35.44)
- destruction_of_sodom (31.2, 35.4 — Dead Sea area)
- joshuas_long_day (31.85, 35.18 — Gibeon area)
- solomons_kingdom (31.77, 35.23 — Jerusalem)
- assyrian_conquest (31.77, 35.23)
- babylonian_exile (31.77, 35.23)
- persian_decree (32.19, 48.25 — Susa)
- crucifixion_darkness (31.77, 35.23 — Jerusalem)
- resurrection (31.77, 35.23)
- patriarchal_longevity (null coords)
- language_dispersion (32.54, 44.42 — Babel)
- messianic_prophecy (31.77, 35.23)
- divine_fire_destruction (31.2, 35.4)

Archaeological entries (~40-50) should include:
Dead Sea Scrolls, Cyrus Cylinder, Merneptah Stele, Tel Dan Stele ("House of David"), Walls of Jericho, Hezekiah's Tunnel, Pilate Stone, Pool of Siloam, Tall el-Hammam (Sodom), Noah's Ark site (Ararat), Taylor Prism (Sennacherib), Lachish reliefs, Moabite Stone (Mesha Stele), Black Obelisk of Shalmaneser, Siloam Inscription, Nazareth Inscription, James Ossuary, Ketef Hinnom silver scrolls, Lachish Letters, LMLK seals, Nebo-Sarsekim tablet, Pontius Pilate ring, Caiaphas Ossuary, Temple Warning inscription, Arch of Titus, Pool of Bethesda, Jacob's Well, Hezekiah's Broad Wall, Sennacherib's Palace reliefs, City of David excavations, Khirbet Qeiyafa (Elah fortress), Seal of Isaiah, Seal of Hezekiah, Seal of King Josiah's servant, Babylonian Chronicles, Nabonidus Chronicle, Elephantine Papyri, Tel Hazor destruction layer, Shishak/Shoshenq invasion relief at Karnak, Gezer Calendar, Samaria Ostraca, Arad Ostraca.

Each entry needs: id (string), name, type ("archaeological"), category, lat, lng, coordinate_type ("exact"), era_start, era_end, biblical_event_id, scripture_refs, description (3-5 sentences), scholarly_detail (excavator, date, museum), reliability, culture, museum, date_discovered.

- [ ] **Step 2: Commit**

```bash
git add backend/data/evidence.json
git commit -m "feat(evidence): create evidence.json with biblical events and archaeological entries"
```

---

## Task 2: Add cross-cultural flood narratives (~50-60 entries)

**Files:**
- Modify: `backend/data/evidence.json`

- [ ] **Step 1: Add flood narrative entries from cultures worldwide**

All should have `biblical_event_id: "great_flood"`, `type: "cross_cultural"`, `category: "flood"`, `era_start: "table_of_nations"`, `era_end: "table_of_nations"`.

Cultures to include (with approximate cultural center coordinates):
- Sumerian (Ziusudra) — Iraq
- Babylonian (Gilgamesh/Utnapishtim) — Iraq
- Chinese (Nu Wa / Gun-Yu) — China
- Hindu (Manu / Matsya) — India
- Greek (Deucalion) — Greece
- Norse (Bergelmir) — Scandinavia
- Aboriginal Australian (multiple) — Australia
- Maori (Ruatapu) — New Zealand
- Hawaiian (Nu'u) — Hawaii
- Hopi (Toktela/Spider Grandmother) — Arizona, USA
- Cree (Wisakedjak) — Canada
- Aztec (Coxcoxtli) — Mexico
- Inca (Viracocha) — Peru
- Maya (Popol Vuh flood) — Guatemala
- Yoruba (Obatala) — Nigeria
- Maasai — Kenya/Tanzania
- Egyptian (Book of the Dead references) — Egypt
- Persian (Yima / Bundahishn) — Iran
- Korean (Namu Dolyeong) — Korea
- Japanese (Izanagi/Izanami) — Japan
- Fijian — Fiji
- Samoan — Samoa
- Tongan — Tonga
- Chaldean (Berossus) — Iraq
- Ojibwe (Nanabozho) — Great Lakes, USA
- Cherokee (Dayunisi) — Southeast USA
- Navajo (Water Monster) — Southwest USA
- Mapuche (Trentren Vilu) — Chile
- Muisca (Bochica) — Colombia
- Taino — Caribbean
- Algonquin — Northeast USA
- Inuit — Arctic
- Finnish (Kalevala references) — Finland
- Lithuanian — Lithuania
- Romanian — Romania
- Babylonian (Atrahasis) — Iraq
- Sumerian (Eridu Genesis) — Iraq
- Egyptian (Hermopolis tradition) — Egypt
- Andaman Islander — India (Andaman Islands)
- Hmong (Nuah) — Southeast Asia
- Taiwanese Aboriginal — Taiwan
- Filipino (Malakas at Maganda) — Philippines
- Vietnamese — Vietnam
- Thai — Thailand
- Batak (Toba) — Indonesia
- Toraja — Indonesia
- Papua New Guinean — PNG
- Ethiopian (various) — Ethiopia
- Congolese (Mbuti/BaTwa) — Congo

Each needs: id, name, lat, lng, coordinate_type ("cultural_region"), description (2-3 sentences about the narrative), scholarly_detail (who documented it, key source), reliability ("confirmed" — the narrative exists even if interpretation differs), culture.

- [ ] **Step 2: Commit**

---

## Task 3: Add cross-cultural non-flood entries (~50-75 entries)

**Files:**
- Modify: `backend/data/evidence.json`

- [ ] **Step 1: Add creation narratives (~15-20)**

All with `biblical_event_id: "creation"`, `category: "creation"`.
Egyptian, Sumerian, Chinese, Hindu, Norse, Mayan, Polynesian, Aboriginal, Yoruba, Aztec, Japanese, Zoroastrian, Mesopotamian (Enuma Elish), Greek (Hesiod), Native American (Iroquois), Inuit, Maori.

- [ ] **Step 2: Add Tower of Babel / language dispersion (~10-15)**

All with `biblical_event_id: "language_dispersion"`, `category: "language_dispersion"`.
Sumerian (Enmerkar), Mayan, Australian Aboriginal, African Wa-Sania, Greek, Hindu, Kiche Maya, Toltec, Karen (Myanmar), Gaikundi (PNG), Mexican (Cholula pyramid tradition).

- [ ] **Step 3: Add plague/Exodus parallels (~5-8)**

`biblical_event_id: "exodus_plagues"`, `category: "exodus_parallels"`.
Ipuwer Papyrus, Ahmose Tempest Stele, El Arish Shrine text, Manetho's account, Hecataeus of Abdera, Artapanus of Alexandria.

- [ ] **Step 4: Add destruction by fire parallels (~5-8)**

`biblical_event_id: "divine_fire_destruction"`, `category: "fire_destruction"`.
Tall el-Hammam airburst, Greek Phaethon, Hindu Mahabharata, Sumerian destruction texts, Roman (Tacitus on Dead Sea region).

- [ ] **Step 5: Add patriarch/longevity traditions (~5-8)**

`biblical_event_id: "patriarchal_longevity"`, `category: "longevity"`.
Sumerian King List, Chinese legendary emperors, Hindu Yugas, Egyptian Turin King List, Babylonian king lists.

- [ ] **Step 6: Add solar/cosmic event records (~5-8)**

`biblical_event_id: "joshuas_long_day"` and `"crucifixion_darkness"`, `category: "cosmic_events"`.
Chinese Bamboo Annals (long day), Mesoamerican long night, Egyptian records, Thallus (crucifixion darkness), Phlegon of Tralles, Tertullian's reference to Roman archives.

- [ ] **Step 7: Add messianic/sacrifice traditions (~5-8)**

`biblical_event_id: "messianic_prophecy"`, `category: "messianic_parallels"`.
Hindu Prajapati, Aztec Quetzalcoatl, Chinese ShangDi border sacrifice, Egyptian Osiris, Zoroastrian Saoshyant, Buddhist Maitreya parallels.

- [ ] **Step 8: Commit**

---

## Task 4: Add inscription & artifact entries (~30-40)

**Files:**
- Modify: `backend/data/evidence.json`

- [ ] **Step 1: Add inscription entries**

These overlap with archaeological but are specifically text-bearing objects. Type: "inscription". Include: Moabite Stone, Black Obelisk, Siloam Inscription, Nazareth Inscription, Ketef Hinnom scrolls, Lachish Letters, LMLK seals, Nebo-Sarsekim tablet, Pontius Pilate ring, Seal of Isaiah, Seal of Hezekiah, Gezer Calendar, Samaria Ostraca, Arad Ostraca, Temple Warning Stone, Theodotus Inscription, Gallio Inscription (Delphi), Erastus Inscription (Corinth), Politarch inscriptions (Thessalonica), Sergius Paulus inscription (Cyprus), Kuyunjik tablet (Babylonian map), Balaam inscription (Deir Alla), Ekron Royal Dedicatory Inscription, Tell Siran bronze bottle, Ophel (Temple Mount) pithos inscription, Khirbet el-Qom inscription, Ivory pomegranate inscription, Bulla of Baruch son of Neriah, Bulla of Gemariah son of Shaphan.

- [ ] **Step 2: Commit**

---

## Task 5: Create evidence_service.py

**Files:**
- Create: `backend/services/evidence_service.py`

- [ ] **Step 1: Create the service**

```python
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

    def get_biblical_events(self) -> list:
        self._load_data()
        return self._data["biblical_events"]

    def get_evidence_summary(self, era: str = None, evidence_type: str = None) -> list:
        """Lightweight list for pin rendering."""
        self._load_data()
        era_order = None
        era_idx = None
        if era:
            # Need era ordering from kingdoms.json to do range comparison
            kingdoms_file = DATA_DIR / "kingdoms.json"
            if kingdoms_file.exists():
                with open(kingdoms_file, "r", encoding="utf-8") as f:
                    kdata = json.load(f)
                era_order = [e["id"] for e in kdata["eras"]]
                try:
                    era_idx = era_order.index(era)
                except ValueError:
                    era_idx = None

        results = []
        for e in self._data["evidence"]:
            # Type filter
            if evidence_type and e["type"] != evidence_type:
                continue
            # Era range filter
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
```

- [ ] **Step 2: Commit**

---

## Task 6: Add evidence API endpoints

**Files:**
- Modify: `backend/main.py`

- [ ] **Step 1: Add import and endpoints**

Add import: `from backend.services.evidence_service import evidence_service`

Add endpoints after the map section:

```python
# ── Evidence ───────────────────────────────────────
@app.get("/api/map/evidence")
async def map_evidence(era: str = None, type: str = None):
    return {"evidence": evidence_service.get_evidence_summary(era, type)}

@app.get("/api/map/evidence/connections")
async def map_evidence_connections(event: str = Query(...)):
    return evidence_service.get_connections(event)

@app.get("/api/map/evidence/{evidence_id}")
async def map_evidence_detail(evidence_id: str):
    result = evidence_service.get_evidence(evidence_id)
    if not result:
        return JSONResponse({"error": "Evidence not found"}, status_code=404)
    return result
```

IMPORTANT: The `/api/map/evidence/connections` route MUST be defined BEFORE `/api/map/evidence/{evidence_id}` — otherwise FastAPI will try to match "connections" as an evidence_id.

- [ ] **Step 2: Commit**

---

## Task 7: Update unified search with evidence

**Files:**
- Modify: `backend/services/search_service.py`

- [ ] **Step 1: Add evidence to search results**

Add import: `from backend.services.evidence_service import evidence_service`

In the `search` method, after the map_results line, add:
```python
evidence_results = evidence_service.search(query)
```

Add to return dict: `"map_evidence": evidence_results`

- [ ] **Step 2: Update /api/search endpoint in main.py**

Add `"map_evidence": results.get("map_evidence", [])` to the return dict in the `unified_search` function.

- [ ] **Step 3: Commit**

---

## Task 8: Frontend — Evidence CSS + control panel HTML

**Files:**
- Modify: `frontend/index.html`

- [ ] **Step 1: Add evidence CSS**

Before closing `</style>`, add:

```css
/* Evidence Pins */
.evidence-controls {
  position: absolute; top: 10px; right: 10px; z-index: 1001;
  background: rgba(26,15,10,0.95); border: 1px solid rgba(201,168,76,0.2);
  border-radius: 8px; min-width: 200px; font-size: 0.78rem;
}
.evidence-controls-header {
  padding: 8px 12px; cursor: pointer; color: #c9a84c; font-weight: 600;
  display: flex; justify-content: space-between; align-items: center;
}
.evidence-controls-body { padding: 0 12px 10px; display: none; }
.evidence-controls-body.open { display: block; }
.evidence-toggle { display: flex; align-items: center; gap: 8px; padding: 4px 0; color: #d4c5b0; cursor: pointer; }
.evidence-toggle input { accent-color: #c9a84c; }
.evidence-toggle .count { color: #8a7a60; font-size: 0.7rem; }
.evidence-badge { display: inline-block; padding: 1px 6px; border-radius: 8px; font-size: 0.65rem; font-weight: 600; }
.evidence-badge.archaeological { background: rgba(212,136,15,0.2); color: #D4880F; }
.evidence-badge.cross_cultural { background: rgba(0,151,167,0.2); color: #0097A7; }
.evidence-badge.inscription { background: rgba(46,125,50,0.2); color: #2E7D32; }
.evidence-badge.confirmed { background: rgba(46,125,50,0.15); color: #4CAF50; }
.evidence-badge.debated { background: rgba(255,152,0,0.15); color: #FF9800; }
.evidence-badge.contested { background: rgba(244,67,54,0.15); color: #F44336; }
@keyframes evidence-pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.6; } }
.evidence-pin-active { animation: evidence-pulse 2s ease-in-out infinite; }
```

- [ ] **Step 2: Add control panel HTML**

In the map-view div, after the legend div and before the detail panel div, add:

```html
<div class="evidence-controls" id="evidence-controls">
  <div class="evidence-controls-header" onclick="toggleEvidencePanel()">
    Evidence <span id="evidence-arrow">&#9660;</span>
  </div>
  <div class="evidence-controls-body" id="evidence-body">
    <label class="evidence-toggle"><input type="checkbox" id="evidence-show-all" onchange="onEvidenceFilterChange()"> Show All Eras</label>
    <label class="evidence-toggle"><input type="checkbox" id="evidence-archaeological" checked onchange="onEvidenceFilterChange()"> Archaeological <span class="count" id="evidence-count-arch"></span></label>
    <label class="evidence-toggle"><input type="checkbox" id="evidence-cross-cultural" checked onchange="onEvidenceFilterChange()"> Cross-Cultural <span class="count" id="evidence-count-cc"></span></label>
    <label class="evidence-toggle"><input type="checkbox" id="evidence-inscription" checked onchange="onEvidenceFilterChange()"> Inscriptions <span class="count" id="evidence-count-ins"></span></label>
  </div>
</div>
```

- [ ] **Step 3: Commit**

---

## Task 9: Frontend — Evidence state, loading, pin rendering

**Files:**
- Modify: `frontend/index.html`

- [ ] **Step 1: Add evidence state properties**

In the state object, add:
```javascript
evidenceData: [],
evidenceBiblicalEvents: [],
evidenceLayers: [],
evidenceConnectionLines: [],
evidenceFilters: { showAll: false, archaeological: true, cross_cultural: true, inscription: true },
```

- [ ] **Step 2: Load evidence data in loadMap()**

After loading peoples data, add:
```javascript
var evidenceResp = await apiFetch('/api/map/evidence');
state.evidenceData = evidenceResp.evidence || [];
// Also fetch biblical events for connections
var eventsResp = await apiFetch('/api/map/evidence?era=table_of_nations');
// We'll load full evidence list for counts
updateEvidenceCounts();
```

- [ ] **Step 3: Add evidence rendering function**

```javascript
function renderEvidencePins(eraId) {
  // Clear existing
  state.evidenceLayers.forEach(function(m) { state.mapInstance.removeLayer(m); });
  state.evidenceLayers = [];
  hideConnections();

  var filters = state.evidenceFilters;
  var eraOrder = state.mapEras.map(function(e) { return e.id; });
  var eraIdx = eraOrder.indexOf(eraId);

  state.evidenceData.forEach(function(e) {
    // Type filter
    if (e.type === 'archaeological' && !filters.archaeological) return;
    if (e.type === 'cross_cultural' && !filters.cross_cultural) return;
    if (e.type === 'inscription' && !filters.inscription) return;

    // Era filter
    var startIdx = eraOrder.indexOf(e.era_start);
    var endIdx = eraOrder.indexOf(e.era_end);
    var inEra = (startIdx <= eraIdx && eraIdx <= endIdx);
    if (!filters.showAll && !inEra) return;

    var colors = { archaeological: '#D4880F', cross_cultural: '#0097A7', inscription: '#2E7D32' };
    var color = colors[e.type] || '#D4880F';
    var isRegion = e.coordinate_type === 'cultural_region';
    var opacity = (filters.showAll && !inEra) ? 0.25 : 0.9;

    var marker = L.circleMarker([e.lat, e.lng], {
      radius: isRegion ? 8 : 5,
      color: '#ffffff', weight: 1.5,
      fillColor: color,
      fillOpacity: isRegion ? opacity * 0.6 : opacity,
      bubblingMouseEvents: false,
      className: inEra ? 'evidence-pin-active' : '',
    });
    marker.bindTooltip(e.name, { permanent: false, direction: 'top' });
    marker.on('click', function() { showEvidencePopup(e, marker); });
    marker.addTo(state.mapInstance);
    state.evidenceLayers.push(marker);
  });
  updateEvidenceCounts();
}
```

- [ ] **Step 4: Call renderEvidencePins at end of loadEra()**

In the `loadEra` function, after `updateNarrative(eraId);`, add:
```javascript
renderEvidencePins(eraId);
```

- [ ] **Step 5: Commit**

---

## Task 10: Frontend — Evidence popup + connection lines

**Files:**
- Modify: `frontend/index.html`

- [ ] **Step 1: Add popup function**

```javascript
async function showEvidencePopup(summary, marker) {
  // Fetch full detail
  var e = await apiFetch('/api/map/evidence/' + summary.id);
  var typeColors = { archaeological: '#D4880F', cross_cultural: '#0097A7', inscription: '#2E7D32' };
  var html = '<div style="max-width:300px; font-family:system-ui;">';
  html += '<div style="font-size:1rem; font-weight:700; color:#1a0f0a;">' + e.name + '</div>';
  html += '<div style="margin:4px 0;">';
  html += '<span class="evidence-badge ' + e.type + '">' + e.type.replace('_', '-') + '</span> ';
  html += '<span class="evidence-badge ' + e.reliability + '">' + e.reliability + '</span>';
  html += '</div>';
  if (e.culture) html += '<div style="font-size:0.75rem; color:#666;">Culture: ' + e.culture + '</div>';
  html += '<div style="font-size:0.8rem; color:#333; line-height:1.4; margin:6px 0;">' + e.description + '</div>';
  if (e.scholarly_detail) {
    html += '<div style="font-size:0.72rem; color:#555; padding-top:6px; border-top:1px solid #ddd; line-height:1.4;">';
    html += '<strong style="color:#722f37;">Scholarly Detail:</strong> ' + e.scholarly_detail + '</div>';
  }
  if (e.museum) html += '<div style="font-size:0.7rem; color:#8a7a60; margin-top:4px;">Housed: ' + e.museum + '</div>';
  if (e.scripture_refs && e.scripture_refs.length) {
    html += '<div style="font-size:0.7rem; color:#8a7a60; margin-top:4px;">' + e.scripture_refs.join(' | ') + '</div>';
  }
  if (e.biblical_event_id) {
    html += '<button onclick="showConnections(\'' + e.biblical_event_id + '\')" style="margin-top:8px; padding:4px 12px; border-radius:12px; background:rgba(0,151,167,0.15); border:1px solid rgba(0,151,167,0.3); color:#0097A7; font-size:0.75rem; cursor:pointer;">Show Connections</button>';
  }
  html += '</div>';
  marker.unbindPopup();
  marker.bindPopup(html, { maxWidth: 320, className: 'evidence-popup' }).openPopup();
}
```

- [ ] **Step 2: Add connection line functions**

```javascript
async function showConnections(biblicalEventId) {
  hideConnections();
  var data = await apiFetch('/api/map/evidence/connections?event=' + biblicalEventId);
  if (!data.event || !data.pins.length) return;

  var eventLat = data.event.lat;
  var eventLng = data.event.lng;
  // For null-coordinate events, use map center
  if (eventLat === null || eventLng === null) {
    var center = state.mapInstance.getCenter();
    eventLat = center.lat;
    eventLng = center.lng;
  }

  // Draw lines from event to each pin with animation delay
  data.pins.forEach(function(pin, i) {
    setTimeout(function() {
      var line = L.polyline([[eventLat, eventLng], [pin.lat, pin.lng]], {
        color: '#0097A7', weight: 1.5, opacity: 0.6, dashArray: '6 4',
      });
      line.addTo(state.mapInstance);
      state.evidenceConnectionLines.push(line);
    }, i * 30); // Stagger for animation effect
  });

  // Show count toast
  showMapToast(data.pins.length + ' cultures recorded: ' + data.event.name);
}

function hideConnections() {
  state.evidenceConnectionLines.forEach(function(line) { state.mapInstance.removeLayer(line); });
  state.evidenceConnectionLines = [];
}
```

- [ ] **Step 3: Add control panel functions**

```javascript
function toggleEvidencePanel() {
  var body = $('evidence-body');
  var arrow = $('evidence-arrow');
  body.classList.toggle('open');
  arrow.innerHTML = body.classList.contains('open') ? '&#9650;' : '&#9660;';
}

function onEvidenceFilterChange() {
  state.evidenceFilters.showAll = $('evidence-show-all').checked;
  state.evidenceFilters.archaeological = $('evidence-archaeological').checked;
  state.evidenceFilters.cross_cultural = $('evidence-cross-cultural').checked;
  state.evidenceFilters.inscription = $('evidence-inscription').checked;
  renderEvidencePins(state.selectedEra);
}

function updateEvidenceCounts() {
  var arch = 0, cc = 0, ins = 0;
  state.evidenceLayers.forEach(function() {}); // count rendered
  state.evidenceData.forEach(function(e) {
    if (e.type === 'archaeological') arch++;
    if (e.type === 'cross_cultural') cc++;
    if (e.type === 'inscription') ins++;
  });
  $('evidence-count-arch').textContent = '(' + arch + ')';
  $('evidence-count-cc').textContent = '(' + cc + ')';
  $('evidence-count-ins').textContent = '(' + ins + ')';
}
```

- [ ] **Step 4: Commit**

---

## Task 11: Frontend — Evidence in search results

**Files:**
- Modify: `frontend/index.html`

- [ ] **Step 1: Add evidence rendering in submitLookup()**

After the map_peoples block in submitLookup(), add:

```javascript
if (data.map_evidence && data.map_evidence.length) {
  html += '<div style="margin-bottom:12px;">';
  html += '<div style="font-size:0.78rem;color:#8a7a60;font-weight:700;margin-bottom:6px;">EVIDENCE</div>';
  data.map_evidence.forEach(function(e) {
    html += '<span class="panel-link-item" onclick="switchTab(\'map\');">';
    html += '<span class="evidence-badge ' + e.type + '" style="margin-right:4px;">' + e.type.replace('_','-') + '</span>';
    html += e.name + '</span>';
  });
  html += '</div>';
}
```

- [ ] **Step 2: Commit**

---

## Task 12: Integration test

- [ ] **Step 1: Restart server**
- [ ] **Step 2: Verify endpoints**

```bash
curl -s http://localhost:8202/api/map/evidence | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Total evidence: {len(d[\"evidence\"])}')"
curl -s "http://localhost:8202/api/map/evidence/connections?event=great_flood" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Flood connections: {len(d[\"pins\"])}')"
curl -s http://localhost:8202/api/map/evidence/gilgamesh_flood | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['name'])"
```

- [ ] **Step 3: Test in browser** — map tab, evidence control panel, pin clicks, connection lines, search
- [ ] **Step 4: Commit any fixes**

---

## Task Summary

| Task | Description |
|------|-------------|
| 1 | Create evidence.json — biblical events + archaeological entries (~40-50) |
| 2 | Add cross-cultural flood narratives (~50-60) |
| 3 | Add cross-cultural non-flood entries (~50-75) |
| 4 | Add inscription & artifact entries (~30-40) |
| 5 | Create evidence_service.py |
| 6 | Add evidence API endpoints to main.py |
| 7 | Update unified search with evidence |
| 8 | Frontend CSS + control panel HTML |
| 9 | Frontend evidence state, loading, pin rendering |
| 10 | Frontend popup + connection lines |
| 11 | Frontend evidence in search results |
| 12 | Integration test |
