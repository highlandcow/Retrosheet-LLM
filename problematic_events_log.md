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
