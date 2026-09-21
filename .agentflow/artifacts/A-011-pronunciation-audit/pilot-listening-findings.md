# Chapter-four pilot listening findings

Owner feedback on the completed pilot:

- Around `00:01`, `第四章` is a standalone three-character chunk and is read too slowly.
- Around `01:30`, the audio maps to the isolated bold span `不是`; the short styled span is read too slowly and creates a sudden pacing change.
- A laugh-like vocal moment is pleasant but has no corresponding laughter cue in the source text. The pilot used zero emotion vectors and `use_qwen_emo=false`, so it is not an intentional configured emotion. It should be treated as model/reference prosody until isolated by a control run.

Recommended Issue #6 changes:

1. Merge chapter heading/title text or exclude standalone headings from normal narration timing.
2. Do not render one- or two-character emphasis spans as independent synthesis calls; promote them to surrounding sentence context or keep them ordinary text.
3. Do not change global speed before testing these boundary/span fixes.
