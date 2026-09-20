# Human listening gate — pending

No human listening verdict has been received. Issue #5 remains open.

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
| Speaker identity continuity | Pending human |
| 伴隨著 pronunciation | Pending human |
| No spoken Markdown/bracket/cue leakage | Pending human |
| Bold/italic emotion strength | Pending human |
| Natural joins, pauses, and pitch | Pending human |
| Audible distortion/clipping | Pending human |

Objective warning: 33,716 / 1,485,242 samples (2.2701%) reach ±32,767.
The external runtime clamps samples at that amplitude. Existing format/finite/
duration checks pass, but they do not certify absence of clipping or good sound.
No normalization, preset tuning, or phrase/sentence policy changes were applied.

If joins or emotion strength fail, hand the observations and timestamps to
Issue #6. Peak/headroom acceptance is a release-quality concern for Issue #7;
do not silently change that policy here. No external issue comment was posted.
