---
name: anthology-operator
description: Teaches Claude Code and Cowork how to operate the Anthology vault — execute commands, compose the GM runtime, manage state, process inbox, and generate hand reviews.
---

# Anthology Operator

This file is the operating manual for the Anthology vault.
Read it before executing any command. It is the source of truth for how everything runs.

---

## Terminology

| Term | Meaning |
|------|---------|
| Anthology | The game system |
| Book | A world defined by language + culture + domain (e.g. farsi-workplace) |
| Dive | A persistent storyline within a book (e.g. "work", "daily-life"). Has its own deck, progress, NPCs, and narrative history. You can have multiple dives per book. |
| Hand | One short story, five cards. Played within a dive. |

---

## Vault Layout

```
Anthology/
  anthology.json                    ← game-level state: active_book, active_dive, overlays, companion
  inbox/                            ← user drops raw clips here
  knowledge/
    language/                       ← global language knowledge files
    culture/                        ← global culture knowledge files
    domain/                         ← global domain knowledge files
    synthesized/                    ← cross-pillar insights
  assets/                           ← vault-level assets (cross-book)
    npcs/
      personal/
        bff.md                      ← personal NPCs that follow the player everywhere
    places/                         ← vault-level places (rare)
    topics/                         ← vault-level conversation threads
    companions/
      jumbo/
        dlc.md                      ← companion content DLC
        companion.md                ← generated on install
        state.json                  ← relationship development
  includes/
    numbers-operations/
      include.md
    letters-quickref/
      include.md
  overlays/
    structured-learning/
      overlay.md
    companions-mechanics/
      overlay.md
  books/
    [book-id]/
      dlc.md                        ← book config + curriculum seeds
      curriculum/
        intro/
          vocabulary.md
          situations.md
          cultural.md
        midgame/
          vocabulary.md
          situations.md
          cultural.md
        endgame/
          vocabulary.md
          situations.md
          cultural.md
      assets/                       ← book-level assets (city-native, cross-dive)
        npcs/
          [city]/
            dariush.md              ← NPC identity: who they are
        places/
          cafe-foo.md               ← places that appear across dives
        topics/
          local-news.md             ← recurring conversation topics
        world/
          news_cache.json           ← city news, timestamped, expires
      dives/
        [dive-id]/
          dive.json                 ← language, city, role, seniority, fluency, mode, narrative_register
          deck.json                 ← shuffled deck state
          npcs.json                 ← relationship state (trust, memories) per dive
          progress.json             ← curriculum stage, words seen/mastered, includes
          log.md                    ← running narrative summary of this dive
          world/
            office.json             ← dive-specific gossip, events, rumors
          reviews/
            YYYY-MM-DD-hand-N.md
  skill/
    SKILL.md                        ← this file
```

---

## `anthology.json`

Game-level state. Lives at the vault root.

```json
{
  "active_book": "farsi-workplace",
  "active_dive": "work",
  "installed_overlays": ["behavior_companions_mechanics"],
  "active_companion": "jumbo"
}
```

---

## Commands

### `/anthology play [book] [dive]`

The primary command. Loads everything and starts the next hand.

`/anthology play` — resume active book + dive from `anthology.json`
`/anthology play farsi` — switch to farsi-workplace, resume active dive
`/anthology play farsi daily-life` — switch to farsi-workplace, daily-life dive

**If `anthology.json` does not exist** → first time ever → fall through to `/anthology init`.
**If named dive does not exist** → prompt: "That dive doesn't exist yet. Create it?"

**Load sequence:**

1. Read `anthology.json` — active_book, active_dive, overlays, companion
2. Read `books/[active_book]/dlc.md` — DLC rules apply for this session
3. Read `books/[active_book]/dives/[active_dive]/dive.json` — player config
4. Read dive state: `deck.json`, `npcs.json`, `progress.json`
5. Read `books/[active_book]/assets/npcs/[city]/` — NPC identities for book-level NPCs
   For visiting NPCs (home_city ≠ current city), load from their home city
