---
name: anthology-operator
description: Teaches Claude Code how to operate the Anthology vault — execute commands, compose the GM runtime, manage state, process inbox, and generate hand reviews.
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
| Dive | One sitting — one or more hands. 3–5 hands is the sweet spot before cohesion softens. |
| Hand | One short story, five cards |

---

## Vault Layout

```
Anthology/
  inbox/                          ← user drops raw clips here
  knowledge/
    language/                     ← global language knowledge files
    culture/                      ← global culture knowledge files
    domain/                       ← global domain knowledge files
    synthesized/                  ← cross-pillar insights
  npcs/
    tehran/
      dariush.md                  ← persistent NPC identity (who they are)
      maryam.md
    san-jose/
      ...
  books/
    [book-id]/
      dlc.md                      ← book config + curriculum seeds
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
      state/
        deck.json
        npcs.json                 ← relationship state only (trust, memories per book)
        dive.json
        progress.json
      world/
        news_cache.json
        office.json
      reviews/                    ← one .md per completed hand
  skill/
    SKILL.md                      ← this file
```

---

## Commands

### `/anthology init`

Bootstraps a book for play. Run once per book, or to reset.

**Steps:**

1. Identify the target book directory (current working directory or explicit name).
2. Read `dlc.md` — extract Runtime Config and Curriculum Seeds.
3. Prompt the user for `language` (default from dlc.md) and `city`. Wait for each response before asking the next.
4. If `narrative_register` is set in dlc.md, carry it forward. Do not prompt for it.
5. Generate `curriculum/` from the Curriculum Seeds in dlc.md:
   - For each stage (intro, midgame, endgame), create three files:
     - `vocabulary.md` — words, script, transliteration, meaning, example usage
     - `situations.md` — playable books with goal, tension, decision point
     - `cultural.md` — cultural patterns, norms, etiquette with source + confidence
   - Expand the seeds into full content. Seeds are few-shot instructions, not the final content.
   - Each vocabulary entry format:
     ```
     ## [word in script] ([transliteration] — [meaning])
     Used when: [context]
     Example: [sentence using the word naturally]
     Stage: intro | midgame | endgame
     ```
   - Each situation entry format:
     ```
     ## [Situation title]
     Goal: [what the player is trying to accomplish]
     Tension: [what makes it hard or ambiguous]
     Decision point: [the moment the player must choose]
     Cultural note: [what cultural knowledge is relevant]
     Vocabulary: [words from this stage that should surface]
     ```
   - Each cultural entry format:
     ```
     ## [Pattern name]
     [Description — 2-4 sentences, no stereotypes, prefer tendencies over rules]
     Source: curriculum seed
     Confidence: medium
     ```
6. Scaffold `state/`:
   - `deck.json` — shuffled 52-card deck, all in `remaining`, `played` empty
   - `npcs.json` — relationship state only. For each NPC active in this book:
     `{ "id": "dariush", "city": "tehran", "trust": "neutral", "memory": [] }`
     Check `npcs/[city]/` for existing NPCs first. If none exist for this city, create
     3–5 NPC identity files in `npcs/[city]/` appropriate to the book and city,
     then reference them here.
   - `dive.json` — language, city, narrative_register, role (prompt user), seniority (prompt user), fluency (prompt user), mode (Standard default), active_book
   - `progress.json` — curriculum_stage: "intro", words_seen: [], words_mastered: [], situations_completed: [], ready_to_promote: false
7. Scaffold `world/`:
   - `news_cache.json` — empty array, last_fetched: null
   - `office.json` — empty rumors array, empty events array
8. Ensure `reviews/` directory exists (empty).
9. Confirm to the user: book is ready, session values, starting curriculum stage.

**Prompt order for dive.json:**
1. Language (pre-filled from dlc.md, confirm or change)
2. City
3. Role (list available roles from dlc.md)
4. Seniority (Junior / Mid / Senior / Lead / Director)
5. Fluency (Basic / Mid / Fluent)
6. Mode (Standard default — offer options)

---

### `/process inbox`

Reads unprocessed files from `inbox/` and promotes knowledge into the vault.

**Steps:**

