# Book of Enoch Study Section — Design Spec

## Overview

A standalone page within the Trials of Judah app dedicated to the study of the Book of Enoch. The central thesis: the Book of Enoch should be considered canonical and accurately explains pre-flood history — who the ancient gods were, where humanity learned the trades, how mythological beings were created, and how they existed on earth.

The section is **not integrated into the main tab navigation** to avoid conflicting with canonical scripture study. It lives at `/enoch` as a separate HTML page and can be linked in when ready.

## Content Structure

### Disclaimer

Fixed top banner (dismissable):

> "This section explores the Book of Enoch as a historical and theological document. All claims are cross-referenced with canonical scripture where applicable. Study with discernment — test all things (1 Thessalonians 5:21)."

Scripture cross-references appear throughout every entry. Where canonical support is absent, this is honestly noted.

### Part 1 — The Case for Canon

A vertical timeline of evidence cards building the argument for Enoch's canonicity. Cards expand on click to reveal full quotes, historical context, and images. A connecting line runs between them to show the argument's progression.

**Evidence cards (in order):**

1. **Dead Sea Scrolls** — 11 copies of 1 Enoch found at Qumran, more than most canonical Old Testament books. Aramaic fragments dating to 3rd-1st century BC.
2. **Jude 1:14-15** — Directly quotes 1 Enoch 1:9. A canonical book treating Enoch as authoritative prophecy.
3. **2 Peter 2:4** — Parallels Enoch's account of the Watchers' imprisonment in chains of darkness.
4. **Genesis 6:1-4** — The canonical passage Enoch expands on. "Sons of God" and the Nephilim.
5. **Ethiopian Orthodox Canon** — Never removed it. Part of their Bible for 2,000+ years.
6. **Early Church Fathers** — Tertullian, Irenaeus, Clement of Alexandria, Justin Martyr all cited or referenced Enoch.
7. **Why It Was Removed** — Council decisions, political motivations, and the theological discomfort that led to exclusion from Western canons.

Each card contains:
- Primary source quote
- Source citation
- Canonical cross-references (array of verses)
- Historical context paragraph
- Images (manuscript photos, scroll fragments)

### Part 2 — The Parallels

Eight mythology regions, each containing multiple deep study entries showing how the Book of Enoch's account was echoed, distorted, and deified across world civilizations.

**Categories:**

1. **Mesopotamian** (Sumerian/Babylonian)
2. **Greek**
3. **Egyptian**
4. **Norse**
5. **Hindu**
6. **Native American / Mesoamerican**
7. **African**
8. **East Asian**

**Example entries per category:**

- **Mesopotamian:** The Watchers and the Anunnaki; Azazel and Enki (forbidden knowledge); The Nephilim and the Apkallu; The Flood of Enoch and the Epic of Gilgamesh
- **Greek:** The Watchers and the Titans; The Nephilim and the Demigods (Hercules, Achilles); Azazel and Prometheus; Imprisonment of the Watchers and Tartarus
- **Egyptian:** Thoth and the forbidden arts; The Ogdoad and the pre-flood world; Osiris and the Watcher narrative
- **Norse:** Jotnar (giants) and the Nephilim; Odin's pursuit of forbidden knowledge; Ragnarok and the flood/judgment parallel
- **Hindu:** Devas/Asuras and the Watchers; Vedic giants and the Nephilim; Rishis and the Watchers' forbidden instruction
- **Native American / Mesoamerican:** Sky beings who descended and taught mankind; Giant traditions across tribes; Flood narratives
- **African:** Fallen sky spirits in oral tradition; Giant beings in ancestral memory; Knowledge bringers from above
- **East Asian:** Chinese flood myths and Enoch's flood; Divine teachers descending to earth; Giant traditions

### Deep Study Entry Template

Each entry follows this structure:

- **Title** — e.g., "The Watchers and the Anunnaki"
- **The Claim** — One thesis statement
- **From Enoch** — Direct quotes with chapter/verse references
- **From the Mythology** — Direct quotes or paraphrased accounts from mythological source texts with citations
- **Side-by-Side Comparison** — Two-column layout highlighting parallel details
- **Images** — Ancient artwork, carvings, seals, artifacts with captions and attribution
- **Canonical Cross-References** — Supporting verses from Genesis, Jude, 2 Peter, Job, Isaiah, etc.
- **Canonical Gaps** — Honestly noted where canonical support is thin (nullable)
- **The Distortion** — Analysis of how Enoch's original account was twisted, deified, or fragmented through cultural transmission
- **Key Takeaway** — Summary paragraph of what this parallel demonstrates

