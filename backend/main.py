"""Trials of Judah — Main API"""
import asyncio
import hashlib
import hmac
import re
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from starlette.middleware.base import BaseHTTPMiddleware

from backend.config import (
    SERVER_HOST, SERVER_PORT, FRONTEND_DIR, DATA_DIR,
    ACCESS_CODE, SESSION_SECRET, SESSION_MAX_AGE_DAYS,
)
from backend.models.database import db
from backend.services.llm_service import llm
from backend.services.verse_service import verse_service
from backend.services.watchdog import watchdog
from backend.services.lineage_service import lineage_service
from backend.services.prophecy_service import prophecy_service
from backend.services.search_service import search_service
from backend.services.map_service import map_service
from backend.services.evidence_service import evidence_service
from backend.services.martyrs_service import martyrs_service
from backend.services.enoch_service import enoch_service
from backend.services.events_service import events_service


@asynccontextmanager
async def lifespan(app):
    await db.init()
    await llm.is_available()

    from backend.data.seed import seed, seed_lineage, seed_bible_kjv, seed_prophecies
    seeded = await seed(db)
    if seeded:
        print("[Trials of Judah] Database seeded with verse data.")
    seeded_lineage = await seed_lineage(db)
    if seeded_lineage:
        print("[Trials of Judah] Lineage data seeded.")
    seeded_bible = await seed_bible_kjv(db)
    if seeded_bible:
        print("[Trials of Judah] Full KJV Bible seeded (31,100 verses).")
    seeded_prophecies = await seed_prophecies(db)
    if seeded_prophecies:
        print("[Trials of Judah] Prophecy data seeded.")

    yield
    await db.close()


