"""Verse lookup and search for Trials of Judah."""


class VerseService:

    async def get_categories(self, db, type_filter: str = None) -> list:
        """Get all categories, optionally filtered by type."""
        if type_filter:
            rows = await db.execute(
                "SELECT id, name, slug, type, description, icon, sort_order "
                "FROM categories WHERE type=? ORDER BY sort_order",
                (type_filter,)
            )
        else:
            rows = await db.execute(
                "SELECT id, name, slug, type, description, icon, sort_order "
                "FROM categories ORDER BY sort_order"
            )
        return [dict(r) for r in rows]

    async def get_verses(self, db, category_slug: str, translation: str = "kjv") -> list:
        """Get all verses for a category in the specified translation."""
        rows = await db.execute(
            """SELECT v.id, v.book, v.chapter, v.verse_start, v.verse_end,
                      v.reference, v.context_note, v.date_written, vt.text
               FROM verses v
               JOIN categories c ON v.category_id = c.id
               JOIN verse_texts vt ON vt.verse_id = v.id
               JOIN translations t ON vt.translation_id = t.id
               WHERE c.slug = ? AND t.code = ?
               ORDER BY v.id""",
            (category_slug, translation)
        )
        return [dict(r) for r in rows]

    async def search_verses(self, db, keywords: list, translation: str = "kjv", limit: int = 30) -> list:
        """Search verses by keywords for LLM candidate narrowing."""
        if not keywords:
            rows = await db.execute(
                """SELECT v.id, v.reference, v.book, v.chapter, v.verse_start,
                          v.verse_end, v.context_note, v.date_written, vt.text, c.name as category_name
                   FROM verses v
                   JOIN verse_texts vt ON vt.verse_id = v.id
                   JOIN translations t ON vt.translation_id = t.id
                   JOIN categories c ON v.category_id = c.id
                   WHERE t.code = ?
                   ORDER BY RANDOM() LIMIT ?""",
                (translation, limit)
            )
            return [dict(r) for r in rows]

        conditions = []
        params = []
        for kw in keywords:
            conditions.append(
                "(LOWER(vt.text) LIKE ? OR LOWER(v.book) LIKE ? "
                "OR LOWER(v.reference) LIKE ? OR LOWER(v.context_note) LIKE ? "
                "OR LOWER(c.name) LIKE ? OR LOWER(c.description) LIKE ?)"
            )
            like = f"%{kw.lower()}%"
            params.extend([like] * 6)

        where_clause = " OR ".join(conditions)
        params.extend([translation, limit])

        rows = await db.execute(
            f"""SELECT v.id, v.reference, v.book, v.chapter, v.verse_start,
                       v.verse_end, v.context_note, vt.text, c.name as category_name
                FROM verses v
                JOIN verse_texts vt ON vt.verse_id = v.id
                JOIN translations t ON vt.translation_id = t.id
                JOIN categories c ON v.category_id = c.id
                WHERE ({where_clause}) AND t.code = ?
                LIMIT ?""",
            tuple(params)
        )
        # Rank by keyword match count
        results = [dict(r) for r in rows]
        for r in results:
            searchable = (r.get("text", "") + " " + r.get("category_name", "")).lower()
            r["_score"] = sum(1 for kw in keywords if kw.lower() in searchable)
        results.sort(key=lambda x: x["_score"], reverse=True)
        for r in results:
            del r["_score"]
        return results

    async def get_verse_by_reference(self, db, book: str, chapter: int, verse_start: int,
                                      translation: str = "kjv") -> dict | None:
        """Look up a single verse by reference. Used by watchdog."""
        rows = await db.execute(
            """SELECT v.id, v.reference, vt.text
               FROM verses v
               JOIN verse_texts vt ON vt.verse_id = v.id
               JOIN translations t ON vt.translation_id = t.id
               WHERE LOWER(v.book) = LOWER(?) AND v.chapter = ? AND v.verse_start = ? AND t.code = ?""",
            (book, chapter, verse_start, translation)
        )
        if rows:
            return dict(rows[0])
        return None

    async def get_all_verse_texts(self, db, translation: str = "kjv") -> list:
        """Get all verse texts for watchdog fuzzy matching."""
        rows = await db.execute(
            """SELECT v.reference, vt.text
               FROM verses v
               JOIN verse_texts vt ON vt.verse_id = v.id
               JOIN translations t ON vt.translation_id = t.id
               WHERE t.code = ?""",
            (translation,)
        )
        return [dict(r) for r in rows]


verse_service = VerseService()
