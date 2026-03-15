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

---

### play,8,0,yastc101 — Inning 8, Top

**Full play:** `play,8,0,yastc101,??,CX,7/F7D` (sequence uncertain)
**LLM proposed:** `CX` (only pitch recoverable from transcript)
**Error:** Unknown — extended dropout after first pitch leaves sequence unresolvable

**Source of error:** After a called strike at [96:44], the transcript produces only dots from [96:45] through [97:38] — approximately 53 seconds of crowd noise with no transcribed commentary. Only the result (fly to left) is known from context.

**Hypothesis:** Whisper struggles to transcribe speech that occurs immediately after prolonged crowd noise. The voice activity detection likely needs a moment to re-engage after a long stretch of non-speech audio, causing it to miss the announcer's re-entry point. This is not hallucination — Whisper is simply not transcribing content that is present in the audio.

**Note:** Prolonged crowd noise followed by resumed commentary is a distinct failure mode from the brief crowd surge dropouts seen earlier. A potential fix on the speech-to-text side would be to adjust Whisper's voice activity detection parameters to be more sensitive to speech re-entry after silence/noise. Worth checking the audio to confirm the broadcaster was speaking during the dropout window.

---

### play,9,0,carbb101 — Inning 9, Top

**Full play:** `play,9,0,carbb101,01,CX,S8/L8.1-2`
**LLM proposed:** `??,UX` (sequence not recoverable from transcript)
**Error:** Sequence could not be determined from transcript alone — required audio verification

**Source of error:** After Bernie Carbo steps in at [113:36], the transcript produces only dots from [113:40] through [114:35] — approximately 55 seconds with no transcribed commentary. The at-bat is entirely absent from the transcript. Only the result (line single) is recoverable from context after the dropout ends.

**Hypothesis:** The dropout coincides with what was likely a significant crowd noise moment — Carbo was a pinch hitter in a high-leverage situation (top of the 9th, scoreless game, Cooper on second). The crowd reaction to him stepping in, or to the pitch itself, may have triggered the same prolonged crowd noise failure mode seen in `play,8,0,yastc101`. Whisper's voice activity detection appears to have failed to re-engage until after the at-bat concluded.

**Note:** High-leverage pinch hitting situations in late innings are a risk point for this failure mode — crowd noise tends to be loudest precisely when the at-bat is most important.

---

### play,9,0,harpt101 — Inning 9, Top

**Full play:** `play,9,0,harpt101,12,FFFFFBX,54(1)/G56/FO.2-3!`
**LLM proposed:** `02,FCFFFX`
**Error:** Second pitch coded as C (called strike) instead of F (foul); ball coded as B instead of F; missing one foul overall; count wrong (02 vs 12)

**Transcript (Whisper):**
```
[115:47.94]  Curve bounce ball outside of third.
[115:51.52]  And it's all in two.
```

**Actual words:**
```
[115:47.94]  Curve! Bounced foul, outside of third.
[115:51.52]  And it's oh and two.
```

**Source of error:** Two distinct Whisper failures on consecutive lines. First, "bounced foul, outside of third" was transcribed as "bounce ball outside of third" — losing the word "foul" and making the pitch description ambiguous. Second, the count confirmation "oh and two" (0-2) was transcribed as "all in two" — rendering it uninterpretable as a count. The LLM then reasoned incorrectly from the garbled count confirmation, overriding what should have been a recoverable pitch description.

**Note on recoverability:** Even with the Whisper transcript, "bounce...outside of third" should have been readable as a foul — a pitch described as ending up outside of third base is a foul ball, not a ball four. This was a close call that a more careful reading might have caught.

**Tension — prompt complexity vs. transcript quality:** This case raises a question about where to invest effort. The audio here was not particularly poor — the actual words were clear enough. The failure was entirely in the transcript. Adding prompt rules to compensate for Whisper mishearings of this kind risks making the prompt unwieldy without addressing the root cause. The problematic events log is building a strong evidence base for where Whisper struggles; the better long-term investment may be improving transcript quality (Whisper parameter tuning, audio pre-processing, alternative ASR) rather than adding more defensive prompt rules.

---

### play,10,0,lynnf001 — Inning 10, Top

**Full play:** `play,10,0,lynnf001,30,BBBB,W`
**LLM proposed:** `30,BBBB,W` ✅ — sequence correct despite transcript issue

**Source of issue:** The transcript appears to repeat the first two pitches of the at-bat, with the audio doubling back on itself. The first pitch and "ball one" confirmation appear twice in the transcript before continuing normally.

**Why it was not problematic:** Count confirmations anchored the sequence correctly regardless of the duplication. "Ball three" at [136:28] and "ball four" at [136:43] provided reliable endpoints, and the walk on four pitches was confirmed explicitly. The repetition in the middle did not cause a miscounting error.

**Note:** Audio repeating itself is a new failure mode not previously seen. It could potentially cause double-counting errors in at-bats without strong count confirmations — particularly foul-heavy at-bats where the count stays frozen. Worth watching for in future games.

---

### play,10,1,aloms101 — Inning 10, Bottom

**Full play:** `play,10,1,aloms101,31,BCBBB,W`
**LLM proposed:** `31,BBCBB,W`
**Error:** Pitch order wrong — C coded at third position instead of second

**Source of error:** Pure Whisper failure. The transcript shows "ball one" at [142:44] followed immediately by "ball two" at [142:45] — half a second apart, too fast for two separate pitches. The LLM correctly identified this as suspicious but interpreted [142:45] as a second ball rather than a garbled "strike one." The audio has a called strike as the second pitch, which Whisper transcribed as "ball two."

**Note:** When two count confirmations appear in rapid succession and one of them contradicts the expected sequence, consider that Whisper may have misheard the pitch type (ball vs. strike) rather than that two pitches were thrown. Audio verification required.

---

### play,10,1,madde101 — Inning 10, Bottom (walk-off)

**Full play:** `play,10,1,madde101,00,X,S7/G56.3-H;1-2`
**LLM proposed:** `??,UX`
**Error:** Count coded as ?? instead of 00; sequence marked uncertain

**Source of error:** The game-winning walk-off hit triggered an immediate and sustained crowd noise dropout from [147:12] onwards. The entire at-bat is absent from the transcript — only the mound conference beforehand is present. This is the most extreme example of the high-leverage crowd noise dropout pattern seen throughout the game.

**Note:** When no pitches are recoverable from the transcript, the correct count is `??` — not `00`. `00` would imply confirmed knowledge that no pitches were thrown before contact, which cannot be determined from the transcript alone. Only audio verification can establish the correct count. The result `S7` anchors the final pitch as X, but everything before it remains unknown.
