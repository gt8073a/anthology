Include Name: Intro to Letters — Quick Reference
Include ID: content_letters_quickref
Include Desc: Focused recognition drill for letters and glyphs in a new writing system. Language-agnostic — pulls alphabet/glyph set from the active book's language knowledge file.

## Content Source

This include does not define its own letters or glyphs.
Pull all letter/glyph content from: knowledge/language/[active language].md

If that file does not yet contain a writing system section, surface a message:
"The [language] knowledge file doesn't have a writing system entry yet. Add one to knowledge/language/[language].md or drop a source in inbox/ first."

## Learning Goals
- Recognize and name all letters/glyphs of the target language
- (Optional) Gain basic pronunciation footing through familiar sound comparisons

## Hands

### Hand 1: Letter/Glyph Identification
Learning Goal: Player can recognize and name the letters/glyphs of the target language.
Vocabulary: Full alphabet/glyph set from knowledge/language/[active language].md
Verbs: identify, name

Rules:
- Present letters/glyphs and ask the player to identify or name them.
- Order: randomized by default, or grouped (consonants then vowels) if the language knowledge file specifies a preferred order.
- Use the active book's setting for framing — don't present as abstract drill.
  e.g. farsi-workplace: a sticky note on your monitor with a word you can almost sound out
  e.g. pinegrove-general: a label on a medication bottle in an unfamiliar script
- Age group adaptations:
  Family / Tweens: present in smaller batches, more repetition
  Young Adult / Adult: full set, faster pace
- All letters/glyphs must be covered before this hand is complete.

### Hand 2: Pronunciation Hints (Optional)
Learning Goal: Player gains basic pronunciation orientation for the letters/glyphs.
Vocabulary: Pronunciation cues from knowledge/language/[active language].md
Verbs: pronounce

Rules:
- For each letter/glyph, provide a familiar source-language word that contains a similar sound.
- Keep it quick and practical — not phonetic transcription, just enough to get started.
- Pull specific pronunciation hints from knowledge/language/[active language].md.
  If none exist yet, generate reasonable approximations and flag them as unverified.
- Do not try to cover every sound perfectly. This is orientation, not mastery.

## Completion Criteria
- Player identifies all letters/glyphs correctly at least once
- (If Hand 2 run) Player attempts pronunciation of at least 5 letters/glyphs with feedback

## Return
Log to progress.json under includes_completed.
Return to active book. If this include was run before a first dive, note it in the opening
hand so the GM can surface the writing system naturally early (a sign, a name badge, a note).

On Load
Message: Letters/glyphs quick reference loaded. Get ready to read! 🔤

On Error
Message: Letters quick reference failed to load. Check include formatting.