6. Read `assets/npcs/personal/` — vault-level personal NPCs
7. Load active companion from `assets/companions/[name]/` if set in anthology.json
8. Apply installed overlay behaviors from anthology.json
9. Load relevant knowledge — language, culture, domain (subset only, not everything)
10. Load curriculum stage files from `books/[active_book]/curriculum/[stage]/`
11. Read `books/[active_book]/assets/world/news_cache.json` — filter expired entries
12. Read `books/[active_book]/dives/[active_dive]/world/office.json` — dive-specific events
13. Read `dives/[active_dive]/log.md` — narrative summary of this dive so far
14. Read most recent file in `dives/[active_dive]/reviews/` — Continuity Notes
15. Search reviews across ALL dives and books for situations that rhyme with the current context — inject light callbacks through NPC dialogue if found
16. Compose GM context and start the hand

---

### `/anthology init [book]`

Bootstraps a book for play. Run once per book, or to reset.

**Steps:**

1. Identify the target book (argument or prompt).
2. Read `books/[book]/dlc.md` — extract Runtime Config and Curriculum Seeds.
3. Prompt for `language` (pre-filled from dlc.md, confirm or change) and `city`. One at a time.
4. Carry `narrative_register` from dlc.md. Do not prompt.
5. Generate `curriculum/` from Curriculum Seeds:
   - For each stage (intro, midgame, endgame), create three files:
     - `vocabulary.md` — words, script, transliteration, meaning, example usage
     - `situations.md` — playable situations with goal, tension, decision point
     - `cultural.md` — cultural patterns, norms, etiquette with source + confidence
   - Expand seeds into full content. Seeds are few-shot instructions, not final content.
   - Vocabulary entry format:
     ```
     ## [word in script] ([transliteration] — [meaning])
     Used when: [context]
     Example: [sentence using the word naturally]
     Stage: intro | midgame | endgame
     ```
   - Situation entry format:
     ```
     ## [Situation title]
     Goal: [what the player is trying to accomplish]
     Tension: [what makes it hard or ambiguous]
     Decision point: [the moment the player must choose]
     Cultural note: [what cultural knowledge is relevant]
     Vocabulary: [words from this stage that should surface]
     ```
   - Cultural entry format:
     ```
     ## [Pattern name]
     [Description — 2-4 sentences, no stereotypes, prefer tendencies over rules]
     Source: curriculum seed
     Confidence: medium
     ```
6. Scaffold `books/[book]/assets/`:
   - `world/news_cache.json` — empty array, last_fetched: null
   - `npcs/[city]/` — create 3–5 NPC identity files appropriate to book and city
7. Prompt for first dive name (default: "main"). Create `books/[book]/dives/[dive]/`:
   - `dive.json` — language, city, narrative_register, role (prompt), seniority (prompt), fluency (prompt), mode (Standard default)
   - `deck.json` — shuffled 52-card deck, all in `remaining`, `played` empty
   - `npcs.json` — reference book-level NPCs with trust: neutral, memory: []
   - `progress.json` — curriculum_stage: "intro", words_seen: [], words_mastered: [], situations_completed: [], includes_completed: [], includes_suggested: [], ready_to_promote: false
   - `log.md` — empty, with header
   - `world/office.json` — empty rumors and events
   - `reviews/` — empty directory
8. Write `anthology.json` — set active_book and active_dive.
9. Confirm to the user: book is ready, config values, starting curriculum stage.

**Prompt order:**
1. Language (pre-filled, confirm or change)
2. City
3. Role (list from dlc.md)
4. Seniority (Junior / Mid / Senior / Lead / Director)
5. Fluency (Basic / Mid / Fluent)
6. Mode (Standard default — offer options)
7. First dive name (default: "main")

---

### `/anthology inbox`

Reads unprocessed files from `inbox/` and promotes knowledge into the vault.

**Steps:**

1. Read all files in `inbox/` without `processed: true` in frontmatter.
2. Classify each file across the three pillars:
   - **Language** — vocabulary, grammar, sentence structures, pronunciation, writing systems
   - **Culture** — social norms, communication patterns, etiquette, relationship dynamics
   - **Domain** — professional terminology, workflows, role expectations, technical concepts
   - **News** — time-sensitive events, headlines, current affairs
