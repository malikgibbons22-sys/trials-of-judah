"""Seed the Trials of Judah database from verses.json, lineage.json, and kjv_bible.json."""
import json
from pathlib import Path


async def seed(db):
    """Populate database from verses.json. Idempotent — skips if data exists."""
    existing = await db.execute("SELECT COUNT(*) FROM categories")
    if existing and existing[0][0] > 0:
        return False

    data_file = Path(__file__).parent / "verses.json"
    if not data_file.exists():
        print("[Seed] verses.json not found — skipping seed.")
        return False

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    trans_rows = await db.execute("SELECT id, code FROM translations")
    trans_map = {r[1]: r[0] for r in trans_rows}

    for i, cat in enumerate(data["categories"]):
        cat_id = await db.execute_insert(
            """INSERT INTO categories (name, slug, type, description, icon, sort_order)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (cat["name"], cat["slug"], cat["type"], cat["description"], cat["icon"], i)
        )

        for verse in cat["verses"]:
            verse_id = await db.execute_insert(
                """INSERT INTO verses (category_id, book, chapter, verse_start, verse_end, reference, context_note, date_written)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (cat_id, verse["book"], verse["chapter"], verse["verse_start"],
                 verse.get("verse_end"), verse["reference"], verse.get("context_note"), verse.get("date_written"))
            )

            if "kjv" in verse and "kjv" in trans_map:
                await db.execute_insert(
                    "INSERT INTO verse_texts (verse_id, translation_id, text) VALUES (?, ?, ?)",
                    (verse_id, trans_map["kjv"], verse["kjv"])
                )

            if "esv" in verse and "esv" in trans_map:
                await db.execute_insert(
                    "INSERT INTO verse_texts (verse_id, translation_id, text) VALUES (?, ?, ?)",
                    (verse_id, trans_map["esv"], verse["esv"])
                )

    return True


async def seed_lineage(db):
    """Populate lineage data from lineage.json. Idempotent."""
    existing = await db.execute("SELECT COUNT(*) FROM persons")
    if existing and existing[0][0] > 0:
        return False

    data_file = Path(__file__).parent / "lineage.json"
    if not data_file.exists():
        print("[Seed] lineage.json not found — skipping lineage seed.")
        return False

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Insert all persons first
    name_to_id = {}
    for p in data["persons"]:
        pid = await db.execute_insert(
            """INSERT INTO persons (name_english, name_hebrew, name_meaning,
               meaning_connection, generation, birth_year_am, death_year_am,
               lifespan, branch, life_summary, scripture_refs, sort_order)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["name_english"], p.get("name_hebrew"), p.get("name_meaning"),
             p.get("meaning_connection"), p["generation"],
             p.get("birth_year_am"), p.get("death_year_am"), p.get("lifespan"),
             p["branch"], p.get("life_summary"), p.get("scripture_refs"),
             p.get("sort_order", 0))
        )
        name_to_id[p["name_english"]] = pid

    # Insert parent-child relationships
    for p in data["persons"]:
        parent_id = name_to_id.get(p["name_english"])
        if not parent_id:
            continue
        for child_name in p.get("children", []):
            child_id = name_to_id.get(child_name)
            if child_id:
                await db.execute_insert(
                    "INSERT OR IGNORE INTO parent_child (parent_id, child_id) VALUES (?, ?)",
                    (parent_id, child_id)
                )

    # Insert spouse relationships (single direction — lower ID first)
    for p in data["persons"]:
        person_id = name_to_id.get(p["name_english"])
        if not person_id:
            continue
        for spouse_name in p.get("spouses", []):
            spouse_id = name_to_id.get(spouse_name)
            if spouse_id:
                lo, hi = min(person_id, spouse_id), max(person_id, spouse_id)
                await db.execute_insert(
                    "INSERT OR IGNORE INTO spouses (person_id, spouse_id) VALUES (?, ?)",
                    (lo, hi)
                )

    # Insert modern connections
    for mc in data.get("modern_connections", []):
        person_id = name_to_id.get(mc["person_name"])
        if person_id:
            await db.execute_insert(
                """INSERT INTO modern_connections (person_id, modern_group, region, source, notes)
                   VALUES (?,?,?,?,?)""",
                (person_id, mc["modern_group"], mc.get("region"),
                 mc.get("source"), mc.get("notes"))
            )

    return True


async def seed_bible_kjv(db):
    """Seed the full KJV Bible text. Idempotent."""
    existing = await db.execute("SELECT COUNT(*) FROM bible_kjv")
    if existing and existing[0][0] > 0:
        return False

    data_file = Path(__file__).parent / "kjv_bible.json"
    if not data_file.exists():
        print("[Seed] kjv_bible.json not found — skipping Bible seed.")
        return False

    with open(data_file, "r", encoding="utf-8") as f:
        verses = json.load(f)

    # Batch insert for performance
    batch = []
    for v in verses:
        batch.append((v["book"], v["chapter"], v["verse"], v["text"]))
        if len(batch) >= 500:
            await db.execute_many(
                "INSERT OR IGNORE INTO bible_kjv (book, chapter, verse, text) VALUES (?,?,?,?)",
                batch
            )
            batch = []
    if batch:
        await db.execute_many(
            "INSERT OR IGNORE INTO bible_kjv (book, chapter, verse, text) VALUES (?,?,?,?)",
            batch
        )

    return True


async def seed_prophecies(db):
    """Seed prophecy data from prophecies.json. Idempotent."""
    existing = await db.execute("SELECT COUNT(*) FROM prophecies")
    if existing and existing[0][0] > 0:
        return False

    data_file = Path(__file__).parent / "prophecies.json"
    if not data_file.exists():
        print("[Seed] prophecies.json not found — skipping prophecy seed.")
        return False

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    title_to_id = {}
    for p in data["prophecies"]:
        pid = await db.execute_insert(
            """INSERT INTO prophecies (title, category, prophecy_text, prophecy_refs,
               prophecy_date_approx, fulfillment_text, fulfillment_refs,
               fulfillment_date_approx, fulfillment_year, prophecy_year,
               status, modern_status, summary, sort_order)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["title"], p["category"], p.get("prophecy_text"), p.get("prophecy_refs"),
             p.get("prophecy_date_approx"), p.get("fulfillment_text"), p.get("fulfillment_refs"),
             p.get("fulfillment_date_approx"), p.get("fulfillment_year"), p.get("prophecy_year"),
             p.get("status", "fulfilled"), p.get("modern_status"), p.get("summary"),
             p.get("sort_order", 0))
        )
        title_to_id[p["title"]] = pid

        for tag in p.get("tags", []):
            await db.execute_insert(
                "INSERT INTO prophecy_tags (prophecy_id, tag) VALUES (?, ?)",
                (pid, tag)
            )

    for ce in data.get("cultural_evidence", []):
        pid = title_to_id.get(ce["prophecy_title"])
        if pid:
            await db.execute_insert(
                """INSERT INTO cultural_evidence (prophecy_id, culture, source_name,
                   source_location, description, date_approx)
                   VALUES (?,?,?,?,?,?)""",
                (pid, ce["culture"], ce["source_name"], ce.get("source_location"),
                 ce.get("description"), ce.get("date_approx"))
            )

    return True
