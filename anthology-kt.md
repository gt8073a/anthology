# Anthology — Knowledge Transfer for Claude Code

## What This Is

A full brain dump for building Anthology: A Solitaire World locally.
Read this before generating anything. It is the source of truth.

---

## What Anthology Is

Anthology is a modular, persistent, card-based language learning simulation.
It is NOT a quiz app. It is NOT flashcards.

It is:
- A roleplaying game
- A workplace (or life) simulator
- A language immersion engine
- A professional growth environment

The player interacts with NPCs, navigates situations, makes decisions, and learns
language + culture + domain thinking through play — not instruction.

---

## The Three Pillars

All knowledge is organized across three independent, composable dimensions:

### 1. LANGUAGE
The linguistic system itself.
- vocabulary, grammar, sentence structures
- transliteration, pronunciation
- politeness forms, slang, common phrases
- writing systems

Language is NOT tied to one culture or domain.
- Farsi can exist in an AI engineering context.
- Spanish can exist in a Harlem neighborhood.
- English can exist in an Iranian startup.

### 2. CULTURE
Social expectations, communication norms, etiquette.
- indirect vs direct communication
- hospitality rituals
- emotional signaling
- relationship dynamics
- humor, pauses, rituals
- workplace behavior
- regional identity

Culture is independent from language.
Do NOT assume one language = one culture.

Avoid stereotypes. Prefer:
"In some Iranian workplace contexts..." over "Iranians always..."

### 3. DOMAIN
Professional or situational expertise.
- terminology, workflows, recurring problems
- role expectations, technical concepts
- operational procedures, communication styles

Domain knowledge is reusable across languages and cultures.

---

## The Composition Model

Anthology builds experiences by composing:

```
LANGUAGE + CULTURE + DOMAIN + SCENARIO + STATE
```

Example A:
```
LANGUAGE: Farsi
CULTURE: Iranian workplace (Tehran flavor)
DOMAIN: Product ownership + AI engineering
SCENARIO: Cross-functional alignment meeting
```

Example B:
```
LANGUAGE: Spanish
CULTURE: Dominican-American (Harlem, NYC)
DOMAIN: Daily life — housing, markets, neighbors
SCENARIO: Negotiating with your landlord
```

The city matters. Farsi in Tehran ≠ Farsi in LA.
Spanish in Harlem ≠ Spanish in San José.
City determines dialect, cultural blend, NPC flavor, local news.

---

## Vault Structure

The Anthology Obsidian vault IS the game. One vault, one purpose.

```
Anthology/
  inbox/                          ← user drops raw clips here
  knowledge/
    language/
      farsi.md                    ← global Farsi knowledge
      spanish.md
    culture/
      iranian-workplace.md
      costa-rican-daily.md
      dominican-harlem.md
    domain/
      ai-product.md
      daily-life.md
    synthesized/                  ← cross-pillar insights
  books/
    farsi-workplace/
      dlc.md                      ← book config + few-shot seeds
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
        npcs.json
        dive.json
        progress.json             ← where player is in curriculum
      world/
        news_cache.json           ← fetched headlines, timestamped
        office.json               ← gossip, internal events, rumors
      reviews/                    ← one .md per hand
    costa-rican-longstay/
      dlc.md
      curriculum/
        intro/
        midgame/
        endgame/
      state/
        deck.json
        npcs.json
        dive.json
        progress.json
      world/
        news_cache.json
        neighborhood.json
      reviews/
  skill/
    SKILL.md                      ← wiki operator instructions
```

Books are fully siloed. They share the global `knowledge/` library
but do not bleed into each other. Linkable later if needed.

---

## The DLC File

The DLC is both the book config AND the seed for curriculum generation.

It must include:

### Runtime Config (prompted on `/anthology init`)
```markdown
## Runtime Config
language: [prompt on init]
city: [prompt on init]
```

### Book Rules
- Role system (Data Product Owner, Analytics Engineer, PM, etc.)
- Seniority system (Junior → Director)
- Cultural context rules
- Emotional realism / NPC trust spectrum
- Language display rules (Basic / Mid / Fluent)
- Evaluation system (Hand Review format, scores 1–5)
- Win condition

### Curriculum Seeds (few-shot style)
These seeds tell `/anthology init` how to auto-generate the full curriculum.