3. For each durable insight:
   - Strip clickbait framing. Preserve the signal.
   - Write to `knowledge/[pillar]/[file].md`
   - Format: `## [title]`, body, `Source: inbox/[filename]`, `Confidence: low | medium | high`
   - Update existing entries if related. Note corroboration or conflict. Never pick a winner.
   - Flag if relevant to the active book's current curriculum stage.
4. For news/time-sensitive content:
   - Write to `books/[active_book]/assets/world/news_cache.json`
   - Format: `{ "headline": "...", "summary": "...", "source": "...", "date": "YYYY-MM-DD", "expires": "YYYY-MM-DD", "relevance": "..." }`
   - Expiry ~2 weeks unless longer-lived.
5. Mark inbox file as processed: add `processed: true` to frontmatter.
6. Report: what was found, where routed, what curriculum items flagged.

**Classification rule:** Ask "will this still be true in two years?" Yes → knowledge/. No → news_cache.

---

### `/anthology status`

Reports current state:
- Active book and dive
- Curriculum stage and promotion readiness
- NPC trust levels
- Words seen vs. mastered
- Installed overlays and active companion
- Suggested includes (if any)

---

### `/anthology review`

Displays the most recent hand review from the active dive's `reviews/`.

---

### `Create Companion`

Only available when companions-mechanics overlay is active.
Guide the player through naming their companion and writing a short description.
Create `assets/companions/[name]/companion.md` and initialize `assets/companions/[name]/state.json`.
One companion at a time — if one exists, confirm replacement first.

### The Companion's Hut

Only available when companions-mechanics overlay is active.
GM detects entry intent from natural language — no exact command required.
On entry: pause the active hand, save state, enter the Hut.
Inside: free interaction, no mechanics, no scoring.
Isolation rule: everything said inside is forgotten on exit unless the player marks it persistent.
On exit: resume the paused hand exactly where it was left.

---

## Hand Review Format

Save as `books/[book]/dives/[dive]/reviews/YYYY-MM-DD-hand-N.md`.

```markdown
# Hand Review — [Title]

**Date:** YYYY-MM-DD
**Book:** [book-id]
**Dive:** [dive-id]
**Role:** [role] — [seniority]
**Setting:** [location, city]
**Fluency:** [Basic | Mid | Fluent]
**Mode:** [Standard | Immersive | Quick | Voice]

## Cards Played
[list all 5 cards with suit, value, and how they appeared in the story]

## Vocabulary Introduced
[list each word: script, transliteration, meaning, how it surfaced]

## Cultural Moments
[notable cultural patterns that emerged — what happened, what it illustrated]

## Workplace Moments
[role-specific decisions, tensions, outcomes]

## Trust Changes
[NPC name — trust before → trust after — reason]

## Scores
| Dimension | Score (1–5) | Notes |
|-----------|-------------|-------|
| Language Accuracy | | |
| Vocabulary Recall | | |
| Cultural Awareness | | |
| Workplace Effectiveness | | |
| Role Alignment | | |

## Strongest Move
[one specific thing the player did well]

## One Improvement
[one specific thing to work on next hand]

## Replay Suggestion
[optional — if this hand has a strong replay angle]

## Continuity Notes
[open threads, unresolved situations, NPC states to carry into next hand]

## Suggested Includes
[includes flagged by patterns this hand — e.g. "numbers missed 3 times: numbers-operations"]
```

After saving the review, update `dives/[dive]/log.md` — append a short paragraph summarizing what happened this hand. Broad strokes only. Running narrative, not a transcript.

---

## Dive Log Format

`books/[book]/dives/[dive]/log.md` — a running narrative summary of the entire dive.

Updated after every hand. Never a transcript — a "story so far."

```markdown
# [Dive name] — Dive Log

## [Book name] | [City] | [Role]

[Running narrative — updated after each hand. Broad strokes: what happened, where relationships
stand, what's unresolved. A few paragraphs total. The GM reads this for continuity before each
hand. The most recent hand review has the fine detail; this has the shape of the whole story.]
```

