# Book of Enoch Study Section — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a standalone `/enoch` page within the Trials of Judah app presenting the case for the Book of Enoch's canonicity and its parallels to world mythology.

**Architecture:** JSON-driven data layer (matching existing patterns like `evidence.json`), a service class for data access, API endpoints under `/api/enoch/`, a static image directory with a JSON manifest, and a separate `enoch.html` frontend page served at `/enoch`.

**Tech Stack:** FastAPI (backend), vanilla HTML/CSS/JS (frontend), JSON data files, public domain images.

**Spec:** `docs/superpowers/specs/2026-03-30-enoch-study-design.md`

---

## File Structure

```
backend/
  services/
    enoch_service.py          — Service class: loads and queries enoch data files
  data/
    enoch_canon.json          — Part 1 canonicity evidence cards
    enoch_parallels.json      — Part 2 deep study entries (all 8 cultures)
    enoch_images.json         — Image manifest (id, filename, source, attribution, caption)
    images/
      enoch/                  — Public domain images directory
frontend/
  enoch.html                  — Standalone Enoch study page
backend/
  main.py                     — Modified: add /api/enoch/* endpoints and /enoch route
```

---

### Task 1: Create Data Files — Canon Evidence

**Files:**
- Create: `backend/data/enoch_canon.json`

- [ ] **Step 1: Create the canonicity evidence JSON**

Create `backend/data/enoch_canon.json` with the 7 evidence cards. Each card has: `id`, `title`, `summary`, `primary_source_quote`, `source_citation`, `canonical_refs` (array of `{verse, text, relevance}`), `historical_context`, `images` (array of image IDs, empty for now), `order`.

```json
[
  {
    "id": "dead-sea-scrolls",
    "title": "The Dead Sea Scrolls",
    "summary": "Eleven copies of the Book of Enoch were found among the Dead Sea Scrolls at Qumran — more copies than most canonical Old Testament books.",
    "primary_source_quote": "The Qumran library contained eleven manuscripts of 1 Enoch in Aramaic (4Q201–202, 4Q204–212), dating from the third to first century BC, making it one of the most frequently copied texts at Qumran.",
    "source_citation": "Milik, J.T., The Books of Enoch: Aramaic Fragments of Qumran Cave 4, Oxford, 1976",
    "canonical_refs": [
      {
        "verse": "Jude 1:14",
        "text": "And Enoch also, the seventh from Adam, prophesied of these, saying, Behold, the Lord cometh with ten thousands of his saints",
        "relevance": "Jude treats the Book of Enoch as genuine prophecy, quoting it directly."
      }
    ],
    "historical_context": "The Dead Sea Scrolls were discovered between 1947 and 1956 in caves near Qumran on the northwest shore of the Dead Sea. Among the roughly 900 manuscripts recovered, eleven contained portions of 1 Enoch written in Aramaic. For context, the book of Isaiah — universally accepted as canonical — was found in only 21 copies. The sheer number of Enoch manuscripts indicates the Qumran community regarded it as authoritative scripture, not peripheral literature.",
    "images": [],
    "order": 1
  },
  {
    "id": "jude-quotes-enoch",
    "title": "Jude 1:14-15 Directly Quotes 1 Enoch",
    "summary": "The canonical epistle of Jude directly quotes 1 Enoch 1:9, treating it as genuine prophecy from the patriarch Enoch.",
    "primary_source_quote": "And Enoch also, the seventh from Adam, prophesied of these, saying, Behold, the Lord cometh with ten thousands of his saints, To execute judgment upon all, and to convince all that are ungodly among them of all their ungodly deeds which they have ungodly committed, and of all their hard speeches which ungodly sinners have spoken against him.",
    "source_citation": "Jude 1:14-15, King James Version",
    "canonical_refs": [
      {
        "verse": "1 Enoch 1:9",
        "text": "And behold! He cometh with ten thousands of His holy ones to execute judgment upon all, and to destroy all the ungodly.",
        "relevance": "This is the source text Jude quotes. The wording is nearly identical, confirming Jude drew directly from the Book of Enoch."
      },
      {
        "verse": "2 Timothy 3:16",
        "text": "All scripture is given by inspiration of God, and is profitable for doctrine, for reproof, for correction, for instruction in righteousness.",
        "relevance": "If Jude was inspired by the Holy Spirit to write his epistle, and he quoted Enoch as prophecy, the source he quoted was also treated as inspired."
      }
    ],
    "historical_context": "The Epistle of Jude is one of the shortest books in the New Testament, yet it makes one of the most significant textual connections in the Bible. Jude does not merely allude to Enoch — he explicitly names the patriarch and introduces his words with 'prophesied,' the same language used for Isaiah, Jeremiah, and other canonical prophets. No other non-canonical text receives this treatment anywhere in the New Testament.",
    "images": [],
    "order": 2
  },
  {
    "id": "second-peter-parallels",
    "title": "2 Peter 2:4 Parallels the Watchers' Imprisonment",
    "summary": "Peter describes angels who sinned being cast into chains of darkness — a scene found in detail only in 1 Enoch, not in the Old Testament.",
    "primary_source_quote": "For if God spared not the angels that sinned, but cast them down to hell, and delivered them into chains of darkness, to be reserved unto judgment...",
    "source_citation": "2 Peter 2:4, King James Version",
    "canonical_refs": [
      {
        "verse": "1 Enoch 10:4-6",
        "text": "And again the Lord said to Raphael: Bind Azazel hand and foot, and cast him into the darkness: and make an opening in the desert, which is in Dudael, and cast him therein.",
        "relevance": "Peter's description of angels bound in chains of darkness directly parallels Enoch's account of the Watchers being bound and cast into darkness."
      },
      {
        "verse": "Genesis 6:1-2",
        "text": "And it came to pass, when men began to multiply on the face of the earth, and daughters were born unto them, That the sons of God saw the daughters of men that they were fair; and they took them wives of all which they chose.",
        "relevance": "Genesis mentions the 'sons of God' but gives no detail about their punishment. Enoch provides the full account that Peter references."
      },
      {
        "verse": "Jude 1:6",
        "text": "And the angels which kept not their first estate, but left their own habitation, he hath reserved in everlasting chains under darkness unto the judgment of the great day.",
        "relevance": "Jude's parallel account confirms Peter and Jude both drew from the same Enochic tradition."
      }
    ],
    "historical_context": "The Greek word Peter uses for 'cast down to hell' is tartaroo — the only occurrence of this word in the entire Bible. Tartarus was the deepest abyss in Greek mythology where the Titans were imprisoned after their war against the Olympians. Peter's use of this specific term suggests he expected his audience to understand the parallel between the imprisoned Watchers of Enoch and the imprisoned Titans of Greek tradition — a connection this study explores in depth.",
    "images": [],
    "order": 3
  },
  {
    "id": "genesis-six",
    "title": "Genesis 6:1-4 — The Passage Enoch Expands",
    "summary": "The canonical account of the 'sons of God' and the Nephilim in Genesis 6 is a compressed summary. The Book of Enoch provides the full narrative.",
    "primary_source_quote": "There were giants in the earth in those days; and also after that, when the sons of God came in unto the daughters of men, and they bare children to them, the same became mighty men which were of old, men of renown.",
    "source_citation": "Genesis 6:4, King James Version",
    "canonical_refs": [
      {
        "verse": "1 Enoch 6:1-2",
        "text": "And it came to pass when the children of men had multiplied that in those days were born unto them beautiful and comely daughters. And the angels, the children of the heaven, saw and lusted after them.",
        "relevance": "Enoch identifies the 'sons of God' as angels (Watchers) and provides their names, their leader Semjaza, and the full account of their descent."
      },
      {
        "verse": "1 Enoch 7:1-2",
        "text": "And all the others together with them took unto themselves wives, and each chose for himself one, and they began to go in unto them and to defile themselves with them... And they became pregnant, and they bare great giants.",
        "relevance": "Enoch expands on 'the same became mighty men' — explaining the Nephilim were the hybrid offspring of the Watchers and human women."
      },
      {
        "verse": "Numbers 13:33",
        "text": "And there we saw the giants, the sons of Anak, which come of the giants: and we were in our own sight as grasshoppers.",
        "relevance": "The Israelite spies encountered giant descendants in Canaan, confirming Genesis 6:4's statement that the Nephilim existed 'also after that.'"
      }
    ],
    "historical_context": "Genesis 6:1-4 is one of the most debated passages in the Bible. In just four verses, it introduces the 'sons of God,' their union with human women, and the resulting Nephilim — then immediately moves to the flood narrative. The brevity is striking. The Book of Enoch reads as the full account behind this compressed passage: it names 200 Watchers, describes their oath on Mount Hermon, details the forbidden knowledge they taught humanity, and explains why their actions provoked the judgment of the flood.",
    "images": [],
    "order": 4
  },
  {
    "id": "ethiopian-canon",
    "title": "The Ethiopian Orthodox Canon",
    "summary": "The Ethiopian Orthodox Tewahedo Church — one of the oldest Christian churches in the world — has never removed the Book of Enoch from its canon.",
    "primary_source_quote": "The Ethiopian biblical canon includes 81 books. Among these is 1 Enoch (known as Henok in Ge'ez), which has been continuously regarded as holy scripture since the church's founding in the 4th century AD.",
    "source_citation": "Cowley, R.W., 'The Biblical Canon of the Ethiopian Orthodox Church Today,' Ostkirchliche Studien, 1974",
    "canonical_refs": [
      {
        "verse": "Acts 8:27-39",
        "text": "And, behold, a man of Ethiopia, an eunuch of great authority under Candace queen of the Ethiopians... was reading Esaias the prophet.",
        "relevance": "The Ethiopian church traces its roots to this encounter. The Ethiopian eunuch was already studying scripture before Philip explained the gospel — suggesting an existing scriptural tradition that included Enoch."
      },
      {
        "verse": "Zephaniah 3:10",
        "text": "From beyond the rivers of Ethiopia my suppliants, even the daughter of my dispersed, shall bring mine offering.",
        "relevance": "The prophetic connection between Ethiopia and the preservation of scriptural truth."
      }
    ],
    "historical_context": "The Ethiopian Orthodox Tewahedo Church is one of the oldest organized Christian churches in the world, predating the Roman Catholic Church's formal establishment. Their canon of scripture was never subject to the same councils that excluded Enoch from Western canons. The Ge'ez manuscripts of 1 Enoch are the only complete surviving copies of the book — the Aramaic fragments from Qumran are partial. Without Ethiopia's faithful preservation, the full text of 1 Enoch would have been lost entirely.",
    "images": [],
    "order": 5
  },
  {
    "id": "early-church-fathers",
    "title": "Early Church Fathers Cited Enoch",
    "summary": "Multiple early church fathers — including Tertullian, Irenaeus, Clement of Alexandria, and Justin Martyr — referenced or quoted the Book of Enoch as authoritative.",
    "primary_source_quote": "I am aware that the Scripture of Enoch, which has assigned this order of action to angels, is not received by some, because it is not admitted into the Jewish canon either... But since Enoch in the same scripture has preached likewise concerning the Lord, nothing at all must be rejected by us which pertains to us.",
    "source_citation": "Tertullian, On the Apparel of Women, Book I, Chapter 3 (circa 200 AD)",
    "canonical_refs": [
      {
        "verse": "Jude 1:14-15",
        "text": "And Enoch also, the seventh from Adam, prophesied of these...",
        "relevance": "Tertullian argued that since canonical scripture (Jude) quotes Enoch, the book should not be dismissed."
      }
    ],
    "historical_context": "Tertullian (c. 155-220 AD) explicitly defended the Book of Enoch's authority. Irenaeus (c. 130-202 AD) referenced the Watchers narrative in Against Heresies. Clement of Alexandria (c. 150-215 AD) cited Enoch in his Eclogae Propheticae. Justin Martyr (c. 100-165 AD) referenced the angels who fell and produced offspring with women. These were not fringe figures — they were the foundational theologians of early Christianity. The fact that they treated Enoch as scripture for the first two centuries of the church undermines the claim that it was always considered apocryphal.",
    "images": [],
    "order": 6
  },
  {
    "id": "why-removed",
    "title": "Why It Was Removed",
    "summary": "The Book of Enoch was gradually excluded from Western canons not because of textual evidence, but because its content became theologically inconvenient.",
    "primary_source_quote": "The book of Enoch was rejected by the Rabbis partly because of its messianic claims which could be applied to Jesus, and partly because of its detailed angelology which conflicted with developing rabbinic theology that sought to minimize intermediary beings between God and man.",
    "source_citation": "VanderKam, James C., Enoch and the Growth of an Apocalyptic Tradition, Catholic Biblical Quarterly Monograph Series, 1984",
    "canonical_refs": [
      {
        "verse": "Matthew 22:30",
        "text": "For in the resurrection they neither marry, nor are given in marriage, but are as the angels of God in heaven.",
        "relevance": "This verse was used to argue angels cannot procreate — but it speaks of resurrected believers and faithful angels, not fallen ones who abandoned their proper domain."
      },
      {
        "verse": "1 Enoch 15:3-7",
        "text": "Wherefore have ye left the high, holy, and eternal heaven, and lain with women, and defiled yourselves with the daughters of men and taken to yourselves wives... And now, the giants, who are produced from the spirits and flesh, shall be called evil spirits upon the earth.",
        "relevance": "Enoch's explicit account of angelic-human hybridization was the primary theological stumbling block for later councils."
      }
    ],
    "historical_context": "The exclusion of Enoch from Western canons was a gradual process driven by multiple factors. Jewish rabbinical authorities rejected it partly because its 'Son of Man' passages (1 Enoch 46-48) could be read as messianic prophecy pointing to Jesus. Early church councils, influenced by Augustine's 'sons of Seth' reinterpretation of Genesis 6 (which replaced the angelic interpretation with a human one), found the Watchers narrative increasingly difficult to reconcile with their evolving theology. By the 4th century, the book was marginalized in the West — though it continued to be read in Ethiopia, where the original interpretation was preserved. The politics of canon formation, not the textual evidence, drove its removal.",
    "images": [],
    "order": 7
  }
]
```

