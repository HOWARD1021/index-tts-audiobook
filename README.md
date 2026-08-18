# IndexTTS Audiobook

Reliable long-form audiobook generation around external IndexTTS runtimes.

This repository owns the audiobook pipeline, not the IndexTTS model or its
checkpoints. Keep the canonical manuscript separate from the narration script:
Traditional Chinese remains the source, while a reviewed Simplified Chinese
derivative is used for the current IndexTTS Mandarin path.

## Status

The pipeline supports the existing IndexTTS-2.5 backend and an MLX IndexTTS 1.5
backend for Apple Silicon. Both reuse the same text preparation,
paragraph-preserving chunking, manifest, resume, validation, and concatenation
flow. Full-book rendering is intentionally gated by preview and human listening
checks.

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

# Render with an existing IndexTTS-2.5 checkout and speaker reference.
uv run audiobook render \
  --backend indextts-2.5 \
  --script work/chapter-01-zh-simplified.md \
  --output audio/chapter-01.wav \
  --project-root /path/to/index-tts \
  --prompt /path/to/speaker.wav \
  --device mps

# Render through an externally installed MLX IndexTTS 1.5 runtime.
uv run audiobook render \
  --backend mlx-1.5 \
  --script work/chapter-01-zh-simplified.md \
  --output audio/chapter-01-yuanyuan.wav \
  --model-dir /Users/howard/index-tts-workspace/mlx-indextts-15/models/IndexTTS-1.5-MLX \
  --prompt /Users/howard/index-tts-workspace/index-tts/prompts/voice.wav
```

The render command keeps chunk text, chunk WAVs, and a manifest next to the
chapter output. It skips a chunk only when its text and configuration identity
still match, its checksum is unchanged, and its WAV passes backend-specific
validation. Use `--dry-run` to inspect chunks and output format without importing
or loading a model.

## Quality gates

- Preserve the Traditional source and review the derived Simplified script.
- Add glossary overrides and Pinyin annotations for high-risk terms.
- Preview representative prose, names, numbers, quotations, and financial terms.
- Reject empty, malformed, non-finite, wrong-format, or implausibly long WAVs.
- Listen to the preview before starting a full chapter or book render.

## Repository boundaries

Do not commit model checkpoints, private speaker references, speaker-conditioning
caches, generated audiobook files, local caches, virtual environments, or
source-book copies. The 2.5 checkout is selected through `--project-root`; the
MLX package, converted model, and prompt remain external and are selected at
runtime. See [`docs/upstream-runtime.md`](docs/upstream-runtime.md).

## Development branch

`main` is the canonical development trunk and the repository's default branch.
All maintained pipeline code, configuration, tests, and documentation belong on
`main`. Short-lived feature branches may be used for isolated work, but they
must branch from and return to `main`; there is no separate long-lived `develop`
branch.

Keep checkpoints, prompts, speaker references, generated audio, source books,
local work directories, and agent checkpoints outside the repository. See
[`CONTRIBUTING.md`](CONTRIBUTING.md) for the complete contribution boundary.
