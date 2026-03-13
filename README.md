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
A Google Colab notebook that handles the transcription pipeline. Given an MP3 of a broadcast, it splits the file into 30-minute chunks, transcribes each chunk using Whisper `large-v3`, and merges the results into a single consolidated transcript with continuous timestamps. Designed to be reusable across any game — only the configuration cell needs to be edited.

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

- **Whisper parameter tuning** — `condition_on_previous_text=False`, `temperature=0`, `no_speech_threshold` adjustment to improve handling of noise/speech transitions
- **Audio pre-processing** — noise reduction and normalization before transcription, particularly targeting crowd noise frequencies
- **Alternative ASR systems** — other speech recognition models may handle sports broadcast audio better than Whisper, particularly around crowd noise
- **Post-processing heuristics** — automated flagging of transcript segments that match known failure patterns (e.g. long stretches of dots, single isolated words, lines immediately adjacent to station ID text)

### Reviewer agent
Human-in-the-loop validation has proven effective at catching LLM errors in pitch sequences, but doesn't scale. A promising future direction is a separate reviewer agent that replicates the human review process — given the transcript and the LLM's proposed sequences, it independently verifies each sequence against the transcript and flags discrepancies. The key insight is that a separate agent avoids the anchoring bias of self-review: an agent that did not produce the sequences is more likely to challenge them. This mirrors how the human-in-the-loop process currently works, with the human as a skeptical second reader rather than a confirmer.

