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

    async def _rewrite_psalm_ref(self, db, row: dict, translation: str) -> dict:
        """If the row is a Psalm and translation is DRA, rewrite chapter/verse/reference
        to match DRA numbering. No-op for other translations and other books.

        Edge case: for curated ranges that cross a DRA chapter boundary within
        KJV Psalms 116 or 147 (e.g. KJV Ps 116:5-15, which spans DRA 114 and 115),
        only the start verse determines the DRA chapter. This is rare in curated
        data; if a genuine cross-boundary reference appears, split it into two
        curated rows rather than extending this logic.
        """
        if translation != "dra" or row.get("book") != "Psalms":
            return row
        chapter = row["chapter"]
        vs = row["verse_start"]
        ve_raw = row.get("verse_end")
        ve = ve_raw if ve_raw is not None else vs

        mapping = await db.execute(
            """SELECT dra_chapter, verse_offset FROM psalm_numbering
               WHERE kjv_chapter=? AND kjv_verse_min<=? AND kjv_verse_max>=?""",
            (chapter, vs, vs)
        )
        if not mapping:
            return row
        dra_chapter, offset = mapping[0][0], mapping[0][1]
        dra_vs = vs + offset
        dra_ve = ve + offset

        row["chapter"] = dra_chapter
        row["verse_start"] = dra_vs
        row["verse_end"] = (ve + offset) if ve_raw is not None else None
        if dra_vs == dra_ve:
            row["reference"] = f"Psalm {dra_chapter}:{dra_vs}"
        else:
            row["reference"] = f"Psalm {dra_chapter}:{dra_vs}-{dra_ve}"

        # Defensive: log if curated range crosses DRA chapter boundary (KJV Ps 116/147).
        if ve_raw is not None and ve_raw != vs:
            end_mapping = await db.execute(
                """SELECT dra_chapter FROM psalm_numbering
                   WHERE kjv_chapter=? AND kjv_verse_min<=? AND kjv_verse_max>=?""",
                (chapter, ve_raw, ve_raw)
            )
            if end_mapping and end_mapping[0][0] != dra_chapter:
                print(f"[verse_service] WARNING: curated Psalm range KJV {chapter}:{vs}-{ve_raw} "
                      f"crosses DRA chapter boundary (start→DRA {dra_chapter}, end→DRA {end_mapping[0][0]}). "
                      f"Reference shown uses start's DRA chapter only.")
        return row

    async def get_verses(self, db, category_slug: str, translation: str = "dra") -> list:
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
        result = [dict(r) for r in rows]
        return [await self._rewrite_psalm_ref(db, r, translation) for r in result]

    async def search_verses(self, db, keywords: list, translation: str = "dra", limit: int = 30) -> list:
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
            result = [dict(r) for r in rows]
            return [await self._rewrite_psalm_ref(db, r, translation) for r in result]

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
        results = [dict(r) for r in rows]
        for r in results:
            searchable = (r.get("text", "") + " " + r.get("category_name", "")).lower()
            r["_score"] = sum(1 for kw in keywords if kw.lower() in searchable)
        results.sort(key=lambda x: x["_score"], reverse=True)
        for r in results:
            del r["_score"]
        return [await self._rewrite_psalm_ref(db, r, translation) for r in results]

    async def get_verse_by_reference(self, db, book: str, chapter: int, verse_start: int,
                                      translation: str = "dra") -> dict | None:
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

    async def get_all_verse_texts(self, db, translation: str = "dra") -> list:
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