## Data Architecture

### Files (in `backend/data/`)

**`enoch_canon.json`**
```json
[
  {
    "id": "dead-sea-scrolls",
    "title": "Dead Sea Scrolls",
    "summary": "11 copies found at Qumran...",
    "primary_source_quote": "...",
    "source_citation": "...",
    "canonical_refs": [
      {"verse": "Jude 1:14", "text": "...", "relevance": "..."}
    ],
    "historical_context": "...",
    "images": ["qumran-cave4", "enoch-fragment-4q201"],
    "order": 1
  }
]
```

**`enoch_parallels.json`**
```json
[
  {
    "id": "watchers-anunnaki",
    "category": "mesopotamian",
    "title": "The Watchers and the Anunnaki",
    "claim": "The Sumerian Anunnaki — 'those who from heaven came down' — are the same beings Enoch identifies as the Watchers.",
    "enoch_quotes": [
      {"text": "...", "reference": "1 Enoch 6:1-2"}
    ],
    "mythology_quotes": [
      {"text": "...", "source": "Enuma Elish", "citation": "Tablet I, lines 1-20"}
    ],
    "side_by_side": [
      {"enoch_point": "200 Watchers descend on Mount Hermon", "mythology_point": "Anunnaki descend from heaven to earth"}
    ],
    "canonical_refs": [
      {"verse": "Genesis 6:2", "text": "...", "relevance_note": "..."}
    ],
    "canonical_gaps": null,
    "distortion_analysis": "...",
    "key_takeaway": "...",
    "images": ["cylinder-seal-anunnaki", "hermon-site"],
    "tags": ["watchers", "descent", "divine-beings"]
  }
]
```

**`enoch_images.json`**
```json
[
  {
    "id": "qumran-cave4",
    "filename": "qumran-cave4.jpg",
    "source": "Wikimedia Commons",
    "attribution": "Public domain",
    "license": "CC0",
    "caption": "Cave 4 at Qumran where 11 copies of 1 Enoch were discovered",
    "related_entry_ids": ["dead-sea-scrolls"]
  }
]
```

### Image Directory

`backend/data/images/enoch/`

Images are dropped into this directory and registered in `enoch_images.json`. The manifest maps image IDs to filenames, sources, attribution, and captions. Adding a new image requires only placing the file and adding one entry to the manifest.

## API Endpoints

All under `/api/enoch/`:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/enoch/canon` | Returns all canonicity evidence cards, ordered |
| GET | `/api/enoch/parallels` | Returns all parallel entries. Optional `?category=` filter |
| GET | `/api/enoch/categories` | Returns the 8 mythology regions with labels and icons |
| GET | `/api/enoch/images/{filename}` | Serves an image from the enoch images directory |

## Frontend

### Page

Separate `enoch.html` served at route `/enoch` from the trialsofjudah backend.

### Aesthetic

- Darker, more ancient scholarly feel than the main app
- Aged parchment textures on dark backgrounds
- Same gold accent (#c9a84c) to stay visually connected to Trials of Judah
- Georgia serif for quotes and scripture, system-ui for UI elements

### Header

- Title: "The Book of Enoch: The Ancient Record"
- Subtitle: "A study of the pre-flood world and its echoes across every civilization"
- Disclaimer banner beneath (dismissable)
- "Return to Trials of Judah" link in top corner

### Part 1 Layout

- Vertical timeline with connecting line
- Evidence cards stack vertically, expand on click
- Images float right within expanded cards
- Progress indicator on side showing position in argument

### Part 2 Layout

- Horizontal category navigation bar with culture labels
- Selecting a category loads that culture's deep study entries
- Each entry is full-width with:
  - Title and claim at top
  - Two-column side-by-side comparison (Enoch left, mythology right)
  - Images displayed between sections with captions and attribution
  - Canonical cross-references in Georgia serif (matching main app verse style)
  - "The Distortion" in a distinct callout block
  - Key takeaway in highlighted summary bar
- Entries stack vertically within a category

### Responsive

Single column on mobile. Side-by-side comparison collapses to stacked (Enoch above, mythology below).

## Future Additions (Not in Scope)

- Ollama AI integration for questions about Enoch parallels
- Search integration with main app's unified search
- Tab link from main navigation
- Interactive map layer showing where each mythology originated
