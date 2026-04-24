"""Ollama LLM service for Trials of Judah study commentary."""
import httpx
from backend.config import OLLAMA_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT

STUDY_BIBLE_SYSTEM_PROMPT = """You are a study Bible commentator. Your role is to help believers find and understand scripture relevant to their situation.

Rules:
- Only reference verses from the provided verse list. Never fabricate scripture.
- Always cite the full reference (Book Chapter:Verse) for every verse you mention.
- Provide historical context: who wrote it, when, to whom, and why.
- Include original Hebrew/Greek word insights when relevant.
- Provide cross-references to related passages from the provided list.
- Write in the style of a study Bible commentary — scholarly but accessible.
- Never add to, subtract from, or paraphrase the word of God.
- Clearly distinguish your commentary from scripture.
- Select the 3-5 most relevant verses from the provided list for the person's situation.
- Format your response as commentary only. Do NOT repeat the verse text — it will be displayed separately.
- IMPORTANT: Do not modernize biblical references. Use the terms as they appear in scripture:
  * Refer to "the twelve tribes," "Israel," "Judah," "Israelites," or "Hebrews" — not "Jews." The biblical twelve tribes of Israel are distinct from modern Judaism.
  * Never use the term "Jewish Christian" — it is a contradiction. Judaism denies the divinity of Christ. One is either a follower of Christ or not.
  * You may use "the church," "believers," "the assembly," or "the congregation" as appropriate.
  * When describing Paul, say "Paul, a Hebrew of the tribe of Benjamin" or "Paul, formerly a Pharisee" — not "a Jewish Christian."
  * Let the scripture speak for itself. Do not impose modern religious categories onto biblical figures or audiences."""


class LLMService:
    def __init__(self):
        self.url = OLLAMA_URL
        self.model = OLLAMA_MODEL
        self.timeout = OLLAMA_TIMEOUT
        self._available = None

    async def is_available(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(f"{self.url}/api/tags")
                if resp.status_code == 200:
                    models = resp.json().get("models", [])
                    model_names = [m["name"] for m in models]
                    self._available = any(self.model in n for n in model_names)
                else:
                    self._available = False
        except (httpx.ConnectError, httpx.TimeoutException):
            self._available = False
        return self._available

    @property
    def available(self) -> bool:
        return self._available if self._available is not None else False

    async def ask(self, question: str, candidate_verses: list) -> dict:
        """Generate study commentary for a question given candidate verses.

        Returns: {references: [str], commentary: str, error: str|None}
        """
        verse_context = "\n".join(
            f"- {v['reference']}: {v['text']}"
            for v in candidate_verses
        )

        prompt = f"""A believer asks: "{question}"

Here are the available verses from the database:
{verse_context}

Select the 3-5 most relevant verses for this person's situation. For each verse you select, cite the reference (e.g., "Proverbs 15:1") and explain:
1. The historical context of the passage
2. How it applies to the person's situation
3. Any relevant Hebrew/Greek word meanings

List the references you selected at the very beginning, one per line, prefixed with "VERSE: "
Then provide your commentary."""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": STUDY_BIBLE_SYSTEM_PROMPT,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 1000,
            },
        }
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(self.timeout, connect=5.0)) as client:
                resp = await client.post(f"{self.url}/api/generate", json=payload)
                resp.raise_for_status()
                raw = resp.json().get("response", "")
        except (httpx.TimeoutException, httpx.HTTPStatusError, httpx.ConnectError) as e:
            return {"references": [], "commentary": "", "error": str(e)}

        # Extract referenced verses from response
        import re
        references = []
        lines = raw.split("\n")
        verse_line_indices = set()
        for i, line in enumerate(lines):
            stripped = line.strip()
            # Match "VERSE: ...", "1. VERSE: ...", "- VERSE: ...", etc.
            m = re.match(r'^[\d.\-\*\s]*VERSE:\s*(.+)', stripped)
            if m:
                ref = m.group(1).split(" - ")[0].strip()
                references.append(ref)
                verse_line_indices.add(i)

        # Remove VERSE: lines from commentary
        commentary_lines = [l for i, l in enumerate(lines) if i not in verse_line_indices]
        commentary = "\n".join(commentary_lines).strip()

        return {
            "references": references,
            "commentary": commentary,
        }


    async def lookup(self, query: str, verse_context: str = "") -> dict:
        """Look up a biblical term, place, person, or concept.

        Returns: {commentary: str, error: str|None}
        """
        system = """You are a biblical scholar and study Bible commentator. A reader is studying the biblical genealogy and wants to learn more about a term, place, person, or concept they encountered.

Rules:
- EVERY factual claim MUST be backed by a specific scripture reference (Book Chapter:Verse).
- If you do not know something from scripture, say "Scripture does not provide further detail on this."
- Clearly separate what scripture says from what scholars suggest.
- For scholarly interpretations, prefix with "Scholars suggest:" or "Historical research indicates:" — never present speculation as fact.
- Always cite the full reference (Book Chapter:Verse) for every verse you mention.
- Include original Hebrew/Greek word insights when relevant.
- Never fabricate scripture or historical claims.
- Do not modernize biblical references. Use "the twelve tribes," "Israel," "Judah," "Israelites," "Hebrews" — not "Jews." Never use "Jewish Christian."
- You may use "the church," "believers," "the assembly" as appropriate.
- When describing Paul, say "Paul, a Hebrew of the tribe of Benjamin" or "Paul, formerly a Pharisee."
- If you are uncertain about something, say so honestly.

Format your response as:

SCRIPTURE SAYS:
[What the Bible directly states, with verse references for every claim]

SCHOLARLY CONTEXT:
[What historians and scholars suggest, clearly labeled as interpretation, with sources where possible]

If there is no scholarly context to add, omit that section entirely."""

        bible_section = ""
        if verse_context:
            bible_section = f"""

Here are the actual Bible verses (KJV) that mention "{query}":
{verse_context}

Use ONLY these verses as your source material. Do NOT cite any verse that is not listed above."""

        prompt = f"""The reader wants to know more about: "{query}"
{bible_section}

STRICT RULES FOR THIS RESPONSE:
1. Only reference verses from the list provided above. Do NOT cite verses not in the list.
2. Quote the verse text exactly as provided — do not paraphrase or alter it.
3. Do NOT fabricate Hebrew/Greek etymologies unless you are absolutely certain.
4. Do NOT conflate different people, places, or concepts. Stay focused on exactly what was asked.
5. Keep it concise — discuss only the verses provided.
6. If no verses were provided, say "This term does not appear directly in scripture" and provide only scholarly context if available."""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 800,
            },
        }
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(self.timeout, connect=5.0)) as client:
                resp = await client.post(f"{self.url}/api/generate", json=payload)
                resp.raise_for_status()
                raw = resp.json().get("response", "")
        except (httpx.TimeoutException, httpx.HTTPStatusError, httpx.ConnectError) as e:
            return {"commentary": "", "error": str(e)}

        return {"commentary": raw}


llm = LLMService()
