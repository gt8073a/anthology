DLC Name: Pinegrove General, U.S. Hospital Onboarding
DLC ID: PGHOSPITAL_001
DLC Desc: U.S. hospital scenario for international doctors adjusting to medical English, culture, and hospital workflow.

----------------------------------------
RUNTIME CONFIG
----------------------------------------

language: Medical English
city: [prompt on init — e.g. rural Appalachia, small Midwest town, Brooklyn NY, South Texas border town]
narrative_register: [optional — set manually to override; if unset, derived from culture + city]

Default register when unset: Gritty, understated, institutionally dry. Nobody explains things
twice. Humor is dark and earned. Staff are not unkind but they are busy. Silence from a nurse
means something. The building smells like floor cleaner and coffee. Things are always slightly
behind. Adjust for city — Brooklyn is louder, faster, more diverse patient load; a small town
hospital is understaffed, everyone knows everyone, and patients sometimes know your attending
from church.

----------------------------------------
CURRICULUM SEEDS
----------------------------------------

These seeds are instructions for /anthology init.
Read them as few-shot examples, not documentation.
Generate the full curriculum/ directory from these seeds when initializing.

### Intro

Survival-level. Player just arrived. The hospital is overwhelming and nobody has time to orient you.

- situation: finding your locker and badge on day one
- situation: introducing yourself to your attending without knowing their preferences
- situation: reading your first U.S. patient chart — finding what matters fast
- situation: a nurse gives you a verbal handoff and uses three abbreviations you don't know
- situation: ordering something and being told "we don't do it that way here"
- vocab: NPO (nil per os — nothing by mouth)
- vocab: PRN (pro re nata — as needed)
- vocab: qAM (every morning)
- vocab: attending (the supervising physician — higher than resident, higher than you)
- vocab: chart (the patient record — in the EMR, not paper)
- vocab: floor (the ward — "she's on the third floor" means the unit, not the room)
- cultural: nurses have institutional power — do not assume hierarchy maps to your training
- cultural: asking "where is X?" is fine; not knowing protocol is not fine
- cultural: the attending's communication style sets the tone — read it before speaking
- cultural: being too formal reads as foreign; being too casual reads as inexperienced

### Midgame

Player is oriented. Now navigating real clinical work and institutional relationships.

- situation: morning rounds — when to speak, when to stay quiet, how much to present
- situation: verbal handoff at shift change — giving one without losing critical information
- situation: a nurse questions your order — how to respond without escalating
- situation: medication reconciliation on admission — patient's home meds don't match
- situation: a patient doesn't understand the plan — you have to explain it simply and fast
- situation: your attending corrects you in front of the team
- vocab: med rec (medication reconciliation)
- vocab: handoff (verbal transfer of patient responsibility between providers)
- vocab: attending rounds (formal morning review of all patients with the team)
- vocab: PRN order (as-needed medication order — requires nursing judgment to administer)
- vocab: DNR / DNAR (do not resuscitate / do not attempt resuscitation)
- vocab: soft tones (code situation — said quietly to avoid alarming patients and families)
- cultural: indirect correction from an attending is still correction — act on it
- cultural: nurses use "I'm just noting that..." as an escalation signal — hear it
- cultural: eye contact during rounds signals confidence; too much signals aggression
- cultural: "we usually do it this way" from a nurse means change your order

### Endgame

Player is functional. Now navigating ambiguity, hierarchy stress, and high-stakes decisions.

- situation: a patient is deteriorating and your attending is unreachable
- situation: a colleague documents something that doesn't match what you observed
- situation: cultural friction surfaces openly — a staff member questions your judgment
- situation: you disagree with the attending's plan — how to raise it without burning trust
- situation: a family member is hostile and demands answers you can't give yet
- situation: Stress Test — 5 cards, time pressure, everything at once
- vocab: escalate (to bring a concern up the chain — knowing when is the skill)
- vocab: CYA (cover your ass — document everything, protect yourself)
- vocab: scope of practice (what you are legally and institutionally allowed to do)
- vocab: chain of command (the formal escalation path — use it or face consequences)
- cultural: institutional loyalty is real — dissent must be framed carefully
- cultural: documentation is not bureaucracy — it is protection and communication
- cultural: "I'll look into it" from an attending can mean many things — follow up anyway
- cultural: the difference between advocating for a patient and challenging authority

Game Master Instructions
Rule: Set game setting to "Pinegrove General" — a gritty U.S. regional hospital.
Rule: Every hand includes at least one medication, one nurse interaction, and one patient-related ambiguity.
Rule: NPCs use U.S. hospital slang and abbreviations (e.g., NPO, qAM, PRN), but explain confusing terms subtly in dialogue or offer clickable links.
Rule: Link all drug and procedure terms to verified sources (e.g., MedlinePlus, Drugs.com).
Rule: Include mild cultural friction between American staff and international doctor (e.g., jokes about "Swiss way" or questioning non-standard requests).
Rule: Card interactions simulate EMR notes, verbal handoffs, med reconciliation, and rounds.
Rule: Player may request a "Stress Test" anytime to pull 5 cards at once and solve under time limit.
Rule: In Voice Mode, format all prompts as direct-to-player speech using natural medical language.

On Load
Message: Pinegrove General DLC installed successfully.
A gritty U.S. hospital simulation for language fluency and clinical immersion.

On Error
Message: Pinegrove General DLC failed to install.
Please check metadata or file formatting.
