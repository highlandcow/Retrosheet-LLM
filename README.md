# Retrosheet Pitch Sequence Enrichment

## Retrosheet-LLM

Teaching Claude to be a good Retrosheet volunteer.

[Retrosheet](https://www.retrosheet.org) is a volunteer organization that has digitized play-by-play records of major league baseball games going back to the 1800s. Their event files describe every play in a game in a structured CSV format. One field in those records — the pitch sequence — is often missing for older games, as it was not consistently recorded.

This project uses AI to recover pitch sequences from old radio broadcast recordings and use them to enrich Retrosheet event files. The workflow is:

1. A radio broadcast MP3 is transcribed using [OpenAI Whisper](https://github.com/openai/whisper)
2. The transcript is fed to an LLM alongside the Retrosheet event file
3. The LLM matches each at-bat in the transcript to its corresponding event file row and fills in the pitch sequence
4. A human reviewer validates the LLM's output against the audio, correcting errors and flagging problem cases

This is a **human-in-the-loop** process — the LLM handles the bulk of the work but human review is essential, particularly for cases where crowd noise, audio dropout, or Whisper mishearings obscure pitch calls.

---

## Files

### `baseball_transcription_pipeline.ipynb`
A Google Colab notebook that handles the transcription pipeline. Given an MP3 of a broadcast, it preprocesses the audio (upsampling, bandpass filtering, FFT denoising, EQ boost, and loudness normalization), splits it into 30-minute chunks, transcribes each chunk using Whisper `large-v3` with optimized parameters to fine-tune performance for low quality audio, and merges the results into a single consolidated transcript with continuous timestamps. Designed to be reusable across any game — only the configuration cell needs to be edited.

### `retrosheet_pitch_sequence_prompt.md`
The prompt used to instruct the LLM to extract pitch sequences from the transcript and enrich the Retrosheet event file. Covers Retrosheet pitch codes, count derivation, handling of edge cases (bunts, pickoffs, stolen bases, audio dropouts), and output format with confidence levels. This is a living document — refined iteratively through human-in-the-loop validation.

### `prompt_changelog.md`
A record of every change made to the prompt, including the specific game and play that drove each change. Useful for understanding why each rule exists and tracing it back to a real example.

### `problematic_events_log.md`
A log of cases where the LLM's proposed pitch sequence could not be resolved from the transcript alone and required audio verification. Ordered by game ID and inning. Useful for identifying recurring failure patterns and informing future prompt improvements.

---

## Future Goals

The ultimate goal of this project is for an LLM to generate complete Retrosheet event files from scratch given only a broadcast transcript — covering not just pitch sequences but all structured data in the event file format, including hit locations, weather conditions, and other game metadata.

The current prompt is intentionally narrow in scope. It focuses on pitch sequences as a way to rigorously inspect and improve the LLM's performance on one well-defined task before expanding to others. The human-in-the-loop validation process, the problematic events log, and the prompt changelog are all designed to build confidence in the LLM's output incrementally.

As accuracy on pitch sequences improves, the project can expand to other enrichment tasks, for example:
- **Hit locations** — trajectory and fielder codes (e.g. `/F7D`, `/G6M`)
- **Weather and conditions** — temperature, wind, sky from broadcast commentary

Each of these will likely follow the same pattern: a focused prompt, human-in-the-loop validation, and iterative refinement.

### Transcript quality improvements
A recurring theme in the problematic events log is that many sequence errors are not LLM errors at all — they originate in the transcript. We have identified several distinct failure modes so far:

- **Brief crowd noise surges** — Whisper misses pitch calls immediately after an exciting moment when the crowd drowns out the announcer
- **Station ID corruption** — plays immediately before or after a station ID announcement are at elevated risk of transcription degradation
- **Prolonged crowd noise re-entry** — after a long stretch of crowd noise with no commentary, Whisper's voice activity detection fails to re-engage promptly, missing the announcer's re-entry point
- **Miscounted repeated actions** — Whisper sometimes mishears the number of repeated events (e.g. "two throws" transcribed as "three throws")

A systematic effort to improve transcript quality would reduce the number of plays that require audio verification. Avenues worth exploring:

- **✅ Whisper parameter tuning** — `condition_on_previous_text=False` and `temperature=0` implemented in pipeline Step 7.
- **✅ Audio pre-processing** — pipeline Step 5 implements a full ffmpeg preprocessing chain: upsampling to 16 kHz, bandpass filtering (300–3000 Hz), FFT denoising, speech EQ boost, loudness normalization, and dynamic range compression. Implemented with a `SKIP_PREPROCESSING` flag to allow easy comparison with and without enhancement.
- **Alternative ASR systems** — other speech recognition models may handle sports broadcast audio better than Whisper, particularly around crowd noise
- **Post-processing heuristics** — automated flagging of transcript segments that match known failure patterns (e.g. long stretches of dots, single isolated words, lines immediately adjacent to station ID text)

### Hit quality and exceptional play notation
Retrosheet play results support several optional notations that can be extracted from broadcast commentary when clearly evident:
- `!` — exceptional play
- `?` — uncertainty in the play
- `+` — hard hit ball
- `-` — softly hit ball

For example, `play,2,0,mendm101,10,BX,53/G5-` captures that Mendoza's grounder to third was weakly hit ("grounds weakly to third base"). This is a minor embellishment to be added opportunistically after hit location enrichment is more fully developed, as hit location (`/G5`, `/F7`, etc.) is the higher-value addition. Both draw on the same broadcast commentary and will likely be tackled together.

### Resolving stolen base uncertainty (#)
Retrosheet events marked `SB2#` indicate the original scorer was uncertain when exactly the steal occurred, typically because the game was digitized from a scorebook rather than play-by-play. With broadcast audio, the steal can often be located precisely and the `#` row corrected. A clear teaching example with documented methodology is needed before this becomes a standard prompt step.

### Reviewer agent
Human-in-the-loop validation has proven effective at catching LLM errors in pitch sequences, but doesn't scale. A promising future direction is a separate reviewer agent that replicates the human review process — given the transcript and the LLM's proposed sequences, it independently verifies each sequence against the transcript and flags discrepancies. The key insight is that a separate agent avoids the anchoring bias of self-review: an agent that did not produce the sequences is more likely to challenge them. This mirrors how the human-in-the-loop process currently works, with the human as a skeptical second reader rather than a confirmer.

A concrete example of where this would help: in NYN197409270, `play,3,0,stenr101` was incorrectly coded as `01,CX,S7` when the correct sequence is `00,X,S7`. The LLM attributed a called strike to Stennett's at-bat based on a misremembered transcript line — "strike one on Manning" at [33:26] actually belongs to Sanguillen's subsequent at-bat. A reviewer agent reading the transcript fresh for that play would immediately see that no pitch is described before the hit and flag the discrepancy. The LLM's own notes, taken during an earlier pass, led it astray — the reviewer agent has no such baggage.

A related improvement would be to integrate the count field sanity check (`check_count.py`) into this reviewer pipeline — automatically flagging any play row where the derived count does not match the count field before human or agent review begins.

---

## Example: How sequences are built

The following is a worked example of the sequence-building process for a single at-bat — `play,10,0,evand002` from NYA197409250 (top of the 10th inning, Dwight Evans batting, one out, nobody on).

**Event file row:**
```
play,10,0,evand002,??,,K
```

**Relevant transcript excerpt:**
```
[132:58.92]  He fouls one back, and that'll be out of play.
[133:07.50]  The ball's in the strike.
[133:10.46]  Evans has walked by, singled, and sacrificed.
[133:22.48]  Has a fastball low.
[133:24.16]  Evans ran up in front of the plate and took it.
[133:26.42]  One ball and one strike.
[133:38.20]  The doctor kicks the deal.
[133:39.66]  The pitch is in for a call.
[133:40.84]  Drag it at one and two.
[134:03.60]  Pitch is fouled.
[134:04.52]  Straight back by Evans.
[134:25.02]  And it's one-two pitch.
[134:26.96]  Not on reserve, but low to a two.
[134:48.64]  And here's the two-two.
[134:51.28]  Swing and a miss.
[134:52.42]  And Doc Bennett picks up his sixth strikeout.
```

**Step 1 — Scan for all count confirmations before building:**
- "one ball and one strike" at [133:26] → 1-1
- "one and two" at [133:40] → 1-2
- "two-two" at [134:48] → 2-2

**Step 2 — Build sequence pitch by pitch:**
- [132:58] "he fouls one back" = F (count 0-1)
- [133:07] "the ball's in the strike" — Whisper garble for "ball one" = B (count 1-1)
- Count confirmation: [133:26] "one ball and one strike" ✅
- [133:39] "the pitch is in for a call" = C (count 1-2)
- Count confirmation: [133:40] "one and two" ✅
- [134:03] "pitch is fouled straight back by Evans" = F (count 1-2)
- [134:25] "one-two pitch, not on reserve but low" — another pitch = B (count 2-2)
- Count confirmation: [134:48] "two-two" ✅
- [134:51] "swing and a miss" = S (strikeout)

**Step 3 — Pitch count self-check:**
F, B, C, F, B, S = 6 distinct pitch events. Sequence `FBCFBS` = 6 pitches ✅. Count 22: 2 balls (B+B), 2 strikes (F+C — fouls only count as strikes until two strikes) ✅. Final S consistent with strikeout ✅.

**Output:**
```
play,10,0,evand002,22,FBCFBS,K
```

