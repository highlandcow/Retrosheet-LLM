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

## Count confirmations as hard constraints
Driven by: NYA197409250 — `play,3,0,yastc101` (CS2)
Details: A garbled transcript line at `[30:54]` ("Off the feed, Mettish is over, strikes two balls") was ambiguous — could have been a ball or a strike. The original rule only used count confirmations reactively to verify sequences already built. The stronger approach is to scan the full at-bat transcript for count confirmations **before** building the sequence, and use them as hard constraints. In this case "0-2" at `[31:41]` would have immediately ruled out any ball being thrown before that point, regardless of the garbled line.

---

## Count field for multi-play plate appearances
Driven by: NYA197409250 — `play,3,0,yastc101` (CS2) and `play,3,0,yastc101` (7/F7)
Details: A plate appearance spanning two play records — a CS mid at-bat followed by the batter completing his at-bat — revealed that each play's count field reflects the count at the moment that specific event occurred. The CS play count was `22` (the count when the runner acted), even though the sequence included a third ball thrown before the runner was retired. The subsequent flyout play inherited count `32` from where the at-bat stood after the CS play concluded.

---

## Retrospective pitch clarifications
Driven by: NYA197409250 — `play,3,0,yastc101` (CS2)
Details: The final pitch was coded as `P` (pitchout) based on the announcer's description during the play. However, immediately after the caught stealing the announcer clarified "that pitch was outside — had the same effect of a pitchout, really", confirming it was a ball (`B`) not a pitchout. Rule added to scan subsequent commentary for any retrospective descriptions that clarify or correct any pitch in the at-bat, not just the final one.

---

## Catcher pickoff throws and lineup cross-reference
Driven by: NYA197409250 — `play,3,1,masoj101`
Details: Pickoff throws by the catcher are coded differently from pitcher pickoffs — they use a `+` prefix (e.g. `+1` for catcher throw to first). The transcript named Bob Montgomery as the thrower; cross-referencing the event file's `start` rows confirmed he is the catcher (position `2`). Rule added to use the lineup to identify the catcher and to note that Whisper may miscount repeated actions like pickoff throws.

---

## Two-stream approach for at-bats with baserunners
Driven by: NYA197409250 — `play,3,0,yastc101` (CS2)
Details: A complex at-bat with multiple pickoff throws, balls, and runner commentary interleaved caused several pitch calls and pickoff throws to be missed. The fix is to separately identify pitch events and baserunner events before combining them. This prevents runner commentary from obscuring pitch calls and vice versa.

Updated: NYA197409250 — `play,4,1,murcb101` (16(1)3/GDP)
Details: Both streams were correctly identified but merged in the wrong order, producing `B1CF1FX` instead of `BC1F1X`. The timestamps were present in the working but not used strictly when recombining. Rule strengthened to require recombination strictly by timestamp, returning to the transcript to confirm each event's position before placing it in the sequence.

⚠️ **Note to revisit:** The two-stream approach may be causing more problems than it solves — the extra cognitive step of separating and recombining streams introduces a new failure mode (incorrect merging) on top of the original problem it was meant to fix. Worth evaluating after more innings whether a simpler rule (e.g. "process strictly by timestamp, tagging each event as pitch or baserunner as you go") performs better.

---

## Pickoff throws vs. looks
Driven by: NYA197409250 — `play,2,1,munst101`
Details: Two pickoff throws to first base (`1`) were missed, resulting in `BBX` instead of `1B1BX`. Rule added to distinguish actual throws ("threw over", "dives back", "close play") from mere looks ("looked over", "checked the runner", "went back") which are not recorded. Ambiguous cases flagged for audio verification.

---

## Garbled count calls — phonetic recognition
Driven by: NYA197409250 — `play,9,1,chamc001` ([127:23] "side ball on" = "ball one")
Details: Whisper frequently mishears count calls in recognizable ways — "ball one" becomes "side ball on", "strike one" becomes "straight one", etc. A line immediately following a pitch delivery that sounds phonetically like a count call should be treated as both a pitch and a count confirmation, not discarded as unintelligible. Added to rule 2.

---