- [ ] **Step 2: Verify the JSON is valid**

Run:
```bash
cd /c/AI/MGC_Workbench/apps/trialsofjudah && python3 -c "import json; data=json.load(open('backend/data/enoch_canon.json','r',encoding='utf-8')); print(f'{len(data)} canon cards loaded')"
```
Expected: `7 canon cards loaded`

- [ ] **Step 3: Commit**

```bash
git add backend/data/enoch_canon.json
git commit -m "feat(enoch): add canonicity evidence data (7 cards)"
```

---

### Task 2: Create Data Files — Mesopotamian Parallels

**Files:**
- Create: `backend/data/enoch_parallels.json`

- [ ] **Step 1: Create the parallels JSON with Mesopotamian entries**

Create `backend/data/enoch_parallels.json` starting with the Mesopotamian category (4 entries). The file is an array. Each entry has: `id`, `category`, `title`, `claim`, `enoch_quotes` (array of `{text, reference}`), `mythology_quotes` (array of `{text, source, citation}`), `side_by_side` (array of `{enoch_point, mythology_point}`), `canonical_refs` (array of `{verse, text, relevance_note}`), `canonical_gaps` (string or null), `distortion_analysis`, `key_takeaway`, `images` (array of image IDs), `tags`.

```json
[
  {
    "id": "watchers-anunnaki",
    "category": "mesopotamian",
    "title": "The Watchers and the Anunnaki",
    "claim": "The Sumerian Anunnaki — 'those who from heaven to earth came' — are the same beings the Book of Enoch identifies as the Watchers: divine beings who descended to earth and altered the course of human history.",
    "enoch_quotes": [
      {
        "text": "And it came to pass when the children of men had multiplied that in those days were born unto them beautiful and comely daughters. And the angels, the children of the heaven, saw and lusted after them, and said to one another: Come, let us choose us wives from among the children of men and beget us children.",
        "reference": "1 Enoch 6:1-2"
      },
      {
        "text": "And they were in all two hundred; who descended in the days of Jared on the summit of Mount Hermon, and they called it Mount Hermon, because they had sworn and bound themselves by mutual imprecations upon it.",
        "reference": "1 Enoch 6:6"
      }
    ],
    "mythology_quotes": [
      {
        "text": "When the gods like men bore the work and suffered the toil — the toil of the gods was great, the work was heavy, the distress was much... the Anunnaki made the Igigi bear the workload.",
        "source": "Atrahasis Epic",
        "citation": "Tablet I, lines 1-5 (Old Babylonian, c. 1700 BC)"
      },
      {
        "text": "The Anunnaki, the great gods, had caused the Igigi to bear the workload. The gods had to dig out the canals, had to clear channels, the lifelines of the land.",
        "source": "Atrahasis Epic",
        "citation": "Tablet I, lines 1-20"
      }
    ],
    "side_by_side": [
      {
        "enoch_point": "200 Watchers descend from heaven to Mount Hermon",
        "mythology_point": "The Anunnaki descend from heaven to earth; their name literally means 'those who from heaven to earth came'"
      },
      {
        "enoch_point": "The Watchers are a specific class of angels with a defined number and named leaders (Semjaza, Azazel)",
        "mythology_point": "The Anunnaki are a specific class of gods with a defined council and named leaders (Anu, Enlil, Enki)"
      },
      {
        "enoch_point": "The Watchers take an oath together before descending",
        "mythology_point": "The Anunnaki hold divine councils and make collective decrees"
      },
      {
        "enoch_point": "Their descent is unauthorized — a rebellion against the Most High's order",
        "mythology_point": "In Sumerian texts, the Anunnaki's activities on earth are presented as authorized divine governance — the rebellion is reframed as legitimate rule"
      }
    ],
    "canonical_refs": [
      {
        "verse": "Genesis 6:1-2",
        "text": "The sons of God saw the daughters of men that they were fair; and they took them wives of all which they chose.",
        "relevance_note": "Genesis confirms divine beings ('sons of God') descended and took human wives — the same event Enoch details and the Sumerians mythologized."
      },
      {
        "verse": "Psalm 82:1,6-7",
        "text": "God standeth in the congregation of the mighty; he judgeth among the gods... I have said, Ye are gods; and all of you are children of the most High. But ye shall die like men, and fall like one of the princes.",
        "relevance_note": "God addresses divine beings ('gods') who will be judged and die — consistent with Enoch's account of the Watchers' judgment."
      }
    ],
    "canonical_gaps": null,
    "distortion_analysis": "The Sumerian scribes transformed the Watchers' unauthorized rebellion into authorized divine governance. In Enoch, the descent is a crime against the Most High's created order. In Sumerian myth, the Anunnaki are the rightful rulers of heaven and earth — their descent is presented as cosmic administration, not cosmic crime. The oath on Mount Hermon becomes a divine council decree. The named Watchers become named gods with temples and cults. The forbidden knowledge they taught becomes gifts of civilization. This is the core pattern of distortion that repeats across every mythology: rebellion is reframed as benevolence, judgment is reframed as cosmic injustice, and the fallen become the worshipped.",
    "key_takeaway": "The Anunnaki are not aliens, ancient astronauts, or mythological inventions. They are the Watchers of 1 Enoch — divine beings who abandoned heaven, descended to earth, and were subsequently deified by the civilizations they corrupted. The Sumerian account preserves the structure of the event while inverting its moral meaning.",
    "images": [],
    "tags": ["watchers", "descent", "divine-beings", "anunnaki", "sumerian"]
  },
  {
    "id": "azazel-enki",
    "category": "mesopotamian",
    "title": "Azazel and Enki — The Forbidden Knowledge",
    "claim": "The Sumerian god Enki, who gave humanity the 'me' (divine arts of civilization), is the mythologized version of the Watcher Azazel, who taught mankind forbidden knowledge including metalwork, weaponry, and cosmetics.",
    "enoch_quotes": [
      {
        "text": "And Azazel taught men to make swords, and knives, and shields, and breastplates, and made known to them the metals of the earth and the art of working them, and bracelets, and ornaments, and the use of antimony, and the beautifying of the eyelids, and all kinds of costly stones, and all colouring tinctures.",
        "reference": "1 Enoch 8:1"
      },
      {
        "text": "And there arose much godlessness, and they committed fornication, and they were led astray, and became corrupt in all their ways.",
        "reference": "1 Enoch 8:2"
      },
      {
        "text": "Thou seest what Azazel hath done, who hath taught all unrighteousness on earth and revealed the eternal secrets which were preserved in heaven.",
        "reference": "1 Enoch 9:6"
      }
    ],
    "mythology_quotes": [
      {
        "text": "Enki, the lord of wisdom, who understands the innermost secrets... who gave the arts of civilization to mankind, who bestowed the me upon the cities.",
        "source": "Enki and the World Order",
        "citation": "Sumerian composition, c. 1900 BC"
      },
      {
        "text": "After the kingship had descended from heaven, the kingship was in Eridu. In Eridu, Alulim became king... The divine arts were brought down from heaven.",
        "source": "Sumerian King List",
        "citation": "Weld-Blundell Prism, c. 2000 BC"
      }
    ],
    "side_by_side": [
      {
        "enoch_point": "Azazel teaches metalwork — swords, knives, shields, breastplates",
        "mythology_point": "Enki gives humanity the 'me' — divine arts including metalworking and craftsmanship"
      },
      {
        "enoch_point": "Azazel reveals cosmetics — antimony, beautifying of eyelids, colouring tinctures",
        "mythology_point": "Enki bestows arts of adornment and beauty upon humanity"
      },
      {
        "enoch_point": "Azazel reveals 'eternal secrets which were preserved in heaven'",
        "mythology_point": "Enki steals the 'me' (divine decrees/knowledge) from other gods and gives them to mankind"
      },
      {
        "enoch_point": "Azazel's teachings lead humanity into corruption and godlessness",
        "mythology_point": "Enki is celebrated as humanity's benefactor and champion — the corruption is inverted into progress"
      },
      {
        "enoch_point": "Azazel is bound and cast into darkness as punishment",
        "mythology_point": "Enki faces no lasting punishment — he outwits the other gods and remains honored"
      }
    ],
    "canonical_refs": [
      {
        "verse": "Genesis 4:22",
        "text": "And Zillah, she also bare Tubalcain, an instructer of every artificer in brass and iron.",
        "relevance_note": "Tubal-Cain's metalworking mastery in the line of Cain may reflect the forbidden knowledge Azazel taught. Enoch provides the source of this sudden technological leap."
      },
      {
        "verse": "Leviticus 16:8-10",
        "text": "And Aaron shall cast lots upon the two goats; one lot for the LORD, and the other lot for the scapegoat [Azazel].",
        "relevance_note": "Azazel appears by name in the Day of Atonement ritual. The scapegoat bearing sins into the wilderness parallels Azazel being cast into the wilderness in 1 Enoch 10:4-5."
      }
    ],
    "canonical_gaps": null,
    "distortion_analysis": "The transformation from Azazel to Enki follows the same inversion pattern: the crime becomes a gift, the punishment becomes a triumph, the rebel becomes the hero. In Enoch, Azazel reveals secrets that were 'preserved in heaven' — knowledge humans were never meant to have, which led directly to corruption and violence. In Sumerian myth, Enki steals the 'me' from other gods and delivers them to humanity as civilization's foundation. The act of forbidden revelation is identical; only the moral framing is reversed. Notably, Enki is associated with water and the abyss (the Abzu) — and Azazel is cast into a pit in the wilderness. The prison becomes a palace.",
    "key_takeaway": "Azazel did not merely 'influence' Sumerian mythology — his actions are the historical event that Sumerian scribes repackaged as the myth of Enki. The forbidden arts he taught became the 'me' of civilization. His punishment was erased and replaced with divine triumph. This is not coincidence; it is the same event told by the corrupted and the faithful.",
    "images": [],
    "tags": ["azazel", "enki", "forbidden-knowledge", "metalwork", "cosmetics", "me"]
  },
  {
    "id": "nephilim-apkallu",
    "category": "mesopotamian",
    "title": "The Nephilim and the Apkallu",
    "claim": "The Sumerian Apkallu — seven pre-flood sages of superhuman wisdom sent from heaven — are a mythologized memory of the Nephilim and the antediluvian world shaped by the Watchers' forbidden knowledge.",
    "enoch_quotes": [
      {
        "text": "And they became pregnant, and they bare great giants, whose height was three thousand ells: Who consumed all the acquisitions of men. And when men could no longer sustain them, the giants turned against them and devoured mankind.",
        "reference": "1 Enoch 7:2-4"
      },
      {
        "text": "And the women also of the angels who went astray shall become sirens.",
        "reference": "1 Enoch 19:2"
      }
    ],
    "mythology_quotes": [
      {
        "text": "In the time before the flood, seven sages came forth from the river, sent by Ea [Enki], to teach mankind the arts of civilization: writing, craftsmanship, building, and divination.",
        "source": "Babylonian tradition (Berossus)",
        "citation": "Berossus, Babyloniaca, Fragment 1 (c. 280 BC)"
      },
      {
        "text": "The Apkallu were of mixed nature — part divine, part human. After the flood, no more pure Apkallu appeared; only their descendants, the Ummanu, who were fully human.",
        "source": "Bit Meseri incantation texts",
        "citation": "Neo-Assyrian period, c. 900-600 BC"
      }
    ],
    "side_by_side": [
      {
        "enoch_point": "The Nephilim are hybrid offspring of angels and humans — giants of immense stature",
        "mythology_point": "The Apkallu are beings of 'mixed nature — part divine, part human' with superhuman abilities"
      },
      {
        "enoch_point": "The Nephilim exist in the pre-flood world and are destroyed by the flood",
        "mythology_point": "The Apkallu are specifically pre-flood figures; after the flood only fully human sages appear"
      },
      {
        "enoch_point": "The Watchers teach forbidden arts (metalwork, sorcery, astrology)",
        "mythology_point": "The Apkallu teach the 'arts of civilization' (writing, craftsmanship, building, divination)"
      },
      {
        "enoch_point": "The Nephilim consume mankind's resources and turn violent",
        "mythology_point": "This aspect is erased — the Apkallu are remembered only as benevolent teachers"
      }
    ],
    "canonical_refs": [
      {
        "verse": "Genesis 6:4",
        "text": "There were giants in the earth in those days; and also after that, when the sons of God came in unto the daughters of men, and they bare children to them, the same became mighty men which were of old, men of renown.",
        "relevance_note": "'Mighty men of old, men of renown' — the Hebrew 'gibborim' and 'anshei hashem' suggest the Nephilim were famous. Every culture remembered them, but reframed them as heroes and sages."
      },
      {
        "verse": "Wisdom of Solomon 14:6",
        "text": "For in the old time also, when the proud giants perished, the hope of the world governed by thy hand escaped in a weak vessel.",
        "relevance_note": "The 'proud giants' who perished before the flood, preserved in Second Temple literature."
      }
    ],
    "canonical_gaps": "The canonical Bible does not describe the Nephilim in detail beyond Genesis 6:4 and Numbers 13:33. Enoch provides the extensive account of their nature, behavior, and destruction.",
    "distortion_analysis": "The Sumerian tradition performs a selective memory: it preserves the Nephilim's superhuman nature and pre-flood existence but strips away their violence, consumption of mankind, and the judgment they provoked. The Apkallu are sanitized Nephilim — their divine-human hybrid nature is retained, their role as civilization-bringers is retained, but their destruction and the reason for the flood are suppressed. The seven named Apkallu likely correspond to specific prominent Nephilim or Watchers whose teachings left the deepest mark on antediluvian society.",
    "key_takeaway": "The Apkallu tradition is Mesopotamia's collective memory of the Nephilim — preserved in form but inverted in character. The giants who consumed mankind became the sages who civilized them. The hybrids who provoked God's judgment became the heroes who built the world.",
    "images": [],
    "tags": ["nephilim", "apkallu", "giants", "pre-flood", "hybrid-beings"]
  },
  {
    "id": "enoch-flood-gilgamesh",
    "category": "mesopotamian",
    "title": "The Flood of Enoch and the Epic of Gilgamesh",
    "claim": "The Babylonian flood narrative in the Epic of Gilgamesh is a distorted retelling of the same event described in Genesis and detailed in 1 Enoch — with the critical difference that Enoch explains WHY the flood was sent.",
    "enoch_quotes": [
      {
        "text": "And destroy all the spirits of the reprobate and the children of the Watchers, because they have wronged mankind. Destroy all wrong from the face of the earth and let every evil work come to an end.",
        "reference": "1 Enoch 10:15-16"
      },
      {
        "text": "And to Noah the Lord said: Go and tell Noah in my name, 'Hide thyself!' and reveal to him the end that is approaching: that the whole earth will be destroyed, and a deluge is about to come upon the whole earth.",
        "reference": "1 Enoch 10:1-2"
      }
    ],
    "mythology_quotes": [
      {
        "text": "The hearts of the great gods moved them to inflict the flood... Enlil said, 'I will bring about a deluge, to destroy mankind.'",
        "source": "Epic of Gilgamesh",
        "citation": "Tablet XI, lines 14-20 (Standard Babylonian version)"
      },
      {
        "text": "Utnapishtim said to Gilgamesh: 'I will reveal to thee, Gilgamesh, a hidden matter and a secret of the gods will I tell thee: The gods agreed to send a flood.'",
        "source": "Epic of Gilgamesh",
        "citation": "Tablet XI, lines 9-12"
      }
    ],
    "side_by_side": [
      {
        "enoch_point": "The flood is sent because of the Watchers' corruption of humanity — a specific, moral cause",
        "mythology_point": "The flood is sent because the gods are annoyed by human noise — a petty, arbitrary cause"
      },
      {
        "enoch_point": "Noah is warned by God to build an ark and preserve life",
        "mythology_point": "Utnapishtim is warned by Ea (Enki) to build a boat and preserve life"
      },
      {
        "enoch_point": "The flood destroys the Nephilim and their corruption",
        "mythology_point": "The flood destroys humanity; no mention of giants or hybrid beings"
      },
      {
        "enoch_point": "After the flood, the spirits of the dead Nephilim become evil spirits on earth",
        "mythology_point": "No parallel — this consequence is entirely suppressed in Mesopotamian tradition"
      },
      {
        "enoch_point": "God's judgment is righteous — the corruption warranted destruction",
        "mythology_point": "The gods regret the flood and weep — the destruction is portrayed as excessive"
      }
    ],
    "canonical_refs": [
      {
        "verse": "Genesis 6:5-7",
        "text": "And God saw that the wickedness of man was great in the earth, and that every imagination of the thoughts of his heart was only evil continually. And it repented the LORD that he had made man on the earth... And the LORD said, I will destroy man whom I have created from the face of the earth.",
        "relevance_note": "Genesis confirms the flood was judgment on wickedness. Enoch explains the source of that wickedness: the Watchers' corruption."
      },
      {
        "verse": "2 Peter 2:5",
        "text": "And spared not the old world, but saved Noah the eighth person, a preacher of righteousness, bringing in the flood upon the world of the ungodly.",
        "relevance_note": "Peter connects the flood directly to the angels who sinned (2 Peter 2:4), confirming the Enochic sequence: angelic sin → corruption → flood judgment."
      }
    ],
    "canonical_gaps": null,
    "distortion_analysis": "The Gilgamesh flood narrative preserves the historical structure of the event — divine warning, one righteous man, a boat, animals saved, universal destruction, a post-flood offering — while completely erasing the cause. In Enoch and Genesis, the flood is the righteous judgment of the one true God against a specific corruption: the Watchers' hybridization of divine and human bloodlines and their introduction of forbidden knowledge. In Gilgamesh, this moral clarity is replaced with divine caprice — the gods flood the earth because humans are too noisy, then regret it and weep. The Nephilim are erased. The Watchers are erased. The moral framework is destroyed. What remains is the skeleton of the event without its meaning.",
    "key_takeaway": "Gilgamesh does not predate or disprove Genesis and Enoch — it is the corrupted memory of the same event. The flood happened. Enoch tells us why. Gilgamesh remembers that it happened but has lost the reason, replacing divine justice with divine caprice.",
    "images": [],
    "tags": ["flood", "gilgamesh", "utnapishtim", "noah", "judgment"]
  }
]
```