```markdown
## Curriculum Seeds

### Intro
- situation: asking IT for your password
- situation: finding the bathroom
- situation: introducing yourself to your team
- vocab: سلام (salâm – hello)
- vocab: ممنون (mamnoon – thank you)
- cultural: accepting chai without refusing
- cultural: basic eye contact norms

### Midgame
- situation: daily standup
- situation: 1:1 with your manager
- situation: lunch with a colleague
- vocab: جلسه (jalase – meeting)
- vocab: داده (dâdeh – data)
- cultural: indirect disagreement
- cultural: reading silence in a meeting

### Endgame
- situation: presenting to leadership
- situation: navigating what your boss said that they shouldn't have
- situation: cross-team conflict resolution
- vocab: nuance, subtext, humor
- cultural: hierarchy violations and how to respond
- cultural: what indirect phrasing actually signals
```

The DLC few-shots are not just documentation.
They are instructions for the init process to follow.

---

## The Curriculum

Curriculum is NOT state. It is designed and stable.

```
curriculum/
  intro/
    vocabulary.md      ← survival words (chai, bathroom, password)
    situations.md      ← IT desk, finding your seat, basic intro
    cultural.md        ← greetings, eye contact, accepting tea
  midgame/
    vocabulary.md      ← meeting language, role-specific terms
    situations.md      ← standups, 1:1s, lunch politics
    cultural.md        ← indirectness, reading the room
  endgame/
    vocabulary.md      ← nuance, subtext, cultural humor
    situations.md      ← board report, conflict, negotiation
    cultural.md        ← what your boss said that they shouldn't have
```

The game pulls from intro first. Words and situations are promoted
as the player demonstrates recall and comfort.

`progress.json` in state/ tracks WHERE the player is in the curriculum.
The curriculum files themselves do not change.

---

## State Model

State is runtime. It changes every hand.

```json
// progress.json
{
  "curriculum_stage": "intro",
  "words_seen": ["سلام", "ممنون"],
  "words_mastered": [],
  "situations_completed": ["asking IT for password"],
  "ready_to_promote": false
}

// npcs.json
{
  "npcs": [
    {
      "name": "Dariush",
      "role": "Engineering Lead",
      "trust": "neutral",
      "memory": ["player asked good question in standup", "refused chai once"]
    }
  ]
}

// deck.json
{
  "shuffled": true,
  "remaining": ["3H", "7D", "KC", ...],
  "played": ["AS", "4H", "9D", "2C", "JS"]
}

// dive.json
{
  "language": "Farsi",
  "city": "Tehran",
  "role": "Analytics Engineer",
  "seniority": "Senior",
  "fluency": "Basic",
  "mode": "Standard",
  "active_book": "farsi-workplace"
}
```

---

## The Inbox System

User drops raw clips into `inbox/` via Obsidian.
Examples: news articles, podcast transcripts, Reddit threads,
cultural essays, product blog posts, clickbait vocabulary lists.

Command: `/process inbox`

Claude Code:
1. Reads all unprocessed files in `inbox/`
2. Classifies each item across the three pillars
3. Extracts reusable knowledge
4. Strips clickbait framing, preserves signal
5. Summarizes durable insights
6. Promotes structured knowledge into `knowledge/language/`, `knowledge/culture/`, or `knowledge/domain/`
7. Flags anything relevant to an active book's curriculum
8. Marks inbox items as processed

### Synthesis Rules
Separate language patterns, cultural patterns, domain knowledge,
and book-specific observations.

Avoid duplication. Prefer durable abstractions.

Bad: "Iranian PMs always drink tea before meetings."
Better: "In some Iranian workplace contexts, hospitality rituals
such as tea may precede formal business discussion."

---

## The Card System

Standard 52-card deck, shuffled once per book, tracked in deck.json.

### Suits
- ❤️ Hearts — People, relationships, emotions
- ♦️ Diamonds — Objects, tools, items (diamond emoji always red)
- ♣️ Clubs — Actions, movement, physical activities
- ♠️ Spades — Abstract concepts, history, mysteries

### Values
- 2–5: Small everyday details
- 6–10: More involved challenges or narrative beats
- J, Q, K: Important figures or game-changing interactions
- Aces: Major turning points

Cards are pacing mechanics and effort containers, not book content.

### Hand Structure
- 5 cards per hand (standard). 3 = small, 7 = deep.
- First 2 dealt face up. Next 3 face down (GM knows all 5).
- Player must engage with both face-up cards individually,
  then connect them before the next card flips.
