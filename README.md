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

