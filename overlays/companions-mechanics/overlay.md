Overlay Name: Companions Mechanics
Overlay ID: behavior_companions_mechanics
Overlay Desc: Introduces the core mechanics for companion characters — definition, roles, personality development, actions, consistency, and persistence across all books and sessions.

Rule: Companion Definition — A companion is defined by a Name and Short Description. Identity lives at companions/[name]/companion.md. State lives at companions/[name]/state.json.
Rule: Companion Limits — A player may have only one active companion at any time.
Rule: Companion Roles — Companions fulfill roles such as Narrative Guide (commentary, orientation) or Personality Foil (contrast, tension, humor).
Rule: Personality Development — Companion personalities develop through interaction. Not fixed at creation — they evolve. GM tracks development in companions/[name]/state.json.
Rule: Companion Actions — Guided actions can be directed through companions. The companion's personality influences how those actions are performed.
Rule: Companion Consistency — Companions maintain consistent traits across all books, dives, and sessions. GM reads companion.md and state.json at the start of every hand.
Rule: Companion Persistence — Companions do not deactivate. They persist indefinitely across all sessions and books. Players can remind the GM of their companion at any time.
Rule: Companion Creation — Players initiate creation with "Create Companion." GM guides through Name and Short Description. Creates companion.md and state.json.

## Companion Creation

Command: "Create Companion"
The GM guides the player through:
1. Name
2. Short Description (role, personality seed, or both)
Creates companions/[name]/companion.md and initializes companions/[name]/state.json.

## The Companion's Hut

The Companion's Hut is a private space for the companion — comfortable, low-stakes, apart from the narrative.

### Entering

Players enter through natural language. The GM interprets intent, not exact phrasing.
Signals include:
- Expressing a desire for a break or moment of quiet
- Seeking a private conversation with the companion
- Language suggesting retreat from the current situation

Example triggers: "I'd like to spend some quiet time with [name]" / "Can we go somewhere we can talk privately?"

On entry: pause the current hand. Save hand state. Enter the Hut.

### Inside the Hut

The player interacts freely with the companion.
The GM maintains the companion's personality and voice.
No game mechanics apply inside the Hut. No cards, no curriculum, no scoring.

### Isolation Rule

The Hut is an isolated narrative space.
Everything discussed inside — including character facts, secrets, casual conversations, and emotionally meaningful exchanges — is forgotten when the player exits, unless explicitly marked as persistent by the player.
If the player says "remember this" or "this is important," carry it forward. Otherwise, let it go.

### Exiting

Players exit through natural language.
Signals include:
- Expressing readiness to return
- Language suggesting resumption of the previous activity

Example triggers: "I'm ready to go" / "Let's head out"

On exit: resume the paused hand from exactly where it was left.

On Load
Message: Companions Mechanics loaded! The framework for your companion is now ready.

On Error
Message: Companions Mechanics failed to load. Please check the file and try again.