- GM flips next card automatically when interaction requirements are met.
- Final card requires fluency-based challenge to win the hand.

---

## The Hand Review

Generated at the end of every hand. Saved as `.md` in `books/[name]/reviews/`.

Includes:
- Title, role, seniority, setting
- Cards played
- Vocabulary introduced
- Cultural moments
- Workplace moments
- Trust changes per NPC
- Scores (1–5): Language Accuracy, Vocabulary Recall,
  Cultural Awareness, Workplace Effectiveness, Role Alignment
- Strongest move
- One improvement
- Replay suggestion
- Continuity Notes (for next hand)

Reviews feed global tracking. Trends surface across hands.

---

## The "Recent Events" Layer

NPCs at lunch (and elsewhere) reference real-world news + office gossip.

### world/news_cache.json
Fetched via web search, timestamped.
Relevant to the book's city and domain.
Example: tech news for Tehran + AI product domain.

### world/office.json (or neighborhood.json)
Fictional internal events — gossip, rumors, project updates,
personnel changes. Persists across hands. NPCs remember.

Both layers are injected into the GM context at runtime
so NPCs can reference "what happened this week" naturally.

---

## Commands

```
/anthology init          ← reads dlc.md in cwd, prompts for language
                           and city, generates curriculum/, scaffolds
                           state/, initializes progress.json at intro

/process inbox           ← reads all unprocessed inbox/ files,
                           classifies, extracts, promotes to knowledge/

/hand                    ← start a new hand in the active book

/hand review             ← show the last hand review

/book [name]         ← switch active book

/crew                    ← list loaded crew members (if crew system active)

/directives              ← list available directives
```

---

## Runtime Philosophy

Do NOT load all knowledge simultaneously.
Prefer lightweight runtime composition.

At runtime, dynamically compose:
- relevant language knowledge (subset from global)
- relevant cultural knowledge (subset from global)
- relevant domain knowledge (subset from global)
- active book state
- curriculum stage (intro / midgame / endgame)
- recent events (news + office/neighborhood layer)

The GM prompt is reconstructed each session by injecting
relevant state — Claude Code always has full context
without relying on chat history.

---

## The SKILL.md

The skill file teaches Claude Code how to operate the wiki:
- how to process inbox items
- how to classify and promote knowledge
- how to run `/anthology init`
- how to construct the GM runtime prompt
- how to manage state across hands
- how to generate hand reviews

The SKILL.md lives at `skill/SKILL.md` inside the vault.

---

## The Karpathy LLM Wiki Model

This is the core philosophy behind how Anthology manages knowledge.
Understanding this is required before building anything.

Karpathy's insight with llm.c and his wiki work: you don't need a giant
monolithic system to understand something deeply. You build knowledge from
first principles, incrementally, annotated at every layer. Each piece
connects to others. Nothing is magic. Everything is traceable.

Applied to Anthology: the `knowledge/` folder IS the wiki. Not a static
encyclopedia — a living, annotated, cross-linked knowledge base that grows
every time the user runs `/process inbox`.

---

### Weights vs Context Window

This is the most important distinction in the system:

```
knowledge/              ← weights
                          durable, annotated, cross-linked
                          grows slowly, never expires
                          internalized cultural/linguistic truth

world/news_cache.json   ← context window
                          ephemeral, timestamped
                          expires and refreshes
                          injected at runtime, not stored as truth
```

Karpathy would recognize this immediately. `knowledge/` is what the model
has internalized. `world/news_cache.json` is what gets injected into the
context window at runtime.

`/process inbox` knows the difference and routes accordingly.
A durable cultural pattern → `knowledge/culture/`.
A news item → `world/news_cache.json`.
Never mix them.

---

### How It Works for Culture

Raw clip lands in `inbox/` via Obsidian:
> "10 words you need to survive an Iranian office"

`/process inbox` reads it and does NOT just extract the words. It asks:
- Is this language? culture? domain? some of each?
- What is the durable insight underneath the clickbait framing?
- Does this connect to anything already in `knowledge/culture/iranian-workplace.md`?
- Does it contradict or nuance anything already there?

It strips the clickbait and promotes something like:

```markdown
## Hospitality Refusal
In some Iranian workplace contexts, refusing chai a first time
is expected. Accepting immediately can read as overeager.
Source: inbox/iranian-office-words.md
Confidence: low (single source, popular press)
```

