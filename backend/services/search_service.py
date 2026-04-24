"""Unified search across Bible, lineage, prophecies, and map."""
from backend.services.map_service import map_service
from backend.services.evidence_service import evidence_service
from backend.services.martyrs_service import martyrs_service


def _bible_table(translation: str) -> str:
    """Map a translation code to its full-text table name. Defaults to DRA."""
    return {"kjv": "bible_kjv", "dra": "bible_dra"}.get(translation, "bible_dra")


class SearchService:

    async def search(self, db, query: str, translation: str = "dra") -> dict:
        """Search across all data types."""
        q = f"%{query.lower()}%"
        table = _bible_table(translation)

        bible = await db.execute(
            f"""SELECT book, chapter, verse, text FROM {table}
                WHERE LOWER(text) LIKE ? LIMIT 10""", (q,))

        persons = await db.execute(
            """SELECT id, name_english, name_hebrew, name_meaning, generation
               FROM persons WHERE LOWER(name_english) LIKE ? LIMIT 10""", (q,))

        prophecies = await db.execute(
            """SELECT id, title, category, summary, status FROM prophecies
               WHERE LOWER(title) LIKE ? OR LOWER(fulfillment_text) LIKE ?
               OR LOWER(prophecy_text) LIKE ? LIMIT 10""", (q, q, q))

        map_results = map_service.search(query)
        evidence_results = evidence_service.search(query)
        martyrs_results = martyrs_service.search(query)

        return {
            "bible_verses": [dict(r) for r in bible],
            "persons": [dict(r) for r in persons],
            "prophecies": [dict(r) for r in prophecies],
            "map_kingdoms": map_results["kingdoms"],
            "map_cities": map_results["cities"],
            "map_peoples": map_results["peoples"],
            "map_evidence": evidence_results,
            "map_martyrs": martyrs_results,
        }


search_service = SearchService()