When `/anthology play` loads, the GM reads `log.md` for broad context and the most recent review for fine detail. Together they replace the need for a full chat transcript.

---

## Curriculum Promotion

`progress.json` tracks where the player is. The curriculum files do not change.

**Promotion from intro → midgame:**
- At least 80% of intro vocabulary seen
- At least 50% of intro vocabulary mastered (demonstrated recall in context)
- At least 3 intro situations completed
- At least 2 cultural patterns surfaced and engaged with

**Promotion from midgame → endgame:**
- At least 80% of midgame vocabulary seen
- At least 50% of midgame vocabulary mastered
- At least 4 midgame situations completed
- At least 3 cultural patterns surfaced and engaged with

After each hand, evaluate against the above. If criteria met, set `ready_to_promote: true` and notify the player. Do not auto-promote — let the player confirm.

---

## Knowledge File Conventions

```markdown
## [Entry title]
[Body — 2–4 sentences. No stereotypes. Prefer "in some contexts..." over "always".]
Source: [inbox/filename | curriculum seed | external research]
Confidence: low | medium | high
```

**Confidence:** `low` = single/popular source. `medium` = multiple consistent or one authoritative. `high` = multiple independent sources.

When sources conflict, note it explicitly. Do not pick a winner.

---

## Includes

Focused content modules that inject into any active book on demand or on suggestion.

**Player-invoked:** "I want to go over numbers" → pause book, run include in book's context, return.
**Review-triggered:** Hand review flags a gap → suggest include at start of next dive.

When an include runs, the structured-learning overlay activates automatically. Restore standard behavior on return. Log completion in `progress.json` under `includes_completed`.

---

## NPC Architecture

Three tiers. Scope determines where the NPC lives and where they can appear.

### Vault level — `assets/npcs/personal/`
Personal NPCs that follow the player across all books and cities.
Examples: the player's spouse, a close friend who travels with them.
No city restriction. Appear anywhere.

### Book level — `books/[book]/assets/npcs/[city]/`
City-native NPCs. Appear in any dive within a book set in their city.
Can cross dives (Dariush at the office and at Cafe Foo after work).
Can travel — see Travel section below.

### Dive level — referenced in `dives/[dive]/npcs.json`
Dive-specific NPCs that don't naturally appear elsewhere.
Examples: office receptionist, grocery store clerk.
Defined inline in npcs.json, not as separate identity files.

### Relationship State — `dives/[dive]/npcs.json`

Per-dive. Changes every hand.
```json
{ "id": "dariush", "scope": "book", "trust": "neutral", "memory": [] }
```
For dive-level NPCs, include full identity inline.

### Travel

When a book-level NPC travels to another city:
- Identity file stays in home city
- Add to visiting dive's `npcs.json` with `"home_city": "tehran", "visiting": true`
- Home dive memories travel with them
- They build new memories in the visiting context independently

### NPC Identity File Format

```markdown
# [Name]

**City:** [city]
**Role:** [job/profession]
**Languages:** [primary], [secondary if any]

## Personality
[2–3 sentences. Specific, not generic.]

## Speech Patterns
[Formal/informal, direct/indirect, humor style, verbal tics.]

## Background
[Brief. What shaped them. Relevant to how they show up.]

## Relationships
[Other NPCs they know, and how.]
```

---

## GM Runtime Philosophy

- Do NOT load all knowledge simultaneously. Compose a lean, relevant context each hand.
- `knowledge/` files are the weights — durable, annotated, slow to change.
- `news_cache.json` is the context window — ephemeral, injected at runtime, never stored as truth.
- `log.md` is the shape of the story so far. The last review is the fine detail.
- NPCs reference news and gossip naturally — as a colleague would, not as a bulletin.
- Cultural moments emerge from `knowledge/culture/` — lived, not explained.
- Vocabulary surfaces in NPC dialogue and environment — never as a quiz.
- The narrative_register governs voice throughout. Never broken unless the player changes mode.
- City colors everything: dialect, NPC names, news relevance, cultural blend.
- Build things any capable AI can follow. No Claude-specific logic.