app = FastAPI(title="Trials of Judah", version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


# ── Auth helpers ──────────────────────────────────
_COOKIE_NAME = "toj_session"
_MAX_AGE = SESSION_MAX_AGE_DAYS * 86400  # seconds

def _sign_token(timestamp: int) -> str:
    """Create an HMAC-signed session token."""
    msg = f"toj:{timestamp}".encode()
    sig = hmac.new(SESSION_SECRET.encode(), msg, hashlib.sha256).hexdigest()
    return f"{timestamp}:{sig}"

def _verify_token(token: str) -> bool:
    """Verify a session token is valid and not expired."""
    try:
        ts_str, sig = token.split(":", 1)
        ts = int(ts_str)
    except (ValueError, AttributeError):
        return False
    if time.time() - ts > _MAX_AGE:
        return False
    expected = hmac.new(
        SESSION_SECRET.encode(), f"toj:{ts}".encode(), hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(sig, expected)

# Routes that don't require auth
_PUBLIC_PATHS = {"/api/auth", "/api/health", "/api/auth/check"}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip auth if no access code is configured
        if not ACCESS_CODE:
            return await call_next(request)

        path = request.url.path

        # Allow public paths
        if path in _PUBLIC_PATHS:
            return await call_next(request)

        # Check session cookie
        token = request.cookies.get(_COOKIE_NAME)
        if token and _verify_token(token):
            return await call_next(request)

        # Not authenticated — serve login page for browser requests, 401 for API
        if path.startswith("/api/"):
            return JSONResponse({"error": "unauthorized"}, status_code=401)

        # Serve the login gate page
        login_html = FRONTEND_DIR / "login.html"
        if login_html.exists():
            return FileResponse(str(login_html))
        return JSONResponse({"error": "unauthorized"}, status_code=401)


app.add_middleware(AuthMiddleware)

_llm_semaphore = asyncio.Semaphore(1)


# ── Auth endpoints ─────────────────────────────────
class AuthRequest(BaseModel):
    code: str

@app.post("/api/auth")
async def auth(body: AuthRequest, response: Response):
    if not ACCESS_CODE:
        return {"status": "ok", "message": "No access code required"}
    if hmac.compare_digest(body.code.strip(), ACCESS_CODE):
        token = _sign_token(int(time.time()))
        response.set_cookie(
            key=_COOKIE_NAME,
            value=token,
            max_age=_MAX_AGE,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        return {"status": "ok"}
    return JSONResponse({"error": "Invalid access code"}, status_code=403)

@app.get("/api/auth/check")
async def auth_check(request: Request):
    if not ACCESS_CODE:
        return {"authenticated": True}
    token = request.cookies.get(_COOKIE_NAME)
    return {"authenticated": bool(token and _verify_token(token))}


# ── Health ──────────────────────────────────────────
@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "llm_available": llm.available,
        "llm_model": llm.model,
    }


# ── Categories ──────────────────────────────────────
@app.get("/api/categories")
async def get_categories(type: str = Query(None, alias="type")):
    cats = await verse_service.get_categories(db, type)
    return {"categories": cats}


# ── Verses ──────────────────────────────────────────
@app.get("/api/verses")
async def get_verses(category: str, translation: str = "kjv"):
    verses = await verse_service.get_verses(db, category, translation)
    return {"verses": verses, "translation": translation}


# ── Translations ────────────────────────────────────
@app.get("/api/translations")
async def get_translations():
    rows = await db.execute("SELECT code, name FROM translations ORDER BY id")
    return {"translations": [dict(r) for r in rows]}


# ── Ask ─────────────────────────────────────────────
class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)
    translation: str = Field(default="kjv", pattern="^(kjv|esv)$")


@app.post("/api/ask")
async def ask_guidance(req: AskRequest):
    if not await llm.is_available():
        return JSONResponse({"error": "Study commentary service unavailable"}, status_code=503)

    stop_words = {"i", "am", "a", "the", "is", "are", "was", "were", "be", "been",
                  "my", "me", "to", "of", "in", "for", "and", "or", "with", "how",
                  "what", "should", "about", "do", "can", "have", "has", "it", "that",
                  "this", "from", "on", "at", "an", "but", "not", "so", "if", "by",
                  "such", "like", "just", "really", "very", "much", "been", "being",
                  "would", "could", "will", "shall", "may", "might", "also", "than",
                  "them", "they", "their", "there", "then", "when", "which", "who",
                  "him", "his", "her", "she", "our", "your", "its", "all", "any",
                  "every", "each", "some", "many", "more", "most", "other", "into",
                  "upon", "unto", "thing", "things", "substance", "way", "man",
                  "men", "make", "made", "need", "want", "get", "got", "going",
                  "feel", "feeling", "help", "know", "life", "time", "day", "people"}
    words = re.findall(r'[a-zA-Z]+', req.question.lower())
    keywords = [w for w in words if w not in stop_words and len(w) > 2]

    # Expand keywords with related biblical/category terms
    keyword_expansions = {
        "drinking": ["drunkenness", "wine", "sober", "addiction"],
        "drugs": ["addiction", "bondage", "captive", "freedom"],
        "abuse": ["addiction", "bondage", "temptation"],
        "drunk": ["drunkenness", "wine", "sober"],
        "alcohol": ["drunkenness", "wine", "sober", "addiction"],
        "addicted": ["addiction", "bondage", "captive"],
        "angry": ["anger", "wrath"],
        "mad": ["anger", "wrath"],
        "temper": ["anger", "wrath"],
        "anxious": ["anxiety", "worry", "peace"],
        "worried": ["anxiety", "worry", "peace"],
        "stressed": ["anxiety", "peace", "trouble"],
        "scared": ["fear", "courage", "afraid"],
        "afraid": ["fear", "courage"],
        "depressed": ["grief", "sorrow", "comfort"],
        "sad": ["grief", "sorrow", "comfort"],
        "lonely": ["grief", "comfort"],
        "jealous": ["jealousy", "envy", "contentment"],
        "envious": ["jealousy", "envy"],
        "lying": ["lies", "deception", "truth"],
        "liar": ["lies", "deception", "truth"],
        "lazy": ["laziness", "diligent", "slothful"],
        "proud": ["pride", "humble", "humility"],
        "arrogant": ["pride", "humble"],
        "lustful": ["lust", "purity", "temptation"],
        "porn": ["lust", "purity", "adultery"],
        "forgive": ["forgiveness", "forgive", "bitterness"],
        "bitter": ["unforgiveness", "bitterness", "forgive"],
        "resentment": ["unforgiveness", "bitterness", "forgive"],
        "doubting": ["doubt", "faith", "trust"],
        "marriage": ["spouse", "wife", "husband"],
        "wife": ["spouse", "marriage"],
        "husband": ["spouse", "marriage"],
        "career": ["work", "calling", "diligent"],
        "job": ["work", "calling", "labor"],
        "money": ["financial", "wealth", "riches"],
        "debt": ["financial", "owe", "borrower"],
        "house": ["home", "dwelling", "build"],
        "moving": ["relocation", "journey", "direction"],
        "children": ["raising", "train", "child"],
        "parenting": ["raising", "children", "train"],
        "business": ["work", "labor", "diligent", "prosper"],
    }
    expanded = list(keywords)
    for kw in keywords:
        if kw in keyword_expansions:
            expanded.extend(keyword_expansions[kw])
    keywords = list(set(expanded))

    candidates = await verse_service.search_verses(db, keywords, req.translation, limit=30)

    if not candidates:
        return JSONResponse({"error": "No relevant verses found in the database."}, status_code=404)

    async with _llm_semaphore:
        llm_result = await llm.ask(req.question, candidates)

    if llm_result.get("error"):
        return JSONResponse({"error": f"Commentary generation failed: {llm_result['error']}"}, status_code=502)

    verification = await watchdog.verify(llm_result["commentary"], db, req.translation)

    # Resolve verses: first try VERSE: prefix format, then fallback to
    # extracting references from commentary text using watchdog regex
    resolved_verses = []
    seen_refs = set()

    for ref_str in llm_result["references"]:
        for c in candidates:
            if c["reference"] == ref_str and ref_str not in seen_refs:
                resolved_verses.append(c)
                seen_refs.add(ref_str)
                break

    # Fallback: extract references from commentary if VERSE: format wasn't used
    if not resolved_verses:
        extracted = watchdog.extract_references(llm_result["commentary"])
        for ext in extracted:
            for c in candidates:
                if c["reference"] not in seen_refs:
                    # Match by book + chapter + verse_start
                    if (c["book"].lower() == ext["book"].lower()
                            and c["chapter"] == ext["chapter"]
                            and c["verse_start"] == ext["verse_start"]):
                        resolved_verses.append(c)
                        seen_refs.add(c["reference"])
                        break
                    # Also match if referenced verse falls within a stored range
                    if (c["book"].lower() == ext["book"].lower()
                            and c["chapter"] == ext["chapter"]
                            and c.get("verse_end") is not None
                            and c["verse_start"] <= ext["verse_start"] <= c["verse_end"]):
                        resolved_verses.append(c)
                        seen_refs.add(c["reference"])
                        break

    return {
        "verses": resolved_verses,
        "commentary": llm_result["commentary"],
        "verified": verification["verified"],
        "flags": verification["flags"],
    }


# ── Unified Search (replaces /api/lookup) ──────────
class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=200)


