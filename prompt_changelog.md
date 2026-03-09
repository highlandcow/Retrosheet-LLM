# Retrosheet Pitch Sequence Prompt — Changelog

*A record of changes to the prompt, including the specific cases that drove each change.*

---

## Initial rules
Baseline prompt created. Included pitch code reference table, core rules for count tracking, count confirmation anchoring, use of U for uncertain pitches, play result as anchor, stolen base/pickoff handling, and output format with confidence levels.

---

## Distinguishing S, C, and K on strikeouts
Driven by: General domain knowledge discussion, not a specific error case.
Details: Added hierarchy for determining final pitch on strikeouts — "swing and a miss" = `S`, "caught looking" = `C`, ambiguous "strike three" defaults to `S`, genuine uncertainty = `K`. `K` designated as last resort only.

---

## Bunt attempts require extra care
Driven by: NYA197409250 — `play,1,1,whitr101`
Details: Whisper transcribed "bunts at it and misses" as "busts at it and misses", causing a missed bunt attempt (`M`) to be coded as a swinging strike (`S`). Rule added to flag words like "busts", "punts" as potential bunt mishearings and to cover `M`, `L`, and `O` codes.

---

## Count field for mid-AB events
Driven by: NYA197409250 — `play,1,0,evand002` (SB2)
Details: Count field should reflect the count at the moment the stolen base occurs, not at the end of the at-bat. In this case the count was `01` at the time of the stolen base even though the at-bat continued afterward.

---

## Pickoff throws vs. looks
Driven by: NYA197409250 — `play,2,1,munst101`
Details: Two pickoff throws to first base (`1`) were missed, resulting in `BBX` instead of `1B1BX`. Rule added to distinguish actual throws ("threw over", "dives back", "close play") from mere looks ("looked over", "checked the runner", "went back") which are not recorded. Ambiguous cases flagged for audio verification.