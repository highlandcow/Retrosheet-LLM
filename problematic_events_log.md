# Retrosheet Pitch Sequence — Problematic Events Log

*A running log of cases where LLM-proposed pitch sequences were incorrect, ordered by game ID and inning.*

---

## NYA197409250 — Red Sox at Yankees, September 25, 1974

### play,2,0,burlr001 — Inning 2, Top

**Full play:** `play,2,0,burlr001,22,CBBCFFX,6/L6M`
**LLM proposed:** `CBBCFFFX`
**Error:** One extra foul — `CFFFX` vs `CFFX`

**LLM reasoning as presented:**
- [1152.9] "on the outside corner strike one" = `C`
- [1168.7] "low and outside, one ball one strike" = `B`
- [1181.7] "low and away again" = `B`
- [1200.3] "fastball is in for a called strike" = `C`
- [1210.3] "foul" = `F` ← **spurious**
- [1214.7] "fastball foul" = `F`
- [1241.8] "fastball fouled back again" = `F`
- [1266.1] "breaking ball is lined up the middle...Mason's got it" = `X`

**Source of error:** Transcript line `[1210.3 --> 1210.4] Foul.` — a single isolated word with no surrounding announcer commentary, likely Whisper misinterpreting crowd noise as a pitch call.

**Note:** No reliable way to detect this from the transcript alone. Count confirmation cannot catch spurious fouls at 2-2 since consecutive fouls don't change the count with two strikes. Requires audio verification.

---

### play,2,0,grifd101 — Inning 2, Top

**Full play:** `play,2,0,grifd101,12,BFFT,K`
**LLM proposed:** `BFF?`
**Error:** Missing final pitch `T` (foul tip) — sequence incomplete

**LLM reasoning as presented:**
- [1300.6] "Medich comes in low with a fastball" = `B`
- [1312.7] "he fouls it back on the right side" = `F`
- [1329.2] "next pitch, foul back" = `F`
- Long gap of `...` in transcript — audio dropout

**Source of error:** Extended crowd noise after the second foul ball caused Whisper to output `...` rather than transcribing the announcer's call of the foul tip. The pitch is audible in the audio but completely absent from the transcript.

**Note:** Crowd noise following exciting moments (big foul tips, close plays) is a recurring risk point in 1970s broadcasts. Pitches occurring in or immediately after crowd noise surges are likely to be missing from the transcript and require audio verification.

---

### play,3,1,masoj101 — Inning 3, Bottom

**Full play:** `play,3,1,masoj101,??,BC+B+X,7/F7`
**LLM proposed:** `B111X`
**Errors:** Multiple

1. Long audio dropout after the first ball obscured a called strike and two catcher pickoff attempts
2. "Three times in a row Montgomery is fired down to first" — Whisper transcribed "two" as "three", and `montb101` (Bob Montgomery) is the catcher, so these are catcher pickoff attempts (`+`) not pitcher pickoffs (`1`, `2`, `3`)

**Source of error:** Extended audio dropout meant most of the at-bat was not represented in the transcript. The one detail that was present — the pickoff throws — was itself miscounted by Whisper and miscoded due to missing catcher/pitcher distinction.

**Note:** The event file's `start` rows should always be used to identify the catcher (position `2`) so catcher pickoff throws can be correctly coded with the `+` prefix. Whisper's count of repeated actions (e.g. "three times in a row") should be treated with caution and verified against audio.

---

### play,4,0,lynnf001 — Inning 4, Top

**Full play:** `play,4,0,lynnf001,00,X,46(1)G4/FO`
**LLM proposed:** `??` (unable to determine)
**Error:** Play not recoverable from transcript alone

**Source of error:** A station ID announcement immediately followed the play, corrupting Whisper's transcription. The ball was hit and the out recorded before the station ID, but Whisper produced garbled output ("About four seconds", "It'd be two", "Alabama makes one") rather than the play call. Station ID announcements are not random — they occur during breaks in the action, meaning the play immediately preceding them is at elevated risk of transcription corruption.

**Note:** Any at-bat immediately followed by a station ID break should be flagged for audio verification.

---

### play,4,0,mcaud101 — Inning 4, Top

**Full play:** `play,4,0,mcaud101,21,BFBX,8/F8`
**LLM proposed:** `?BX`
**Error:** First pitch miscoded as unknown, foul ball missed entirely

**Source of error:** Transcript quality was poor in this at-bat, likely due to proximity to the preceding station ID break. The foul ball was not represented in the transcript at all.

**Note:** At-bats immediately following a station ID break are also at elevated risk of transcription degradation, not just the at-bat preceding it.
