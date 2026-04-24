"""SQLite database for Trials of Judah."""
import aiosqlite
from pathlib import Path
from backend.config import DB_PATH

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('trial', 'guidance')),
    description TEXT NOT NULL,
    icon TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS translations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS verses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    book TEXT NOT NULL,
    chapter INTEGER NOT NULL,
    verse_start INTEGER NOT NULL,
    verse_end INTEGER,
    reference TEXT NOT NULL,
    context_note TEXT,
    date_written TEXT
);

CREATE TABLE IF NOT EXISTS verse_texts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    verse_id INTEGER NOT NULL REFERENCES verses(id),
    translation_id INTEGER NOT NULL REFERENCES translations(id),
    text TEXT NOT NULL,
    UNIQUE(verse_id, translation_id)
);

CREATE INDEX IF NOT EXISTS idx_verses_category ON verses(category_id);
CREATE INDEX IF NOT EXISTS idx_verse_texts_verse ON verse_texts(verse_id);
CREATE INDEX IF NOT EXISTS idx_categories_type ON categories(type);

INSERT OR IGNORE INTO translations (code, name) VALUES ('kjv', 'King James Version');
INSERT OR IGNORE INTO translations (code, name) VALUES ('esv', 'English Standard Version');

CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_english TEXT NOT NULL,
    name_hebrew TEXT,
    name_meaning TEXT,
    meaning_connection TEXT,
    generation INTEGER NOT NULL,
    birth_year_am INTEGER,
    death_year_am INTEGER,
    lifespan INTEGER,
    branch TEXT NOT NULL DEFAULT 'trunk',
    life_summary TEXT,
    scripture_refs TEXT,
    sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS parent_child (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER NOT NULL REFERENCES persons(id),
    child_id INTEGER NOT NULL REFERENCES persons(id),
    UNIQUE(parent_id, child_id)
);

CREATE TABLE IF NOT EXISTS spouses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL REFERENCES persons(id),
    spouse_id INTEGER NOT NULL REFERENCES persons(id),
    UNIQUE(person_id, spouse_id)
);

CREATE TABLE IF NOT EXISTS modern_connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL REFERENCES persons(id),
    modern_group TEXT NOT NULL,
    region TEXT,
    source TEXT,
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_persons_generation ON persons(generation);
CREATE INDEX IF NOT EXISTS idx_persons_branch ON persons(branch);
CREATE INDEX IF NOT EXISTS idx_parent_child_parent ON parent_child(parent_id);
CREATE INDEX IF NOT EXISTS idx_parent_child_child ON parent_child(child_id);
CREATE INDEX IF NOT EXISTS idx_spouses_person ON spouses(person_id);
CREATE INDEX IF NOT EXISTS idx_modern_connections_person ON modern_connections(person_id);

CREATE TABLE IF NOT EXISTS bible_kjv (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book TEXT NOT NULL,
    chapter INTEGER NOT NULL,
    verse INTEGER NOT NULL,
    text TEXT NOT NULL,
    UNIQUE(book, chapter, verse)
);

CREATE INDEX IF NOT EXISTS idx_bible_kjv_book ON bible_kjv(book);
CREATE INDEX IF NOT EXISTS idx_bible_kjv_ref ON bible_kjv(book, chapter);

CREATE TABLE IF NOT EXISTS prophecies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    prophecy_text TEXT,
    prophecy_refs TEXT,
    prophecy_date_approx TEXT,
    fulfillment_text TEXT,
    fulfillment_refs TEXT,
    fulfillment_date_approx TEXT,
    fulfillment_year INTEGER,
    prophecy_year INTEGER,
    status TEXT NOT NULL DEFAULT 'fulfilled',
    modern_status TEXT,
    summary TEXT,
    sort_order INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS cultural_evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prophecy_id INTEGER NOT NULL REFERENCES prophecies(id),
    culture TEXT NOT NULL,
    source_name TEXT NOT NULL,
    source_location TEXT,
    description TEXT,
    date_approx TEXT
);

CREATE TABLE IF NOT EXISTS prophecy_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prophecy_id INTEGER NOT NULL REFERENCES prophecies(id),
    tag TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_prophecies_category ON prophecies(category);
CREATE INDEX IF NOT EXISTS idx_prophecies_status ON prophecies(status);
CREATE INDEX IF NOT EXISTS idx_prophecies_year ON prophecies(fulfillment_year);
CREATE INDEX IF NOT EXISTS idx_cultural_evidence_prophecy ON cultural_evidence(prophecy_id);
CREATE INDEX IF NOT EXISTS idx_prophecy_tags_prophecy ON prophecy_tags(prophecy_id);
CREATE INDEX IF NOT EXISTS idx_prophecy_tags_tag ON prophecy_tags(tag);
"""


class Database:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._conn = None

    async def init(self):
        self._conn = await aiosqlite.connect(self.db_path)
        self._conn.row_factory = aiosqlite.Row
        await self._conn.executescript(SCHEMA_SQL)
        await self._conn.commit()

    async def close(self):
        if self._conn:
            await self._conn.close()
            self._conn = None

    async def execute(self, sql: str, params: tuple = ()):
        cursor = await self._conn.execute(sql, params)
        if sql.strip().upper().startswith("SELECT"):
            return await cursor.fetchall()
        await self._conn.commit()
        return await cursor.fetchall()

    async def execute_insert(self, sql: str, params: tuple = ()) -> int:
        cursor = await self._conn.execute(sql, params)
        await self._conn.commit()
        return cursor.lastrowid

    async def execute_many(self, sql: str, params_list: list):
        await self._conn.executemany(sql, params_list)
        await self._conn.commit()


db = Database()