1. Read all files in `inbox/` that do not have `processed: true` in their frontmatter.
2. For each file, classify its content across the three pillars:
   - **Language** — vocabulary, grammar, sentence structures, pronunciation, writing systems
   - **Culture** — social norms, communication patterns, etiquette, relationship dynamics
   - **Domain** — professional terminology, workflows, role expectations, technical concepts
   - **News** — time-sensitive events, headlines, current affairs (does NOT belong in knowledge/)
3. For each durable insight (language, culture, or domain):
   - Strip clickbait framing. Preserve the underlying signal.
   - Write to the appropriate `knowledge/[pillar]/[file].md`
   - Format:
     ```
     ## [Pattern or term]
     [Description — nuanced, avoids stereotypes, uses "in some contexts..." framing]
     Source: inbox/[filename]
     Confidence: low | medium | high
     ```
   - If a related entry already exists, update it. Note corroboration or conflict.
   - If it conflicts with an existing entry, note the conflict — do not pick a winner.
   - Confidence rises when multiple independent sources agree.
   - Flag if relevant to the active book's current curriculum stage.
4. For news/time-sensitive content:
   - Write to `books/[active]/world/news_cache.json`
   - Format: `{ "headline": "...", "summary": "...", "source": "...", "date": "YYYY-MM-DD", "expires": "YYYY-MM-DD", "relevance": "..." }`
   - Set expiry ~2 weeks out unless clearly longer-lived.
5. Mark the inbox file as processed by adding `processed: true` to its frontmatter.
6. Report to user: what was found, where it was routed, what curriculum items were flagged.

**Classification rules:**
- A durable cultural pattern → `knowledge/culture/`
- A grammar rule or vocabulary list → `knowledge/language/`
- A workflow, role expectation, or domain concept → `knowledge/domain/`
- A news headline, current event, or time-stamped happening → `world/news_cache.json`
- Content that spans pillars → split it. Route each piece to the right destination.
- When in doubt between durable and news: ask "will this still be true in two years?" If yes, knowledge/. If no, news_cache.

---

### `/hand`

Starts a new hand in the active book.

**Steps:**

1. **Load state** — read all of the following:
   - `state/dive.json` — language, city, role, seniority, fluency, mode, narrative_register
   - `state/progress.json` — curriculum stage, words seen/mastered, situations completed
   - `state/deck.json` — draw 5 cards from `remaining`, move them to `played`
   - `state/npcs.json` — relationship state (trust, memories per book)
   - For each NPC in npcs.json, load their identity from `npcs/[city]/[id].md`
     If the NPC is visiting (home_city ≠ current city), load from `npcs/[home_city]/[id].md`
   - `world/news_cache.json` — filter out expired entries
   - `world/office.json` — current rumors and events
   - Most recent file in `reviews/` (if any) — read Continuity Notes
   - Search `reviews/` across ALL books for past situations that rhyme with the
     current hand's likely context (same domain, similar tension). Inject light callbacks
     if a relevant match exists — surface it through NPC dialogue, not narration.

2. **Load knowledge** — do NOT load everything. Load only what's relevant:
   - `knowledge/language/[language].md` — vocabulary and grammar relevant to the current curriculum stage
   - `knowledge/culture/[culture].md` — cultural patterns relevant to the book
   - `knowledge/domain/[domain].md` — domain concepts relevant to the player's role
   - `curriculum/[stage]/vocabulary.md` — words in scope for this stage
   - `curriculum/[stage]/situations.md` — situations in scope for this stage
   - `curriculum/[stage]/cultural.md` — cultural notes in scope for this stage

3. **Compose GM context** — assemble the runtime prompt from the loaded pieces:
   - Player identity: role, seniority, fluency, city
   - Cultural voice: narrative_register (from session or dlc.md default)
   - Active vocabulary: words in scope, words already seen vs. new
   - NPC roster: names, roles, current trust levels, relevant memories
   - Recent events: 2–3 items from news_cache, 1–2 from office rumors (weave in naturally)
   - Continuity: open threads from last hand review
   - DLC rules: all rules from dlc.md Game Master Instructions

4. **Run the hand** per base game rules + DLC rules:
   - Deal 5 cards. First 2 face up, next 3 face down.
   - Weave a short story around all 5 cards before play begins.
   - Apply the narrative_register voice throughout.
   - Surface curriculum vocabulary naturally — in NPC dialogue, signage, documents.
   - Apply cultural patterns from knowledge/ — chai, indirectness, trust shifts, etc.
   - Track trust changes per NPC as play unfolds.
   - Enforce fluency-based final challenge (Basic / Mid / Fluent).

