# External IndexTTS runtimes

This repository does not contain IndexTTS source code or model checkpoints.
Install or clone a compatible IndexTTS-2.5 checkout separately and pass its
location to `audiobook render --project-root` when using the default
`indextts-2.5` backend.

On Apple Silicon, the intended initial settings are:

- `device = "mps"`;
- FP32 inference;
- CUDA kernels, DeepSpeed, acceleration engine, and torch compilation disabled;
- QwenEmotion disabled unless explicitly required;
- `PYTORCH_ENABLE_MPS_FALLBACK=1` set before importing PyTorch.

The speaker reference WAV is an explicit input and is recorded in the manifest
by path and checksum. Do not commit private reference audio to this repository.

## MLX IndexTTS 1.5 on Apple Silicon

Install the MLX runtime from its external source checkout into the active Python
environment; do not vendor it or its environment into this repository. Keep the
converted model and speaker prompt external as well. For example:

```bash
uv pip install -e /Users/howard/index-tts-workspace/mlx-indextts-15/source

uv run audiobook render \
  --backend mlx-1.5 \
  --script work/chapter-01-simplified.md \
  --output audio/chapter-01-yuanyuan.wav \
  --model-dir /Users/howard/index-tts-workspace/mlx-indextts-15/models/IndexTTS-1.5-MLX \
  --prompt /Users/howard/index-tts-workspace/index-tts/prompts/voice.wav
```

The model is loaded once per chapter run. Speaker conditioning is stored beside
the ignored chunk workspace as a prompt-SHA-keyed `.npz` cache and reused.
Validated chunks are reused only when the complete manifest identity (backend,
script, prompt, model path, sampling settings, chunking settings, and output
format) still matches.

MLX 1.5 output is validated as mono, 24,000 Hz, PCM 16-bit. Its sampling settings
are read from `config/default.toml`; override them with a separate TOML config
when needed. The `--dry-run` path plans chunks without importing MLX or loading
the model.

### Opt-in real-model smoke test

```bash
RUN_MLX_SMOKE=1 \
MLX_INDEXTTS_RUNTIME_ROOT=/Users/howard/index-tts-workspace/mlx-indextts-15/source \
MLX_INDEXTTS_MODEL_DIR=/Users/howard/index-tts-workspace/mlx-indextts-15/models/IndexTTS-1.5-MLX \
MLX_INDEXTTS_PROMPT=/Users/howard/index-tts-workspace/index-tts/prompts/voice.wav \
uv run pytest -q tests/test_mlx_smoke.py
```
