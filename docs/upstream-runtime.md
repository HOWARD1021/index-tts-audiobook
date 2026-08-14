# Upstream IndexTTS runtime

This repository does not contain IndexTTS source code or model checkpoints.
Install or clone a compatible IndexTTS-2.5 checkout separately and pass its
location to `audiobook render --project-root`.

On Apple Silicon, the intended initial settings are:

- `device = "mps"`;
- FP32 inference;
- CUDA kernels, DeepSpeed, acceleration engine, and torch compilation disabled;
- QwenEmotion disabled unless explicitly required;
- `PYTORCH_ENABLE_MPS_FALLBACK=1` set before importing PyTorch.

The speaker reference WAV is an explicit input and is recorded in the manifest
by path and checksum. Do not commit private reference audio to this repository.
