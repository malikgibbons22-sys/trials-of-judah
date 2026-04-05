"""Lineage data queries for Trials of Judah."""


class LineageService:

    async def get_tree(self, db) -> dict:
        """Return full tree structure: nodes + edges."""
        nodes = await db.execute(
            """SELECT id, name_english, name_hebrew, name_meaning,
                      generation, branch, sort_order
               FROM persons ORDER BY generation, sort_order"""
        )
        edges = await db.execute(
            "SELECT parent_id, child_id FROM parent_child"
        )
        return {
            "nodes": [dict(r) for r in nodes],
            "edges": [dict(r) for r in edges],
        }

    async def get_timeline(self, db) -> dict:
        """Return persons ordered by generation with era markers."""
        persons = await db.execute(
            """SELECT id, name_english, name_meaning, generation, branch, birth_year_am
               FROM persons ORDER BY generation, sort_order"""
        )
        eras = [
            {"name": "Creation", "generation_start": 1, "generation_end": 1},
            {"name": "Pre-Flood Patriarchs", "generation_start": 2, "generation_end": 9},
            {"name": "The Flood", "generation_start": 10, "generation_end": 10},
            {"name": "Table of Nations", "generation_start": 11, "generation_end": 14},
            {"name": "Post-Babel Patriarchs", "generation_start": 15, "generation_end": 19},
            {"name": "The Patriarchs", "generation_start": 20, "generation_end": 22},
            {"name": "Twelve Tribes", "generation_start": 23, "generation_end": 24},
            {"name": "United Kingdom", "generation_start": 25, "generation_end": 34},
            {"name": "Divided Kingdom & Exile", "generation_start": 35, "generation_end": 48},
            {"name": "Return & Intertestamental", "generation_start": 49, "generation_end": 59},
            {"name": "The Messiah", "generation_start": 60, "generation_end": 67},
        ]
        return {
            "eras": eras,
            "persons": [dict(r) for r in persons],
        }

    async def get_person(self, db, person_id: int) -> dict | None:
        """Return full detail for one person."""
        rows = await db.execute(
            "SELECT * FROM persons WHERE id=?", (person_id,)
        )
        if not rows:
            return None
        person = dict(rows[0])

        parents = await db.execute(
            """SELECT p.id, p.name_english FROM persons p
               JOIN parent_child pc ON pc.parent_id = p.id
               WHERE pc.child_id = ?""",
            (person_id,)
        )
        children = await db.execute(
            """SELECT p.id, p.name_english FROM persons p
               JOIN parent_child pc ON pc.child_id = p.id
               WHERE pc.parent_id = ?
               ORDER BY p.sort_order""",
            (person_id,)
        )
        spouse_rows = await db.execute(
            """SELECT DISTINCT p.id, p.name_english FROM persons p
               JOIN spouses s ON (s.spouse_id = p.id OR s.person_id = p.id)
               WHERE (s.person_id = ? OR s.spouse_id = ?) AND p.id != ?""",
            (person_id, person_id, person_id)
        )
        mc_rows = await db.execute(
            "SELECT modern_group, region, source, notes FROM modern_connections WHERE person_id=?",
            (person_id,)
        )

        # Map location from modern_connections
        map_location = None
        if mc_rows:
            from backend.services.map_service import map_service
            for mc in mc_rows:
                region = dict(mc).get("region", "")
                if region:
                    results = map_service.search(region.split("(")[0].strip().split(",")[0].strip())
                    if results["kingdoms"]:
                        map_location = {
                            "kingdom_id": results["kingdoms"][0]["id"],
                            "kingdom_name": results["kingdoms"][0]["name"],
                        }
                        break

        return {
            "person": person,
            "parents": [dict(r) for r in parents],
            "children": [dict(r) for r in children],
            "spouses": [dict(r) for r in spouse_rows],
            "modern_connections": [dict(r) for r in mc_rows],
            "map_location": map_location,
        }

    async def search_persons(self, db, query: str = None, branch: str = None,
                              generation: int = None) -> list:
        """Search/filter persons."""
        conditions = []
        params = []
        if query:
            conditions.append("LOWER(name_english) LIKE ?")
            params.append(f"%{query.lower()}%")
        if branch:
            conditions.append("branch = ?")
            params.append(branch)
        if generation is not None:
            conditions.append("generation = ?")
            params.append(generation)

        where = " AND ".join(conditions) if conditions else "1=1"
        rows = await db.execute(
            f"""SELECT id, name_english, name_hebrew, name_meaning,
                       generation, branch, sort_order
                FROM persons WHERE {where} ORDER BY generation, sort_order""",
            tuple(params)
        )
        return [dict(r) for r in rows]


lineage_service = LineageService()