@app.post("/api/search")
async def unified_search(req: SearchRequest):
    # Search across all data types
    results = await search_service.search(db, req.query)

    # Build Bible verse context for LLM
    bible_context = "\n".join(
        f"- {r['book']} {r['chapter']}:{r['verse']}: {r['text']}"
        for r in results["bible_verses"][:10]
    )

    # LLM commentary (if available)
    commentary = {"scripture": "", "scholarly": ""}
    verified = True
    flags = []

    if await llm.is_available() and bible_context:
        async with _llm_semaphore:
            llm_result = await llm.lookup(req.query, bible_context)
        if not llm_result.get("error"):
            raw = llm_result["commentary"]
            if "SCHOLARLY CONTEXT:" in raw:
                parts = raw.split("SCHOLARLY CONTEXT:", 1)
                commentary["scripture"] = parts[0].replace("SCRIPTURE SAYS:", "").strip()
                commentary["scholarly"] = parts[1].strip()
            elif "SCRIPTURE SAYS:" in raw:
                commentary["scripture"] = raw.replace("SCRIPTURE SAYS:", "").strip()
            else:
                commentary["scripture"] = raw
            verification = await watchdog.verify_quotes_only(raw, db)
            verified = verification["verified"]
            flags = verification["flags"]

    return {
        "query": req.query,
        "bible_verses": results["bible_verses"],
        "persons": results["persons"],
        "prophecies": results["prophecies"],
        "map_kingdoms": results.get("map_kingdoms", []),
        "map_cities": results.get("map_cities", []),
        "map_peoples": results.get("map_peoples", []),
        "map_evidence": results.get("map_evidence", []),
        "map_martyrs": results.get("map_martyrs", []),
        "commentary": commentary,
        "verified": verified,
        "flags": flags,
    }


# ── Prophecy ────────────────────────────────────────
@app.get("/api/prophecy/timeline")
async def prophecy_timeline():
    return await prophecy_service.get_timeline(db)

@app.get("/api/prophecy/categories")
async def prophecy_categories():
    return await prophecy_service.get_categories(db)

@app.get("/api/prophecy/filter")
async def prophecy_filter(category: str = None, status: str = None, tag: str = None):
    return {"prophecies": await prophecy_service.filter_prophecies(db, category, status, tag)}

@app.get("/api/prophecy/{prophecy_id}")
async def prophecy_detail(prophecy_id: int):
    result = await prophecy_service.get_prophecy(db, prophecy_id)
    if not result:
        return JSONResponse({"error": "Prophecy not found"}, status_code=404)
    return result


# ── Lineage ─────────────────────────────────────────
@app.get("/api/lineage/tree")
async def lineage_tree():
    return await lineage_service.get_tree(db)

@app.get("/api/lineage/timeline")
async def lineage_timeline():
    return await lineage_service.get_timeline(db)

@app.get("/api/lineage/person/{person_id}")
async def lineage_person(person_id: int):
    result = await lineage_service.get_person(db, person_id)
    if not result:
        return JSONResponse({"error": "Person not found"}, status_code=404)
    return result

