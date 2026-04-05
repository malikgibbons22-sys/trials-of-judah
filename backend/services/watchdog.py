"""Watchdog: verify LLM commentary against scripture database."""
import re
from difflib import SequenceMatcher

# Regex for Bible references: handles "1 Corinthians 13:4-7", "John 3:16",
# "Song of Solomon 2:16", "Psalm 37:8", etc.
REFERENCE_PATTERN = re.compile(
    r'(\d?\s?[A-Z][a-z]+(?:\s(?:of\s)?[A-Z][a-z]+)*)\s+(\d+):(\d+)(?:-(\d+))?'
)

# Extract quoted text — match text that appears to be a direct scripture quote.
# Uses a stricter pattern: starts with a capital letter after the opening quote,
# must be 50+ chars, and must not contain internal quote marks.
QUOTE_PATTERN = re.compile(r'(?:^|(?<=\s))["\u201c]([A-Z][^"\u201d\n]{50,})["\u201d]')

SIMILARITY_THRESHOLD = 0.85


class Watchdog:

    def extract_references(self, text: str) -> list:
        """Extract all Bible references from text."""
        matches = REFERENCE_PATTERN.findall(text)
        refs = []
        for match in matches:
            book = match[0].strip()
            chapter = int(match[1])
            verse_start = int(match[2])
            verse_end = int(match[3]) if match[3] else None
            refs.append({
                "book": book,
                "chapter": chapter,
                "verse_start": verse_start,
                "verse_end": verse_end,
                "raw": f"{book} {chapter}:{verse_start}" + (f"-{verse_end}" if verse_end else ""),
            })
        return refs

    def extract_quotes(self, text: str) -> list:
        """Extract quoted text that looks like scripture from commentary.

        Filters out Greek/Hebrew terms, word definitions, and short phrases
        that aren't actual scripture quotes.
        """
        raw = QUOTE_PATTERN.findall(text)
        filtered = []
        for q in raw:
            # Skip if contains Greek/Hebrew characters
            if re.search(r'[\u0370-\u03FF\u0590-\u05FF]', q):
                continue
            # Skip if it looks like a word definition (contains "means" or "refers to")
            if re.search(r'\bmeans\b|\brefers to\b|\bfreedom from\b|\bstate of\b', q.lower()):
                continue
            filtered.append(q)
        return filtered

    async def _check_verse_in_range(self, db, book: str, chapter: int, verse_num: int,
                                      translation: str = "kjv") -> bool:
        """Check if a verse number falls within a stored verse range.

        e.g., if DB has Galatians 5:19-21 and LLM references Galatians 5:21,
        this returns True.
        """
        rows = await db.execute(
            """SELECT v.verse_start, v.verse_end FROM verses v
               WHERE LOWER(v.book) = LOWER(?) AND v.chapter = ?
               AND v.verse_end IS NOT NULL
               AND v.verse_start <= ? AND v.verse_end >= ?""",
            (book, chapter, verse_num, verse_num)
        )
        return len(rows) > 0

    async def verify(self, commentary: str, db, translation: str = "kjv") -> dict:
        """Verify LLM commentary against the scripture database.

        Returns: {verified: bool, flags: [{type, reference, detail}]}
        """
        from backend.services.verse_service import verse_service

        flags = []

        # 1. Check all referenced verses exist in DB
        refs = self.extract_references(commentary)
        for ref in refs:
            found = await verse_service.get_verse_by_reference(
                db, ref["book"], ref["chapter"], ref["verse_start"], translation
            )
            # Fallback: check if the referenced verse falls within a stored range
            if not found:
                found = await self._check_verse_in_range(
                    db, ref["book"], ref["chapter"], ref["verse_start"], translation
                )
            if not found:
                flags.append({
                    "type": "unknown_reference",
                    "reference": ref["raw"],
                    "detail": f"Reference {ref['raw']} not found in the verse database.",
                })

        # 2. Check quoted text against DB verse texts
        quotes = self.extract_quotes(commentary)
        if quotes:
            all_texts = await verse_service.get_all_verse_texts(db, translation)
            for quote in quotes:
                best_score = 0
                best_ref = ""
                for vt in all_texts:
                    score = SequenceMatcher(None, quote.lower(), vt["text"].lower()).ratio()
                    if score > best_score:
                        best_score = score
                        best_ref = vt["reference"]
                if best_score < SIMILARITY_THRESHOLD:
                    flags.append({
                        "type": "misquote",
                        "reference": best_ref if best_score > 0.5 else "unknown",
                        "detail": f"Quoted text could not be verified (best match: {best_score:.0%} to {best_ref}).",
                    })

        return {
            "verified": len(flags) == 0,
            "flags": flags,
        }


    async def verify_quotes_only(self, commentary: str, db, translation: str = "kjv") -> dict:
        """Verify quoted text in lookup responses against the full KJV Bible.
        """
        flags = []
        quotes = self.extract_quotes(commentary)
        if quotes:
            for quote in quotes:
                # Search for Bible verses containing key words from the quote
                words = [w for w in quote.split() if len(w) > 3][:5]
                if not words:
                    continue

                # Use LIKE with multiple words to find candidates
                stop = {"the","and","that","they","them","this","with","have","from",
                        "were","was","shall","will","unto","upon","said","which","their",
                        "there","been","into","also","than","made","came","went","hath",
                        "every","your","thou","thee","whom"}
                search_words = [w.lower() for w in words if w.lower() not in stop][:3]
                if not search_words:
                    search_words = [words[0].lower()]

                conditions = " AND ".join([f"LOWER(text) LIKE ?" for _ in search_words])
                params = tuple(f"%{w}%" for w in search_words)
                candidates = await db.execute(
                    f"""SELECT book || ' ' || chapter || ':' || verse as ref, text
                       FROM bible_kjv WHERE {conditions} LIMIT 50""",
                    params
                )

                best_score = 0
                best_ref = ""
                for row in candidates:
                    score = SequenceMatcher(None, quote.lower(), row[1].lower()).ratio()
                    if score > best_score:
                        best_score = score
                        best_ref = row[0]

                # Only flag if it's a substantial quote with very low match
                if len(quote) > 60 and best_score < 0.4:
                    flags.append({
                        "type": "unverified_quote",
                        "reference": best_ref if best_score > 0.2 else "unknown",
                        "detail": f"A quoted passage could not be verified against the KJV Bible text (best match: {best_score:.0%}).",
                    })

        return {
            "verified": len(flags) == 0,
            "flags": flags,
        }


watchdog = Watchdog()
