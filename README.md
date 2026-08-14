# IndexTTS Audiobook

Reliable long-form audiobook generation around an external IndexTTS-2.5 checkout.

This repository owns the audiobook pipeline, not the IndexTTS model or its
checkpoints. Keep the canonical manuscript separate from the narration script:
Traditional Chinese remains the source, while a reviewed Simplified Chinese
derivative is used for the current IndexTTS Mandarin path.

## Status

The first vertical slice covers text preparation, paragraph-preserving chunk
planning, WAV validation, configuration loading, and the IndexTTS-2.5 render
boundary. Full-book rendering is intentionally gated by preview and human
listening checks.

## Quick start

```bash
uv sync --extra dev

# Derive a narration script without changing the source manuscript.
uv run audiobook prepare \
  --input /path/to/chapter-01-zh.md \
  --output work/chapter-01-zh-simplified.md

# Inspect the planned chunks without loading a model.
uv run audiobook plan \
  --script work/chapter-01-zh-simplified.md \
  --max-chars 400

# Render with an existing IndexTTS checkout and speaker reference.
uv run audiobook render \
  --script work/chapter-01-zh-simplified.md \
  --output audio/chapter-01.wav \
  --project-root /path/to/index-tts \
  --prompt /path/to/speaker.wav \
  --device mps
```

The render command keeps chunk text, chunk WAVs, and a manifest next to the
chapter output. It skips a chunk only when its text and configuration identity
still match and its WAV passes validation.

## Quality gates

- Preserve the Traditional source and review the derived Simplified script.
- Add glossary overrides and Pinyin annotations for high-risk terms.
- Preview representative prose, names, numbers, quotations, and financial terms.
- Reject empty, malformed, non-finite, wrong-format, or implausibly long WAVs.
- Listen to the preview before starting a full chapter or book render.

## Repository boundaries

Do not commit model checkpoints, private speaker references, generated audiobook
files, local caches, or source-book copies. The upstream model repository is
configured at runtime through `--project-root`.

## Development branch

`main` is the canonical development trunk and the repository's default branch.
All maintained pipeline code, configuration, tests, and documentation belong on
`main`. Short-lived feature branches may be used for isolated work, but they
must branch from and return to `main`; there is no separate long-lived `develop`
branch.

Keep checkpoints, prompts, speaker references, generated audio, source books,
local work directories, and agent checkpoints outside the repository. See
[`CONTRIBUTING.md`](CONTRIBUTING.md) for the complete contribution boundary.
