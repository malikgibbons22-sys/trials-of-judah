"""Prophecy queries for Trials of Judah."""


class ProphecyService:

    async def get_timeline(self, db) -> dict:
        prophecies = await db.execute(
            """SELECT id, title, category, summary, prophecy_year, fulfillment_year, status
               FROM prophecies ORDER BY COALESCE(fulfillment_year, 9999), sort_order"""
        )
        eras = [
            {"name": "Ancient History", "year_start": -2500, "year_end": -1500, "color": "#3d2b1f"},
            {"name": "Prophetic Era", "year_start": -1500, "year_end": -400, "color": "#722f37"},
            {"name": "Intertestamental", "year_start": -400, "year_end": -5, "color": "#5a4d40"},
            {"name": "Life of Christ", "year_start": -5, "year_end": 33, "color": "#c9a84c"},
            {"name": "Early Assembly", "year_start": 33, "year_end": 100, "color": "#a8a9ad"},
            {"name": "Post-Biblical", "year_start": 100, "year_end": 2026, "color": "#6b5d4f"},
            {"name": "Unfulfilled", "year_start": 2026, "year_end": None, "color": "transparent"},
        ]
        return {
            "eras": eras,
            "prophecies": [dict(r) for r in prophecies],
        }

    async def get_prophecy(self, db, prophecy_id: int) -> dict | None:
        rows = await db.execute("SELECT * FROM prophecies WHERE id=?", (prophecy_id,))
        if not rows:
            return None
        prophecy = dict(rows[0])
        evidence = await db.execute(
            """SELECT culture, source_name, source_location, description, date_approx
               FROM cultural_evidence WHERE prophecy_id=?""", (prophecy_id,))
        tags = await db.execute(
            "SELECT tag FROM prophecy_tags WHERE prophecy_id=?", (prophecy_id,))
        # Map location cross-reference
        map_location = None
        from backend.services.map_service import map_service
        title = prophecy.get("title", "") if isinstance(prophecy, dict) else ""
        search_result = map_service.search(title)
        if search_result["kingdoms"]:
            map_location = {
                "kingdom_id": search_result["kingdoms"][0]["id"],
                "kingdom_name": search_result["kingdoms"][0]["name"],
            }

        return {
            "prophecy": prophecy,
            "cultural_evidence": [dict(r) for r in evidence],
            "tags": [r[0] for r in tags],
            "map_location": map_location,
        }

    async def filter_prophecies(self, db, category=None, status=None, tag=None) -> list:
        conditions = []
        params = []
        if category:
            conditions.append("p.category = ?")
            params.append(category)
        if status:
            conditions.append("p.status = ?")
            params.append(status)
        if tag:
            conditions.append("p.id IN (SELECT prophecy_id FROM prophecy_tags WHERE tag = ?)")
            params.append(tag)
        where = " AND ".join(conditions) if conditions else "1=1"
        rows = await db.execute(
            f"""SELECT p.id, p.title, p.category, p.summary, p.fulfillment_year, p.status
                FROM prophecies p WHERE {where}
                ORDER BY COALESCE(p.fulfillment_year, 9999), p.sort_order""",
            tuple(params))
        return [dict(r) for r in rows]

    async def get_categories(self, db) -> list:
        rows = await db.execute(
            """SELECT category, COUNT(*) as count FROM prophecies
               GROUP BY category ORDER BY category""")
        return [{"name": r[0], "count": r[1]} for r in rows]


prophecy_service = ProphecyService()
