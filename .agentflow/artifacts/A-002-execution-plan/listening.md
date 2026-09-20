# Human listening gate — completed: quality fail / Issue #6 handoff

Human listening verdict received from the owner. Objective generation and file
validation passed, but the overall delivery is too excited for audiobook
narration. Issue #5 is complete as a diagnostic preview; the acoustic profile
decision is handed to Issue #6.

Audio: `/Users/howard/index-tts-workspace/previews/issue-5-20260920-v3/preview.wav`
Duration: 67.3579 seconds. Backend: IndexTTS-2.5 / MPS / FP32 / QwenEmotion off.
Reference: `/Users/howard/orca/workspaces/index-tts/horseshoe/prompts/voice.wav`.

Listen at:

- 00:00–00:03: ordinary voice.
- 00:03.39–00:05.90: first bold phrase.
- 00:05.98–00:20.79: ordinary passage containing the ZHE5 override.
- 00:24.27–00:27.61: second bold phrase.
- 00:29.25–00:35.52: italic passage.
- 00:35.97–01:07.36: long bold passage; cross-chunk join at 00:49.68.

| Check | Verdict |
| --- | --- |
| Speaker identity continuity | Not separately rejected; overall delivery failed |
| 伴隨著 pronunciation | Not separately rejected |
| No spoken Markdown/bracket/cue leakage | Not separately rejected |
| Bold/italic emotion strength | Failed: overall voice is too excited |
| Natural joins, pauses, and pitch | Needs re-evaluation after profile change |
| Audible distortion/clipping | Needs follow-up; rail warning remains |

Owner verdict: the current overall delivery is too excited and is unsuitable
for audiobook narration. Do not reuse the current emphasis profile as the
default audiobook voice.

Issue #6 decision space:

- test a restrained affirmative / confident emotion for selective emphasis;
- test a light attention cue only where the listener must notice a point;
- test no explicit emotion vector for most narration, keeping only short
  pauses at emphasis boundaries.

No option is selected in this ticket. Preserve the current preview and presets
until Issue #6 chooses and tests a policy. Peak/headroom acceptance remains an
Issue #7 release concern.

Objective warning: 33,716 / 1,485,242 samples (2.2701%) reach ±32,767.
The external runtime clamps samples at that amplitude. Existing format/finite/
duration checks pass, but they do not certify absence of clipping or good sound.
No normalization, preset tuning, or phrase/sentence policy changes were applied.

If joins or emotion strength fail, hand the observations and timestamps to
Issue #6. Peak/headroom acceptance is a release-quality concern for Issue #7;
do not silently change that policy here. No external issue comment was posted.