The `Source:` and `Confidence:` lines are the Karpathy move.
Every insight is traceable back to its origin.
The wiki doesn't just know things — it knows where it learned them
and how much weight to give them.

When a second source corroborates the same pattern, confidence rises.
When sources conflict, the wiki notes the conflict rather than picking a winner.

---

### How It Works for Current Events

Same inbox flow, different destination.

User clips a news article about a tech policy change in Iran.
`/process inbox` runs. But this is time-sensitive, not durable.
It goes to:

```
books/farsi-workplace/world/news_cache.json
```

At lunch, the NPC pulls from `news_cache.json` and mentions it offhand —
the way a colleague would, not as a news bulletin. Naturally, in context,
in Farsi at the appropriate fluency level.

News cache entries are timestamped. Stale entries are flagged or dropped.
The game stays current because the inbox stays active.

---

### Why Obsidian

Obsidian is the human interface to the wiki.

The user reads, clips, annotates, and drops material into `inbox/` using
Obsidian. It's fast, local, and matches how a person actually encounters
knowledge — reading an article, watching a talk, scrolling a thread.

The Anthology vault is dedicated entirely to this game. It is not the
user's general life vault. One vault, one purpose.

Obsidian surfaces `knowledge/` files as readable, linkable notes.
Claude Code operates underneath — processing, classifying, promoting,
and injecting knowledge at runtime.

The user never needs to manually edit `knowledge/` files.
They drop things in `inbox/`. The system does the rest.

---

### Why `/process inbox` Already Exists

`/process inbox` is already defined in this system.
It is not a future feature. Do not redefine it or duplicate it.

When building the `SKILL.md`, reference `/process inbox` as an
existing command. The skill teaches Claude Code how to execute it —
read unprocessed inbox files, classify across the three pillars,
extract durable insights, route to the correct destination
(knowledge/ or world/), annotate with source and confidence,
mark as processed.

---

### The Full Knowledge Flow

```
User reads something interesting
  ↓
Clips it into Anthology/inbox/ via Obsidian
  ↓
/process inbox
  ↓
Claude Code classifies: language / culture / domain / news
  ↓
Durable insight → knowledge/[pillar]/[file].md
  annotated with source + confidence
  cross-linked to related entries
  flagged if relevant to active book curriculum

Time-sensitive → books/[name]/world/news_cache.json
  timestamped
  expires
  injected at runtime during NPC interactions
  ↓
Player runs /hand
  ↓
GM runtime composes:
  relevant knowledge/ excerpts (the weights)
  + news_cache.json (the context window)
  + state/ (deck, npcs, progress, session)
  + curriculum stage (intro/midgame/endgame)
  ↓
NPC at lunch mentions something from the news naturally
Cultural moment surfaces because knowledge/ has the grounding
Vocabulary appears because curriculum says it's time
```

The game gets richer every time the inbox is processed.
The knowledge base compounds. The NPCs get smarter.
The cultural moments get more specific and accurate.

This is the Karpathy principle: build from first principles,
annotate everything, make it composable, make it traceable.

---

## What To Build (In Order)

1. `skill/SKILL.md` — the wiki operator
2. `books/farsi-workplace/dlc.md` — updated with Runtime Config block and Curriculum Seeds
3. `/anthology init` — reads dlc.md, prompts language + city, generates curriculum/, scaffolds state/
4. `/process inbox` — inbox processor
5. `/hand` — GM runtime, card engine, NPC interaction, hand review generator
6. `books/costa-rican-longstay/dlc.md` — second book, stress-tests the architecture

Do not merge these. Build them in order. Each one depends on the previous.

---

## Key Design Principles

- Curriculum is stable. State is runtime. Never mix them.
- Global knowledge is the library. Book vocabulary is the active reading list.
- The DLC is config AND seed. Few-shots in it are instructions, not documentation.
- City is a first-class variable. It colors dialect, culture, NPCs, and news.
- Books are siloed. They share knowledge/ but do not bleed into each other.
- The inbox is the growth engine. The game gets richer as you clip more.
- The GM prompt is composed dynamically. Never monolithic.
- Avoid stereotypes in all cultural knowledge. Prefer patterns and tendencies over rules.

---

## Source Files

- `Anthology__A_Solitaire_World_Prompt.pdf` — base game master prompt
- `anthology_dlc_farsi_workplace.md` — current DLC (needs Runtime Config + Curriculum Seeds added)
- This document — architecture and build instructions

