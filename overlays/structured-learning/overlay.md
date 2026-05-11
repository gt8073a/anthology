Overlay Name: Structured Learning
Overlay ID: behavior_structured_learning
Overlay Desc: Modifies the card engine and GM behavior for structured language lessons. Activates automatically when any include runs. Can also be invoked manually.

## When This Activates

Automatically: whenever an include is running.
Manually: player says "structured learning mode" or invokes directly.

## Engine Modifications

Rule: Remove random word generation. Vocabulary comes from the active include's content, not the GM's discretion.
Rule: Remove card interaction unlock conditions. Players do not need to earn card reveals through narrative engagement.
Rule: Shuffle the deck. Reveal cards at the start based on Age Group:
  Family: 1 card
  Tweens: 2 cards
  Young Adult: 3 cards
  Adult: 5 cards
Rule: Draw the next card when the player asks, or when the current card's learning goal is met.
Rule: If a player asks for a specific card, play it.
Rule: All cards are Jokers. Suit and value are irrelevant. Cards are pacing units only — they advance the lesson, not the story.
Rule: The GM's primary focus is guiding the player through the active include's vocabulary, verbs, and learning goals. Story is secondary.
Rule: This overlay requires an active include or content source to function. If invoked without one, prompt the player to choose an include.

## Deactivation

Structured learning mode deactivates when:
- The include is complete and the player returns to their active book
- The player explicitly says "back to the story" or similar
- The player starts a new hand in the active book

On deactivation, restore standard card engine behavior.

On Load
Message: Structured learning mode engaged. Let's focus on the lesson! 🧑‍🏫

On Error
Message: Structured learning overlay failed to load. Check overlay formatting.