## Runner going on pitch (>) — optional enrichment
Driven by: CHN197409270 — `play,5,0,sizet101` — Brock clearly breaking for second on first pitch of Sizemore's walk
Details: When the transcript unambiguously describes a runner breaking for the next base on a specific pitch (typically a hit and run), prefix that pitch with `>`. Do not use when the movement results in a separate SB or CS row. Multiple `>` can appear in a sequence but never consecutively. Omit when in doubt — this is a nice-to-have enrichment and errors are worse than omissions.

---

## Wrap-up section added
Driven by: NYA197409250 — completion of first fully validated game
Details: Added a wrap-up section to the prompt covering the final step of updating `info,pitches,none` to `info,pitches,pitches` once sequences are complete. A count field sanity check script also exists (derived from human reviewer's Python script) and is a candidate for future integration — either as a checker agent or embedded logic in the prompt.

---

## Pickoff throws require explicit throw description
Driven by: NYA197409250 — `play,10,0,mcaud101` — fielder movement toward base misread as pickoff throws
Details: Before recording a pickoff throw, the transcript must explicitly describe the ball leaving the pitcher's or catcher's hand. Words like "threw over", "fires to", "throws down to" are required. Fielder movement toward a base or a runner retreating are not sufficient — these describe positioning or bluffs. The existing "only actual throws are recorded" principle was not specific enough; this reframes it as a positive check.

---

## Wild pitches and passed balls split plate appearances like SB/CS
Driven by: NYA197409250 — `play,10,0,mcaud101` — wild pitch splits PA, count field was 20 instead of correct 10
Details: Wild pitches and passed balls follow the same pattern as stolen bases and caught stealings. The count field on the WP/PB play row reflects the count before the pitch that caused the event was thrown, not after. The subsequent play row for the same batter inherits the full sequence and continues from there.

---

## Garbled count calls should not be discarded
Driven by: NYA197409250 — `play,9,1,chamc001` — "side ball on" miscoded as commentary rather than "ball one"
Details: Whisper frequently mishears count calls. "Ball one" may appear as "side ball on", "ball on", or similar; "strike one/two/three" may appear as "straight one", "strike line", etc. A line immediately following a pitch delivery that resembles a count call should be treated as both a pitch and a count confirmation, not discarded.

---

## Fouls are never S
Driven by: NYA197409250 — `play,9,1,nettg001` — "swing and a foul back" miscoded as S instead of F
Details: `S` is strictly for swings with no contact. Any swing that makes contact is `F` (foul not caught), `T` (foul tip caught by catcher), or `X` (ball in play). The word "swing" in an announcer's call does not mean `S` if contact was made.

---

## Never skip rows
Driven by: NYA197409250 — `play,9,1,pinil001` (three NP rows before PA)
Details: When multiple substitutions occur before or during a plate appearance, there may be several `play` rows for the same batter. Every row must appear in the output — do not collapse, skip, or omit any. The correct count and sequence for each row follows from the existing substitution rules.

---

## Hitter substitutions / defensive substitutions — never delete sub rows
Driven by: NYA197409250 — `play,8,1,masoj101` / `play,8,1,johna104`, `play,9,0,grifd101` / `play,9,0,coopc001`, and `play,9,0,burlr001` / `sub,stanf101` / `play,9,0,burlr001`
Details: When any substitution occurs mid-plate appearance — whether offensive (pinch hitter, position code 11) or defensive (new fielder, position codes 2-9) — the event file contains a `sub` row between two `play` rows for the same batter. The original batter's first row gets the count and sequence up to that point (or `00` and empty sequence if no pitches thrown), and the batter's second row continues from there. Defensive substitutions are easy to miss in the transcript — look for announcer mentions of a new fielder entering the game. Critical rule: never delete or skip a `sub` row from the event file under any circumstances.

---

## Experiments

### Real-time reasoning log
Driven by: NYA197409250 — human-in-the-loop review session
Details: During validation of `play,4,1,chamc001`, it became clear that retrospective explanations of errors were unreliable — the LLM was reconstructing plausible-sounding reasoning after the fact rather than reporting what actually happened. An attempt was made to produce a full-game reasoning log (START/UPDATED format with timestamp-by-timestamp working) as a diagnostic tool for identifying where sequences go wrong. After building the log it became clear the output was still an executive summary rather than genuine real-time reasoning, and that enforcing a more structured format risked interfering with the natural working process. Experiment abandoned. The value of human-in-the-loop review is that the human can identify errors directly from the sequence and count; the LLM does not need to fully narrate its process for that to work.