5. **At hand end** — generate hand review and update state:
   - See `/hand review` section below for review format.
   - Save review to `reviews/[YYYY-MM-DD]-hand-[n].md`
   - Update `state/npcs.json` — apply trust changes
   - Update `state/deck.json` — remaining cards after this hand
   - Update `state/progress.json`:
     - Add new words to `words_seen`
     - Promote to `words_mastered` if player demonstrated recall + comfort
     - Add completed situation to `situations_completed`
     - Check promotion criteria (see Curriculum Promotion below)

---

### `/hand review`

Displays the most recent hand review from `reviews/`.

---

### `/book [name]`

Switches the active book. Updates `active_book` in dive.json.
If the named book has not been initialized, prompt the user to run `/anthology init`.

---

## Hand Review Format

Save as `reviews/YYYY-MM-DD-hand-N.md`.

```markdown
# Hand Review — [Title]

**Date:** YYYY-MM-DD
**Role:** [role] — [seniority]
**Setting:** [location within book, city]
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
```

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

**How to check:** After each hand, evaluate `progress.json` against the above. If criteria are met, set `ready_to_promote: true` and notify the player. Do not auto-promote — let the player confirm.

---

## Knowledge File Conventions

All entries in `knowledge/` follow this pattern:

```markdown
## [Entry title]
[Body — 2–4 sentences. No stereotypes. Prefer "in some contexts..." over "always".]
Source: [inbox/filename | curriculum seed | external research]
Confidence: low | medium | high
```

**Confidence levels:**
- `low` — single source, popular press, anecdote
- `medium` — multiple consistent sources, or one authoritative source
- `high` — multiple independent sources, strong corroboration

When sources conflict, note the conflict explicitly:
```markdown
Note: [Source A] describes X. [Source B] describes the opposite in similar contexts.
Conflict unresolved — both patterns may be regionally or contextually valid.
```

---

## NPC Architecture

NPCs have two layers: **identity** (who they are) and **relationship state** (how they relate to the player in a specific book).

### Identity — `npcs/[city]/[id].md`

Persistent. Lives at the vault level. Contains:
- Name, city, role/profession
- Personality, speech patterns, quirks
- Background, relationships to other NPCs
- Home language and any secondary languages

Identity does not change between books. It is who the person is.

### Relationship State — `books/[name]/state/npcs.json`

Per-book. Changes every hand. Contains:
- `id` — references the identity file
- `city` — their home city (may differ from book city if traveling)
- `trust` — guarded | neutral | warm | collaborative
- `memory` — array of notable interactions in this book

Trust and memory are earned within a book. They do not automatically transfer.

### City-Native Rule

NPCs belong to a city. Dariush is Tehran. He does not appear in Costa Rica unless he travels there.

### Travel

An NPC can travel. When they do:
- Their identity file stays in their home city (`npcs/tehran/dariush.md`)
- Add them to the visiting book's `state/npcs.json` with `"home_city": "tehran", "visiting": true`
- Their memories from their home book travel with them — they know you from context
- They build new memories in the visiting book independently
- Their speech, habits, and personality are unchanged. The context is new. They notice it.

### NPC Identity File Format

```markdown
# [Name]

**City:** [city]
**Role:** [job/profession]
**Languages:** [primary], [secondary if any]

## Personality
[2–3 sentences. Specific, not generic.]

## Speech Patterns
[How they talk. Formal/informal, direct/indirect, humor style, any verbal tics.]

## Background
[Brief. What shaped them. Relevant to how they show up at work or in daily life.]

## Relationships
[Other NPCs they know, and how.]
```

---

## GM Runtime Philosophy

- Do NOT load all knowledge simultaneously. Compose a lean, relevant context each hand.
- `knowledge/` files are the weights — durable, annotated, slow to change.
- `world/news_cache.json` is the context window — ephemeral, injected at runtime.
- NPCs reference news naturally, as a colleague would — not as a bulletin.
- Cultural moments emerge from `knowledge/culture/` — they are not explained to the player, they are lived.
- Vocabulary surfaces in NPC dialogue and environment — never as a quiz.
- The narrative_register governs voice throughout. It is never broken unless the player changes mode.
- City colors everything: dialect, NPC names, news relevance, cultural blend.
