# Martyrs Layer — Design Spec

## Overview

Add a martyrs layer to the Biblical Kingdoms Map showing 300+ church-approved martyrs plotted at their location of martyrdom. Crimson cross pins, integrated with the era slider, with detail popups including method of martyrdom, life summary, artwork from Wikimedia Commons, and church approval source.

## Data Structure

New file: `backend/data/martyrs.json`

```json
{
  "martyrs": [
    {
      "id": "stephen_protomartyr",
      "name": "Saint Stephen",
      "title": "Protomartyr, First Deacon",
      "lat": 31.78,
      "lng": 35.24,
      "location": "Jerusalem",
      "date_of_death": "~AD 34",
      "year_of_death": 34,
      "era_id": "early_church",
      "method": "Stoned to death",
      "description": "Stephen was one of the seven deacons chosen by the Apostles. Filled with the Holy Spirit, he performed great wonders and spoke with irrefutable wisdom. Brought before the Sanhedrin on false charges of blasphemy, he delivered a powerful speech recounting Israel's history and accusing the council of resisting the Holy Spirit. As they stoned him, he saw heaven opened and Jesus standing at the right hand of God. His last words echoed Christ's: 'Lord, lay not this sin to their charge.'",
      "scripture_refs": ["Acts 6:1-8:2", "Acts 7:54-60"],
      "feast_day": "December 26 (Western) / December 27 (Eastern)",
      "approved_by": "Catholic, Orthodox",
      "approval_source": "Roman Martyrology, Orthodox Synaxarion",
      "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Rembrandt_-_The_Stoning_of_Saint_Stephen_-_Google_Art_Project.jpg/800px-Rembrandt_-_The_Stoning_of_Saint_Stephen_-_Google_Art_Project.jpg",
      "image_attribution": "Rembrandt, 'The Stoning of Saint Stephen' (1625), Museum of Fine Arts, Lyon"
    }
  ]
}
```

## Pin Visual

- Crimson/red cross icon (#8B0000 dark red circle with white cross)
- Size: 22px (standard), 26px for Apostles/major saints
- White border, drop shadow (matching evidence pin style)
- Distinct from evidence pins (cross shape vs circle icons)

## UI Controls

Add to the existing evidence control panel OR create a separate "Martyrs" collapsible panel below it:

```
[Martyrs ▼]
  [x] Show Martyrs (312)
  [ ] Show All Eras
```

## Popup Detail

- Name and title
- Feast day
- Church approval badges (Catholic / Orthodox / Both)
- Location and date
- Method of martyrdom (factual, one sentence)
- Life description (3-5 sentences)
- Artwork image (from Wikimedia Commons, with attribution)
- Scripture references

## Era Mapping

Each martyr has a `year_of_death` and `era_id`. The era slider filters visible martyrs. "Show All Eras" shows all.

## Artwork (Wikimedia Commons)

- `image_url`: Direct link to Wikimedia Commons image (public domain, pre-1900 artwork preferred)
- `image_attribution`: Artist name, painting title, year, museum/collection
- Null for martyrs without known artwork (many medieval/modern martyrs)
- Images loaded in popup on click (not pre-loaded)

## Backend

- New service: `backend/services/martyrs_service.py`
- New endpoints: `/api/map/martyrs`, `/api/map/martyrs/{id}`
- Martyrs included in unified search under `"map_martyrs"` key

## Data Sources

- Roman Martyrology (Martyrologium Romanum) — official Catholic list
- Orthodox Synaxarion — Eastern Orthodox calendar of saints
- Butler's Lives of the Saints — biographical reference
- Foxe's Book of Martyrs — Protestant martyrology

## Image Fields (Retroactive)

Add `image_url` and `image_attribution` fields to:
- Evidence entries in evidence.json (archaeological artifacts, inscriptions)
- City entries in kingdoms.json (major archaeological sites)