- [ ] **Step 2: Verify the JSON is valid**

Run:
```bash
cd /c/AI/MGC_Workbench/apps/trialsofjudah && python3 -c "import json; data=json.load(open('backend/data/enoch_parallels.json','r',encoding='utf-8')); cats=set(e['category'] for e in data); print(f'{len(data)} entries across {len(cats)} categories: {cats}')"
```
Expected: `4 entries across 1 categories: {'mesopotamian'}`

- [ ] **Step 3: Commit**

```bash
git add backend/data/enoch_parallels.json
git commit -m "feat(enoch): add Mesopotamian parallel entries (4 deep studies)"
```

---

### Task 3: Add Greek Parallel Entries

**Files:**
- Modify: `backend/data/enoch_parallels.json`

- [ ] **Step 1: Append Greek entries to the parallels JSON**

Add 4 entries to the `enoch_parallels.json` array with `"category": "greek"`:

**Entry 1: "watchers-titans"**
- **Title:** "The Watchers and the Titans"
- **Claim:** The Greek Titans — divine beings who ruled before the Olympians and were overthrown and imprisoned in Tartarus — are the mythologized Watchers of 1 Enoch, and their imprisonment parallels the Watchers' binding in chains of darkness.
- **Enoch quotes:** 1 Enoch 10:4-6 (Azazel bound and cast into darkness), 1 Enoch 10:11-12 (Semjaza and associates bound for 70 generations)
- **Mythology quotes:** Hesiod's Theogony (Titans cast into Tartarus by Zeus), Homer's Iliad (Tartarus described as far below Hades as heaven is above earth)
- **Side by side:** Watchers rebel against God / Titans rebel against Zeus; Watchers bound in darkness / Titans imprisoned in Tartarus; 200 named Watchers / 12 named Titans; Watchers await final judgment / Titans await release that never comes; Peter uses the Greek word "tartaroo" — directly connecting the two traditions
- **Canonical refs:** 2 Peter 2:4 (tartaroo — the ONLY use of this word in the Bible), Jude 1:6 (everlasting chains under darkness)
- **Distortion:** The one true God becomes a pantheon. The Most High's righteous judgment becomes Zeus's political victory. The Watchers' sin (abandoning heaven, corrupting humanity) becomes the Titans' crime (opposing Zeus's kingship). Moral rebellion is reframed as political conflict.
- **Tags:** watchers, titans, tartarus, imprisonment, greek

**Entry 2: "nephilim-demigods"**
- **Title:** "The Nephilim and the Demigods"
- **Claim:** Greek demigods — Hercules, Achilles, Perseus, and others born of a god and a mortal woman — are cultural memories of the Nephilim: hybrid offspring of the Watchers and human women.
- **Enoch quotes:** 1 Enoch 7:1-2 (Watchers take wives, produce giants), 1 Enoch 7:3-4 (giants consume all resources and turn on mankind)
- **Mythology quotes:** Homer's Iliad (heroes of superhuman strength, born of gods and mortals), Hesiod's Works and Days (the "race of heroes" who lived before the current age)
- **Side by side:** Nephilim are angel-human hybrids / Demigods are god-human hybrids; Nephilim are giants of great stature / Demigods possess superhuman size and strength; Nephilim are violent and consume mankind / Demigods are warriors and slayers; Nephilim are destroyed in the flood / The heroic age ends in catastrophic wars (Trojan War, Theban cycle); Nephilim are "mighty men of old, men of renown" (Genesis 6:4) / Demigods are the famous heroes of old
- **Canonical refs:** Genesis 6:4 ("mighty men of old, men of renown"), Numbers 13:33 (Nephilim survivors in Canaan)
- **Tags:** nephilim, demigods, hercules, giants, hybrid-beings

**Entry 3: "azazel-prometheus"**
- **Title:** "Azazel and Prometheus — The Theft of Divine Knowledge"
- **Claim:** Prometheus, the Titan who stole fire from the gods and gave it to humanity, is the Greek retelling of Azazel's revelation of forbidden heavenly knowledge to mankind.
- **Enoch quotes:** 1 Enoch 8:1 (Azazel teaches metalwork, weapons, cosmetics), 1 Enoch 9:6 (Azazel revealed eternal secrets preserved in heaven)
- **Mythology quotes:** Hesiod's Theogony (Prometheus steals fire and gives it to mortals), Aeschylus's Prometheus Bound (Prometheus teaches mankind all arts — metalwork, writing, medicine, astronomy)
- **Side by side:** Azazel reveals secrets "preserved in heaven" / Prometheus steals fire "from the gods"; Azazel teaches metalwork, weaponry, cosmetics / Prometheus teaches metalwork, writing, medicine, astronomy; Azazel is bound and cast into darkness in the wilderness / Prometheus is chained to a mountain and tortured; Azazel's punishment is decreed by God / Prometheus's punishment is decreed by Zeus; Both acts lead to human suffering despite appearing as gifts
- **Canonical refs:** Leviticus 16:8-10 (Azazel and the scapegoat), Genesis 4:22 (Tubal-Cain's metalwork)
- **Tags:** azazel, prometheus, fire, forbidden-knowledge, punishment

**Entry 4: "watchers-imprisonment-tartarus"**
- **Title:** "The Chains of Darkness and the Pit of Tartarus"
- **Claim:** Tartarus in Greek mythology — the deepest abyss where the Titans are imprisoned in unbreakable chains — is a direct cultural memory of the imprisonment of the Watchers described in 1 Enoch and referenced in 2 Peter 2:4.
- **Enoch quotes:** 1 Enoch 10:4-5 (bind Azazel, cast him into darkness, place sharp rocks upon him), 1 Enoch 10:11-12 (bind Watchers for 70 generations in valleys of the earth until judgment)
- **Mythology quotes:** Hesiod's Theogony (Tartarus surrounded by bronze fence, night poured around its throat, Titans imprisoned within), Homer's Iliad (Tartarus as far below Hades as earth is below heaven)
- **Side by side:** Watchers bound in "valleys of the earth" / Titans imprisoned in the deepest abyss beneath the earth; "Chains of darkness" / Bronze chains in eternal darkness; Reserved "until the great day of judgment" / Imprisoned eternally with no release; God decrees the punishment through archangels / Zeus decrees the punishment through the Hundred-Handed Ones; The prison is beneath the earth in darkness / Tartarus is beneath the earth in darkness
- **Canonical refs:** 2 Peter 2:4 (tartaroo — Peter chose THIS word specifically), Jude 1:6 (everlasting chains under darkness), Revelation 20:1-3 (the angel binds Satan in the abyss)
- **Distortion:** The Greeks preserved the structure of the imprisonment almost intact — chains, darkness, underground, eternal — because the horror of the event was too vivid to distort. What they changed was the identity of the jailer (Zeus instead of God) and the nature of the crime (political rebellion instead of moral corruption).
- **Tags:** tartarus, chains, imprisonment, darkness, abyss

Provide the full JSON for all 4 entries with complete quotes, side-by-side arrays, and analysis paragraphs following the exact schema established in Task 2.

- [ ] **Step 2: Verify**

Run:
```bash
cd /c/AI/MGC_Workbench/apps/trialsofjudah && python3 -c "import json; data=json.load(open('backend/data/enoch_parallels.json','r',encoding='utf-8')); cats={e['category']:0 for e in data}; [cats.__setitem__(e['category'], cats[e['category']]+1) for e in data]; print(f'{len(data)} entries: {dict(cats)}')"
```
Expected: `8 entries: {'mesopotamian': 4, 'greek': 4}`

- [ ] **Step 3: Commit**

```bash
git add backend/data/enoch_parallels.json
git commit -m "feat(enoch): add Greek parallel entries (4 deep studies)"
```

---

### Task 4: Add Egyptian Parallel Entries

**Files:**
- Modify: `backend/data/enoch_parallels.json`

- [ ] **Step 1: Append Egyptian entries**

Add 3 entries with `"category": "egyptian"`:

**Entry 1: "watchers-thoth"**
- **Title:** "Thoth and the Forbidden Arts of the Watchers"
- **Claim:** The Egyptian god Thoth — lord of wisdom, writing, magic, and all hidden knowledge — is the mythologized composite of the Watchers who taught humanity forbidden arts, particularly Azazel (who taught metalwork and cosmetics) and Penemue (who taught writing).
- **Enoch quotes:** 1 Enoch 8:1 (Azazel teaches arts), 1 Enoch 69:8-9 (Penemue teaches writing — "the bitter and the sweet and the secrets of wisdom"), 1 Enoch 8:3 (Armaros teaches enchantments, Baraqijal teaches astrology)
- **Mythology quotes:** Book of the Dead (Thoth as scribe of the gods and inventor of writing), Corpus Hermeticum (Thoth/Hermes as bearer of all divine knowledge to mankind)
- **Side by side:** Multiple Watchers teach distinct forbidden arts / Thoth is credited with ALL knowledge — writing, magic, medicine, astronomy; Watchers reveal "secrets preserved in heaven" / Thoth possesses "the words of power" hidden in divine books; The revelation leads to corruption / Thoth's gifts are celebrated as civilization's foundation; Watchers are punished for teaching / Thoth is honored eternally as a god
- **Canonical refs:** 1 Enoch 69:8-9 (Penemue teaches writing), Genesis 4:22 (metalwork in Cain's line)
- **Tags:** thoth, writing, magic, forbidden-knowledge, egyptian

**Entry 2: "ogdoad-preflood"**
- **Title:** "The Ogdoad and the Pre-Flood World"
- **Claim:** The Egyptian Ogdoad — eight primordial deities who existed before creation in a dark watery chaos — preserves a distorted memory of the pre-flood world described in Enoch, where the Watchers' corruption plunged earth into chaos before God's judgment through water.
- **Enoch quotes:** 1 Enoch 10:15-16 (destroy all wrong, let every evil work come to an end), 1 Enoch 10:1-2 (the deluge is about to come upon the whole earth)
- **Mythology quotes:** Hermopolis creation texts (eight primordial gods in dark waters before creation), Coffin Texts (the Ogdoad as beings of the first time)
- **Side by side:** Pre-flood world ruled by Watchers and Nephilim / "First time" (Zep Tepi) ruled by the Ogdoad; World destroyed by water (the flood) / Primordial watery chaos from which the new world emerges; 8 people saved on the ark (Noah + family) / 8 primordial deities form the Ogdoad; The pre-flood world is judged and destroyed / The "first time" is remembered as a golden age
- **Canonical refs:** Genesis 7:13 (eight people saved — Noah, his wife, three sons, three wives), 1 Peter 3:20 (eight souls saved by water), 2 Peter 3:5-6 (the world that then was, being overflowed with water, perished)
- **Tags:** ogdoad, pre-flood, chaos, eight, creation-myth

**Entry 3: "osiris-fallen-divine"**
- **Title:** "Osiris and the Fallen Divine Ruler"
- **Claim:** The myth of Osiris — a divine king who ruled earth, was betrayed and killed, and became lord of the underworld — echoes the Enochic pattern of divine beings who descended to rule earth and were judged, their spirits consigned to the realm beneath.
- **Enoch quotes:** 1 Enoch 15:8-10 (the spirits of the giants shall be called evil spirits upon earth; their dwelling shall be upon the earth), 1 Enoch 10:11-12 (Watchers bound in valleys of the earth)
- **Mythology quotes:** Pyramid Texts (Osiris as first king of the earth, now ruler of the Duat/underworld), Book of the Dead (Osiris judges the dead in the halls beneath the earth)
- **Side by side:** Watchers descend from heaven to rule earth / Osiris descends from divine realm to rule Egypt; Watchers are judged and imprisoned beneath the earth / Osiris is killed and becomes ruler of the underworld; Spirits of dead Nephilim become evil spirits on earth / Osiris exists between death and life, ruling the dead; The Watchers' rule leads to corruption and judgment / Osiris's rule is remembered as a golden age
- **Canonical refs:** Genesis 6:1-4 (sons of God on earth), Isaiah 14:9-15 (the dead/Rephaim stir to greet the fallen king), Ezekiel 32:27 (mighty men of old who descended to the pit with their weapons)
- **Tags:** osiris, underworld, divine-kingship, judgment, fallen-rulers

Full JSON for all 3 entries with complete content.

- [ ] **Step 2: Verify**

Expected: `11 entries: {'mesopotamian': 4, 'greek': 4, 'egyptian': 3}`

- [ ] **Step 3: Commit**

```bash
git add backend/data/enoch_parallels.json
git commit -m "feat(enoch): add Egyptian parallel entries (3 deep studies)"
```

---

### Task 5: Add Norse Parallel Entries

**Files:**
- Modify: `backend/data/enoch_parallels.json`

- [ ] **Step 1: Append Norse entries**

Add 3 entries with `"category": "norse"`:

**Entry 1: "nephilim-jotnar"**
- **Title:** "The Jotnar and the Nephilim"
- **Claim:** The Norse Jotnar (giants) — primordial beings of immense size and power who existed before and alongside the gods — are Scandinavia's memory of the Nephilim.
- **Enoch quotes:** 1 Enoch 7:2-4 (giants of great height who consumed all), 1 Enoch 15:8-10 (spirits of giants as evil spirits)
- **Mythology quotes:** Prose Edda (Ymir the first giant from whose body the world was made), Voluspa (the Jotnar as ancient beings predating the gods)
- **Side by side:** Nephilim are hybrid offspring of divine and human / Jotnar are primordial beings distinct from gods and men; Nephilim are giants of immense stature / Jotnar are giants of immense stature; Nephilim devour mankind's resources / Jotnar are enemies of mankind and the gods; Nephilim are destroyed in the flood / The frost giants are destroyed by the flood of Ymir's blood; Nephilim existed before the flood in a corrupted world / Jotnar existed before the current world order
- **Canonical refs:** Genesis 6:4 (giants in the earth), Numbers 13:33 (sons of Anak), Deuteronomy 3:11 (Og's iron bedstead — 13.5 feet)
- **Tags:** jotnar, giants, nephilim, norse, ymir

**Entry 2: "odin-forbidden-knowledge"**
- **Title:** "Odin's Pursuit of Forbidden Knowledge"
- **Claim:** Odin's relentless pursuit of hidden knowledge — sacrificing his eye at Mimir's well, hanging on Yggdrasil for nine nights to learn the runes — mirrors the Watchers' revelation of forbidden heavenly secrets, reframed as a heroic quest rather than a transgression.
- **Enoch quotes:** 1 Enoch 8:1-3 (Watchers teach metalwork, enchantments, astrology, signs), 1 Enoch 9:6 (revealed eternal secrets preserved in heaven), 1 Enoch 69:8-12 (specific forbidden knowledge — writing, oaths, the secrets of the angels)
- **Mythology quotes:** Havamal stanzas 138-141 (Odin hangs on the world tree and gains the runes), Prose Edda (Odin sacrifices his eye for a drink from the well of wisdom)
- **Side by side:** Watchers reveal secrets "preserved in heaven" / Odin gains runes (divine knowledge) through extreme sacrifice; Azazel teaches enchantments and sorcery / Odin masters seidr (sorcery) and galdr (incantation); The revelation is a transgression punished by God / The quest is celebrated as Odin's greatest achievement; Multiple Watchers each teach a specific art / Odin alone accumulates all forbidden knowledge into one figure
- **Canonical refs:** 1 Enoch 9:6 (Azazel revealed the eternal secrets), Deuteronomy 18:10-12 (sorcery and enchantment are abominations)
- **Tags:** odin, runes, forbidden-knowledge, sorcery, wisdom

**Entry 3: "ragnarok-flood-judgment"**
- **Title:** "Ragnarok and the Flood Judgment"
- **Claim:** Ragnarok — the Norse apocalypse in which the world is destroyed and reborn — contains clear structural parallels to both the flood judgment described in Genesis and Enoch, and the final judgment described in Revelation.
- **Enoch quotes:** 1 Enoch 10:15-16 (destroy all wrong, let every evil work come to an end), 1 Enoch 1:3-7 (the Holy Great One will come forth, mountains will melt, earth will be destroyed)
- **Mythology quotes:** Voluspa stanzas 52-66 (the world is destroyed by fire and flood, then rises again renewed from the sea), Prose Edda (Surtr burns the world, the sea swallows the land, Lif and Lifthrasir survive to repopulate)
- **Side by side:** The flood destroys the corrupted pre-flood world / Ragnarok destroys the corrupted current world; God judges the Watchers and Nephilim / The gods and giants destroy each other; Noah and family survive to repopulate / Lif and Lifthrasir survive to repopulate; A new, purified earth after the flood / A new, green earth rises from the sea after Ragnarok; Final judgment reserved for the end of all things (1 Enoch 16:1) / Ragnarok is the final reckoning
- **Canonical refs:** Genesis 6:13 (the end of all flesh), 2 Peter 3:10 (the heavens shall pass away with a great noise, the earth also shall be burned up), Revelation 21:1 (a new heaven and a new earth)
- **Tags:** ragnarok, flood, judgment, apocalypse, renewal

Full JSON for all 3 entries.

- [ ] **Step 2: Verify**

Expected: `14 entries: {'mesopotamian': 4, 'greek': 4, 'egyptian': 3, 'norse': 3}`

- [ ] **Step 3: Commit**

```bash
git add backend/data/enoch_parallels.json
git commit -m "feat(enoch): add Norse parallel entries (3 deep studies)"
```

---

### Task 6: Add Hindu Parallel Entries

**Files:**
- Modify: `backend/data/enoch_parallels.json`

- [ ] **Step 1: Append Hindu entries**

Add 3 entries with `"category": "hindu"`:

**Entry 1: "watchers-devas-asuras"**
- **Title:** "The Devas, Asuras, and the Watchers"
- **Claim:** The Vedic cosmic struggle between Devas (celestial beings) and Asuras (powerful rivals who were once divine but fell from grace) preserves the Enochic pattern of faithful angels versus the Watchers who rebelled.
- **Enoch quotes:** 1 Enoch 6:1-6 (Watchers conspire and descend), 1 Enoch 10:11-12 (Watchers bound as punishment for rebellion), 1 Enoch 15:3 ("Wherefore have ye left the high, holy, and eternal heaven?")
- **Mythology quotes:** Rig Veda (Devas and Asuras as rival divine groups), Bhagavata Purana (Asuras as fallen divine beings who oppose the celestial order)
- **Side by side:** Watchers are angels who abandon heaven / Asuras are divine beings who fall from celestial status; Watchers are led by named leaders (Semjaza, Azazel) / Asuras are led by named kings (Hiranyakashipu, Bali); Watchers rebel against the Most High's order / Asuras rebel against the Devas' authority; Watchers are bound and judged / Asuras are defeated and cast down; Faithful angels (Michael, Raphael) carry out judgment / Devas (Indra, Vishnu) carry out the defeat of Asuras
- **Canonical refs:** Revelation 12:7-9 (war in heaven — Michael and his angels against the dragon), Isaiah 14:12-15 (the fall from heaven), Jude 1:6 (angels who kept not their first estate)
- **Tags:** devas, asuras, divine-war, rebellion, hindu

**Entry 2: "vedic-giants-nephilim"**
- **Title:** "The Daityas, Rakshasas, and the Nephilim"
- **Claim:** The Daityas (giant sons of Diti) and Rakshasas (powerful demonic beings) of Hindu tradition are India's memory of the Nephilim — giant hybrid beings born from the union of the divine and the earthly.
- **Enoch quotes:** 1 Enoch 7:2-4 (giants of immense height who devoured mankind), 1 Enoch 15:8-10 (spirits of giants become evil spirits on earth)
- **Mythology quotes:** Mahabharata (Daityas as giant sons of divine parents who war against the gods), Ramayana (Rakshasas as powerful shapeshifting beings of enormous size)
- **Side by side:** Nephilim are offspring of angels and humans / Daityas are offspring of the divine progenitor Kashyapa and Diti; Nephilim are giants who consume all / Daityas and Rakshasas are giants who threaten creation; Nephilim are destroyed in the flood / Daityas are defeated in cosmic wars by the avatars of Vishnu; Dead Nephilim become evil spirits on earth / Rakshasas are demonic beings that haunt the earth
- **Canonical refs:** Genesis 6:4 (giants / mighty men of old), 1 Samuel 17:4 (Goliath's stature), Baruch 3:26-28 (the giants of old who perished)
- **Tags:** daityas, rakshasas, nephilim, giants, hybrid-beings

**Entry 3: "rishis-watchers-teachers"**
- **Title:** "The Rishis and the Watchers' Forbidden Instruction"
- **Claim:** The Vedic Rishis — divine sages who descended to earth and taught humanity the sacred arts, sciences, and rituals — preserve the memory of the Watchers' role as teachers of forbidden knowledge, stripped of its transgressive nature.
- **Enoch quotes:** 1 Enoch 8:1-3 (Watchers teach metalwork, enchantments, astrology, root-cutting, signs), 1 Enoch 69:8-12 (Penemue teaches writing, Kasdeja teaches abortion and the striking of the spirit)
- **Mythology quotes:** Rig Veda (the seven Rishis who brought knowledge from heaven), Vishnu Purana (Rishis as divine seers who taught mankind the Vedas and all arts)
- **Side by side:** Watchers descend from heaven to teach mankind / Rishis descend from celestial realms to teach mankind; Watchers teach specific arts: metalwork, astrology, sorcery, writing / Rishis teach specific arts: Vedas, medicine (Ayurveda), astronomy (Jyotish), rituals; Seven archangels stand before God / Seven Rishis (Saptarishi) are the primal sages; The teaching is forbidden — "eternal secrets preserved in heaven" / The teaching is celebrated as divine grace; There are exactly 200 Watchers organized under leaders / There are various groups of Rishis organized by lineage (gotra)
- **Canonical refs:** 1 Enoch 9:6 (Azazel revealed eternal secrets), Deuteronomy 29:29 (the secret things belong unto the LORD)
- **Tags:** rishis, sages, forbidden-knowledge, teaching, vedic

Full JSON for all 3 entries.

- [ ] **Step 2: Verify**

Expected: `17 entries: {'mesopotamian': 4, 'greek': 4, 'egyptian': 3, 'norse': 3, 'hindu': 3}`

- [ ] **Step 3: Commit**

```bash
git add backend/data/enoch_parallels.json
git commit -m "feat(enoch): add Hindu parallel entries (3 deep studies)"
```

---

### Task 7: Add Native American, African, and East Asian Parallel Entries

**Files:**
- Modify: `backend/data/enoch_parallels.json`

- [ ] **Step 1: Append remaining culture entries**

Add 8 entries total:

**Native American / Mesoamerican (3 entries, `"category": "native_american"`):**

**Entry 1: "sky-beings-descent"**
- **Title:** "The Sky Beings Who Descended"
- **Claim:** Across dozens of Native American traditions — from the Hopi to the Maya to the Lakota — powerful beings descended from the sky, taught humanity, and shaped the world. These are memories of the Watchers' descent.
- Cover: Hopi kachinas (spirit beings from the sky), Mayan Kukulkan/Quetzalcoatl (feathered serpent who descended and taught civilization), Lakota star people traditions
- **Side by side:** Watchers descend from heaven / Sky beings descend to earth; Watchers teach forbidden arts / Sky beings teach agriculture, astronomy, building; Watchers are eventually removed/punished / Sky beings depart with a promise to return
- **Canonical refs:** Genesis 6:1-2, 1 Enoch 6:6 (descent on Mount Hermon)
- **Tags:** sky-beings, descent, kachina, quetzalcoatl, teaching

**Entry 2: "giant-traditions"**
- **Title:** "Giant Traditions Across the Americas"
- **Claim:** Virtually every Native American tribal tradition includes accounts of giants who once roamed the land — beings of immense stature who were eventually destroyed. These are the Nephilim.
- Cover: Paiute Si-Te-Cah (red-haired giants), Choctaw Nahullo (giant race), Aztec Quinametzin (giants of the previous age), Inca tradition of giants at Tiahuanaco
- **Side by side:** Nephilim are giants / Native traditions describe giants; Nephilim destroyed in flood / Giants destroyed by flood, fire, or divine intervention; Nephilim were violent and cannibalistic / Many traditions describe man-eating giants
- **Canonical refs:** Genesis 6:4, Numbers 13:33, Deuteronomy 3:11
- **Tags:** giants, nephilim, si-te-cah, quinametzin, oral-tradition

**Entry 3: "flood-narratives-americas"**
- **Title:** "Flood Narratives of the Americas"
- **Claim:** Over 200 Native American flood narratives share core elements with the Genesis/Enoch account — a global deluge sent as divine judgment, a small group of survivors, and a renewed world.
- Cover: Hopi emergence through worlds of destruction, Aztec fourth sun destruction by water, Cree/Ojibwe flood narratives, Mapuche flood tradition
- **Side by side:** God sends flood as judgment on corruption / Great Spirit sends flood to cleanse the world; Noah warned and saved / A righteous person/family warned and saved; Animals preserved / Animals preserved; New covenant after flood / New age begins after waters recede
- **Canonical refs:** Genesis 6-8, 1 Enoch 10:1-2, 2 Peter 3:5-6
- **Tags:** flood, americas, deluge, survival, judgment

**African (2 entries, `"category": "african"`):**

**Entry 1: "fallen-sky-spirits"**
- **Title:** "Fallen Sky Spirits in African Oral Tradition"
- **Claim:** Multiple African traditions describe powerful spirit beings who descended from the sky, interacted with humans, and were punished — mirroring the Watchers' descent and judgment.
- Cover: Zulu tradition (Unkulunkulu sent beings from the sky), Dogon (Nommo — amphibious beings from the sky who taught humanity), Yoruba Orisha (divine beings who descended from heaven to earth)
- **Side by side:** Watchers descend from heaven / Sky spirits descend to earth; Watchers interact with humans and teach them / Nommo/Orisha interact with and teach humanity; Watchers are punished for transgression / Some sky spirits face consequences for mixing with the earthly realm
- **Canonical refs:** Genesis 6:1-2, 1 Enoch 6:1-6, Jude 1:6
- **Tags:** sky-spirits, descent, nommo, orisha, african

**Entry 2: "african-giant-traditions"**
- **Title:** "Giant Beings in African Ancestral Memory"
- **Claim:** African traditions across the continent preserve accounts of giant beings who lived in ancient times — from the Anansi stories referencing ancient giants to the Tutsi and Zulu oral histories of enormous ancestral beings.
- **Side by side:** Nephilim as giants of old / Giant beings in ancestral oral traditions; Nephilim as "mighty men of renown" / Ancient giants revered or feared in oral histories; Nephilim destroyed in judgment / Giants disappeared in ancient cataclysms
- **Canonical refs:** Genesis 6:4, 1 Enoch 7:2-4
- **Tags:** giants, nephilim, african, oral-tradition, ancestors

**East Asian (3 entries, `"category": "east_asian"`):**

**Entry 1: "chinese-flood-myths"**
- **Title:** "The Chinese Flood and the Flood of Enoch"
- **Claim:** The Chinese flood narrative of Gun-Yu — a catastrophic deluge that covered the earth and was only tamed after divine intervention — preserves structural parallels to the Genesis/Enoch flood account.
- Cover: Gun's failed attempt to stop the flood (steals divine soil, is executed), Yu the Great succeeds (drains the waters, establishes order), Nüwa repairs the broken sky after a cosmic catastrophe
- **Side by side:** God sends flood as judgment / Tian (Heaven) sends flood; Noah builds ark to survive / Gun steals divine soil to block waters; God establishes post-flood order / Yu the Great establishes post-flood order; Rainbow covenant / Nüwa repairs the sky
- **Canonical refs:** Genesis 6-9, 1 Enoch 10:1-2, Isaiah 54:9
- **Tags:** flood, chinese, gun-yu, nuwa, deluge

**Entry 2: "divine-teachers-east-asia"**
- **Title:** "Divine Teachers Who Descended to Earth"
- **Claim:** East Asian traditions of divine culture heroes — beings who descended from heaven and taught humanity the essential arts of civilization — parallel the Watchers' role as teachers of forbidden knowledge.
- Cover: Chinese Fuxi and Nüwa (taught writing, music, fishing, hunting), Japanese Ninigi (descended from heaven with divine regalia), Korean Hwanung (descended from heaven to teach mankind)
- **Side by side:** Watchers descend and teach forbidden arts / Divine heroes descend and teach civilizational arts; Watchers teach in violation of heavenly order / Divine teachers are sent or sanctioned by heaven (the transgression is sanitized); Specific Watchers teach specific arts / Specific culture heroes teach specific arts
- **Canonical refs:** 1 Enoch 8:1-3 (specific Watchers, specific arts), 1 Enoch 9:6
- **Tags:** divine-teachers, descent, fuxi, ninigi, hwanung

**Entry 3: "east-asian-giants"**
- **Title:** "Giant Traditions in East Asian Records"
- **Claim:** Chinese, Japanese, and Korean traditions record the existence of giant beings in ancient times — from the Chinese Kua Fu to the Japanese Daidarabotchi to Korean giant founder myths.
- **Side by side:** Nephilim are giants of the ancient world / Kua Fu, Daidarabotchi, Pangu are giants of the primordial age; Nephilim are destroyed / Ancient giants disappear in cosmic events; Nephilim leave a lasting mark on the earth / Giant myths explain landscape features (mountains, lakes shaped by giants)
- **Canonical refs:** Genesis 6:4, 1 Enoch 7:2-4
- **Tags:** giants, nephilim, kuafu, daidarabotchi, pangu

Full JSON for all 8 entries with complete content.

- [ ] **Step 2: Verify**

Expected: `25 entries: {'mesopotamian': 4, 'greek': 4, 'egyptian': 3, 'norse': 3, 'hindu': 3, 'native_american': 3, 'african': 2, 'east_asian': 3}`

- [ ] **Step 3: Commit**

```bash
git add backend/data/enoch_parallels.json
git commit -m "feat(enoch): add Native American, African, and East Asian parallel entries (8 deep studies)"
```

---

### Task 8: Create Image Manifest and Directory

**Files:**
- Create: `backend/data/enoch_images.json`
- Create: `backend/data/images/enoch/` (directory)

- [ ] **Step 1: Create the images directory**

```bash
mkdir -p /c/AI/MGC_Workbench/apps/trialsofjudah/backend/data/images/enoch
```

- [ ] **Step 2: Create the image manifest with placeholder structure**

Create `backend/data/enoch_images.json` — an empty array that serves as the manifest template:

```json
[]
```

This file is intentionally empty. Images will be added by:
1. Placing the image file in `backend/data/images/enoch/`
2. Adding an entry to this manifest with: `id`, `filename`, `source`, `attribution`, `license`, `caption`, `related_entry_ids`

- [ ] **Step 3: Commit**

```bash
git add backend/data/enoch_images.json
git commit -m "feat(enoch): add image manifest and directory structure"
```

---

### Task 9: Create Enoch Service

**Files:**
- Create: `backend/services/enoch_service.py`
- Test: Manual endpoint test (Task 11)

- [ ] **Step 1: Create the service class**

Create `backend/services/enoch_service.py` following the same pattern as `evidence_service.py`:

```python
"""Enoch study service — loads and queries canon and parallel data."""
import json
from pathlib import Path
from backend.config import DATA_DIR


class EnochService:

    def __init__(self):
        self._canon = None
        self._parallels = None
        self._images = None

    def _load_canon(self):
        if self._canon is not None:
            return
        canon_file = DATA_DIR / "enoch_canon.json"
        if canon_file.exists():
            with open(canon_file, "r", encoding="utf-8") as f:
                self._canon = json.load(f)
        else:
            self._canon = []

    def _load_parallels(self):
        if self._parallels is not None:
            return
        parallels_file = DATA_DIR / "enoch_parallels.json"
        if parallels_file.exists():
            with open(parallels_file, "r", encoding="utf-8") as f:
                self._parallels = json.load(f)
        else:
            self._parallels = []

    def _load_images(self):
        if self._images is not None:
            return
        images_file = DATA_DIR / "enoch_images.json"
        if images_file.exists():
            with open(images_file, "r", encoding="utf-8") as f:
                self._images = json.load(f)
        else:
            self._images = []

    def get_canon(self) -> list:
        """Return all canonicity evidence cards, ordered."""
        self._load_canon()
        return sorted(self._canon, key=lambda c: c.get("order", 0))

    def get_categories(self) -> list:
        """Return the mythology region categories with entry counts."""
        self._load_parallels()
        category_meta = {
            "mesopotamian": {"id": "mesopotamian", "label": "Mesopotamian", "subtitle": "Sumerian & Babylonian"},
            "greek": {"id": "greek", "label": "Greek", "subtitle": "Titans, Olympians & Heroes"},
            "egyptian": {"id": "egyptian", "label": "Egyptian", "subtitle": "The Nile Civilization"},
            "norse": {"id": "norse", "label": "Norse", "subtitle": "The Northern Tradition"},
            "hindu": {"id": "hindu", "label": "Hindu", "subtitle": "Vedic & Puranic"},
            "native_american": {"id": "native_american", "label": "Native American & Mesoamerican", "subtitle": "Traditions of the Americas"},
            "african": {"id": "african", "label": "African", "subtitle": "Oral Traditions of the Continent"},
            "east_asian": {"id": "east_asian", "label": "East Asian", "subtitle": "Chinese, Japanese & Korean"},
        }
        counts = {}
        for entry in self._parallels:
            cat = entry.get("category", "")
            counts[cat] = counts.get(cat, 0) + 1

        result = []
        for cat_id, meta in category_meta.items():
            if counts.get(cat_id, 0) > 0:
                result.append({**meta, "entry_count": counts[cat_id]})
        return result

    def get_parallels(self, category: str = None) -> list:
        """Return parallel entries, optionally filtered by category."""
        self._load_parallels()
        if category:
            return [e for e in self._parallels if e.get("category") == category]
        return self._parallels

    def get_image_manifest(self) -> list:
        """Return the full image manifest."""
        self._load_images()
        return self._images


enoch_service = EnochService()
```

- [ ] **Step 2: Verify syntax**

Run:
```bash
cd /c/AI/MGC_Workbench/apps/trialsofjudah && python3 -c "from backend.services.enoch_service import enoch_service; print('Service loaded OK'); cards = enoch_service.get_canon(); print(f'{len(cards)} canon cards'); cats = enoch_service.get_categories(); print(f'{len(cats)} categories'); entries = enoch_service.get_parallels(); print(f'{len(entries)} parallel entries')"
```
Expected output:
```
Service loaded OK
7 canon cards
8 categories
25 parallel entries
```

- [ ] **Step 3: Commit**

```bash
git add backend/services/enoch_service.py
git commit -m "feat(enoch): add EnochService for data access"
```

---

### Task 10: Add API Endpoints and Route

**Files:**
- Modify: `backend/main.py`

- [ ] **Step 1: Add import**

At the top of `backend/main.py`, after the martyrs_service import (line 20), add:

```python
from backend.services.enoch_service import enoch_service
```

- [ ] **Step 2: Add Enoch API endpoints**

Before the `# ── Frontend` section (before line 391 `@app.get("/{rest_of_path:path}")`), add:

```python
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
```

- [ ] **Step 3: Add DATA_DIR import to main.py**

At the top of `backend/main.py`, update the config import to include DATA_DIR:

```python
from backend.config import SERVER_HOST, SERVER_PORT, FRONTEND_DIR, DATA_DIR
```

- [ ] **Step 4: Add /enoch route**

Replace the existing frontend catch-all route:

```python
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
```

- [ ] **Step 5: Verify endpoints**

Restart the server and test:
```bash
cd /c/AI/MGC_Workbench/apps/trialsofjudah && python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8202 &
sleep 3
curl -s http://localhost:8202/api/enoch/canon | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{len(d[\"canon\"])} canon cards')"
curl -s http://localhost:8202/api/enoch/categories | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{len(d[\"categories\"])} categories')"
curl -s http://localhost:8202/api/enoch/parallels?category=mesopotamian | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{len(d[\"parallels\"])} mesopotamian entries')"
```
Expected:
```
7 canon cards
8 categories
4 mesopotamian entries
```

- [ ] **Step 6: Commit**

```bash
git add backend/main.py
git commit -m "feat(enoch): add /api/enoch/* endpoints and /enoch route"
```

---

### Task 11: Build the Enoch Frontend Page

**Files:**
- Create: `frontend/enoch.html`

- [ ] **Step 1: Create the complete enoch.html page**

Create `frontend/enoch.html` — a standalone HTML page with inline CSS and JS (matching the main app's architecture). The page includes:

**HTML structure:**
- Disclaimer banner (fixed top, dismissable with localStorage persistence)
- Header with title "The Book of Enoch: The Ancient Record", subtitle, and "Return to Trials of Judah" link
- Part 1 section: vertical timeline of canon evidence cards (expandable on click)
- Part 2 section: horizontal category nav bar + deep study entry cards below
- Each entry card has: title, claim, Enoch quotes block, mythology quotes block, two-column side-by-side comparison, images area, canonical refs in Georgia serif, "The Distortion" callout block, key takeaway summary bar

**CSS (inline in `<style>`):**
- Base: `background: #120a06` (slightly darker than main app's `#1a0f0a`), `color: #d4c5b0`
- Gold accent: `#c9a84c` (matching main app)
- Parchment texture effect via CSS gradients on card backgrounds
- Typography: `Georgia, serif` for quotes and scripture, `system-ui` for UI
- Timeline: vertical line with connected dots for Part 1
- Two-column grid for side-by-side comparison (collapses to single column on mobile)
- Category nav bar: horizontal scrollable pills
- Distortion callout: distinct background (`rgba(180, 60, 60, 0.1)`) with left border accent
- Key takeaway: gold-bordered summary bar at card bottom
- Responsive breakpoint at 768px

**JavaScript (inline in `<script>`):**
- State object: `{ canon: [], parallels: [], categories: [], activeCategory: 'mesopotamian', dismissedDisclaimer: false }`
- `loadCanon()`: fetch `/api/enoch/canon`, render timeline cards
- `loadCategories()`: fetch `/api/enoch/categories`, render category nav
- `loadParallels(category)`: fetch `/api/enoch/parallels?category=`, render entry cards
- `toggleCanonCard(id)`: expand/collapse canon evidence cards
- `selectCategory(id)`: update activeCategory, call loadParallels
- `dismissDisclaimer()`: hide banner, save to localStorage
- `init()`: check localStorage for disclaimer, call loadCanon, loadCategories, loadParallels('mesopotamian')
- Image rendering: for each entry's images array, look up image metadata from manifest (fetched once), render `<img>` with caption and attribution. If image array is empty, show nothing (no broken image placeholders).

The full HTML file should be approximately 800-1200 lines with all CSS and JS inline, following the same single-file pattern as the main `index.html`.

- [ ] **Step 2: Verify the page loads**

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8202/enoch
```
Expected: `200`

Open in browser: `http://localhost:8202/enoch`

- [ ] **Step 3: Commit**

```bash
git add frontend/enoch.html
git commit -m "feat(enoch): add standalone Enoch study frontend page"
```

---

### Task 12: End-to-End Verification

**Files:** None (testing only)

- [ ] **Step 1: Verify all API endpoints return valid data**

```bash
cd /c/AI/MGC_Workbench/apps/trialsofjudah
curl -s http://localhost:8202/api/enoch/canon | python3 -c "import sys,json; d=json.load(sys.stdin); assert len(d['canon'])==7, f'Expected 7 got {len(d[\"canon\"])}'; print('Canon: OK (7 cards)')"
curl -s http://localhost:8202/api/enoch/categories | python3 -c "import sys,json; d=json.load(sys.stdin); assert len(d['categories'])==8, f'Expected 8 got {len(d[\"categories\"])}'; print('Categories: OK (8 regions)')"
curl -s http://localhost:8202/api/enoch/parallels | python3 -c "import sys,json; d=json.load(sys.stdin); assert len(d['parallels'])==25, f'Expected 25 got {len(d[\"parallels\"])}'; print('Parallels: OK (25 entries)')"
curl -s http://localhost:8202/api/enoch/parallels?category=greek | python3 -c "import sys,json; d=json.load(sys.stdin); assert len(d['parallels'])==4; print('Greek filter: OK (4)')"
curl -s http://localhost:8202/api/enoch/parallels?category=african | python3 -c "import sys,json; d=json.load(sys.stdin); assert len(d['parallels'])==2; print('African filter: OK (2)')"
```

- [ ] **Step 2: Verify frontend page renders**

```bash
curl -s http://localhost:8202/enoch | python3 -c "import sys; html=sys.stdin.read(); assert 'The Book of Enoch' in html; assert 'The Ancient Record' in html; print('Frontend: OK')"
```

- [ ] **Step 3: Verify main app is unaffected**

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8202/
curl -s http://localhost:8202/api/health | python3 -c "import sys,json; d=json.load(sys.stdin); assert d['status']=='ok'; print('Main app: OK')"
```

- [ ] **Step 4: Final commit**

```bash
git add -A
git status
git commit -m "feat(enoch): complete Book of Enoch study section — canon evidence, 25 mythology parallels across 8 cultures, standalone frontend"
```
