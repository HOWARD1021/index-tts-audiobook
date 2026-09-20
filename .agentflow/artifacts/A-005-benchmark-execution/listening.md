# Human listening gate — completed with pronunciation follow-up

Owner listened to the fresh Yuanyuan-reference outputs under:
`/Users/howard/index-tts-workspace/previews/issue-8-benchmark-yuanyuan-20260920/`.

## Verdict

- IndexTTS-2.5 is preferred over MLX IndexTTS 1.5 for the current audiobook
  direction. The owner heard it as smoother and with fewer wrong characters.
- MLX 1.5 is not selected for the current default audiobook narrator despite
  its lower measured RTF.
- The pronunciation of `伴隨著` remains a failure. The intended reading is
  `ㄓㄜ` / `ZHE5`; the observed output still sounds like `ㄓㄨˋ` / `ZHU4`.
- The existing text-level override and unit test are insufficient acceptance
  evidence because the real IndexTTS-2.5 acoustic output still fails.

## Required follow-up

Create a pronunciation issue requiring every real-model pronunciation test to
use the default Yuanyuan reference:
`/Users/howard/index-tts-workspace/index-tts/prompts/voice.wav`, which is
byte-identical to `prompts/yuanyuan/yuanyuan_vocals_30s.wav`.

The test fixture must include `伴隨著` and the acceptance gate must listen for
`ㄓㄜ`, not only assert that the prepared text contains `ZHE5`. Candidate audio
forms are preserved externally for comparison:

- `current-annotation.wav`: `伴随<著|ZHE5>高成交量。`
- `direct-pinyin.wav`: `伴随ZHE5高成交量。`
- `plain.wav`: `伴随着高成交量。`

No pronunciation override or runtime file was changed in this benchmark round.
Issue #6 remains responsible for emotion policy; Issue #7 remains responsible
for peak/headroom policy.