@app.get("/api/lineage/persons")
async def lineage_persons(search: str = None, branch: str = None, generation: int = None):
    persons = await lineage_service.search_persons(db, search, branch, generation)
    return {"persons": persons}


# ── Map ────────────────────────────────────────────
@app.get("/api/map/eras")
async def map_eras():
    return {"eras": map_service.get_eras()}

@app.get("/api/map/kingdoms")
async def map_kingdoms():
    return {"kingdoms": map_service.get_kingdoms()}

@app.get("/api/map/era/{era_id}")
async def map_era(era_id: str):
    return map_service.get_era(era_id)

@app.get("/api/map/kingdom/{kingdom_id}")
async def map_kingdom(kingdom_id: str, era: str = None):
    result = map_service.get_kingdom(kingdom_id, era)
    if not result:
        return JSONResponse({"error": "Kingdom not found"}, status_code=404)
    kingdom = result["kingdom"]
    refs = await map_service.get_cross_references(
        db, kingdom["name"], kingdom.get("aliases", [])
    )
    result["related_prophecies"] = refs["prophecies"]
    result["related_persons"] = refs["persons"]
    return result

@app.get("/api/map/kingdom/{kingdom_id}/geojson")
async def map_kingdom_geojson(kingdom_id: str, era: str = Query(...)):
    geojson = map_service.get_kingdom_geojson(kingdom_id, era)
    if not geojson:
        return JSONResponse({"error": "GeoJSON not found"}, status_code=404)
    return geojson

@app.get("/api/map/peoples")
async def map_peoples():
    return {"peoples": map_service.get_peoples()}

@app.get("/api/map/people/{people_id}")
async def map_people(people_id: int):
    result = map_service.get_people(people_id)
    if not result:
        return JSONResponse({"error": "People not found"}, status_code=404)
    return result

@app.get("/api/map/search")
async def map_search(q: str = Query(..., min_length=2)):
    return map_service.search(q)


# ── Evidence ───────────────────────────────────────
@app.get("/api/map/evidence")
async def map_evidence(era: str = None, type: str = None):
    return {"evidence": evidence_service.get_evidence_summary(era, type)}

@app.get("/api/map/evidence/connections")
async def map_evidence_connections(event: str = Query(...)):
    return evidence_service.get_connections(event)

@app.get("/api/map/evidence/{evidence_id}")
async def map_evidence_detail(evidence_id: str):
    result = evidence_service.get_evidence(evidence_id)
    if not result:
        return JSONResponse({"error": "Evidence not found"}, status_code=404)
    return result


# ── Martyrs ────────────────────────────────────────
@app.get("/api/map/martyrs")
async def map_martyrs(era: str = None):
    return {"martyrs": martyrs_service.get_martyrs_summary(era)}

@app.get("/api/map/martyrs/{martyr_id}")
async def map_martyr_detail(martyr_id: str):
    result = martyrs_service.get_martyr(martyr_id)
    if not result:
        return JSONResponse({"error": "Martyr not found"}, status_code=404)
    return result


# ── Historical Events ─────────────────────────────
@app.get("/api/events")
async def get_events():
    return {"events": events_service.get_all_events()}

@app.get("/api/events/{event_id}")
async def get_event(event_id: str):
    result = events_service.get_event(event_id)
    if not result:
        return JSONResponse({"error": "Event not found"}, status_code=404)
    return result


# ── Enoch Study ────────────────────────────────────
@app.get("/api/enoch/canon")
async def enoch_canon():
    return {"canon": enoch_service.get_canon()}

@app.get("/api/enoch/categories")
async def enoch_categories():
    return {"categories": enoch_service.get_categories()}

@app.get("/api/enoch/parallels")
async def enoch_parallels(category: str = None):
    return {"parallels": enoch_service.get_parallels(category)}

@app.get("/api/enoch/images/{filename:path}")
async def enoch_image(filename: str):
    image_dir = DATA_DIR / "images" / "enoch"
    image_path = image_dir / filename
    if not image_path.exists() or not image_path.is_file():
        return JSONResponse({"error": "Image not found"}, status_code=404)
    return FileResponse(str(image_path))


# ── Frontend ────────────────────────────────────────
@app.get("/enoch")
async def enoch_page():
    enoch_html = FRONTEND_DIR / "enoch.html"
    if enoch_html.exists():
        return FileResponse(str(enoch_html))
    return {"message": "Enoch study page not yet built."}

@app.get("/{rest_of_path:path}")
async def frontend(rest_of_path: str = ""):
    index = FRONTEND_DIR / "index.html"
    if index.exists():
        return FileResponse(str(index))
    return {"message": "Trials of Judah is running. Frontend not yet built."}


if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port)
