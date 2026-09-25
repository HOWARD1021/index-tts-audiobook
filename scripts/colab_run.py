"""Turnkey execution helper for Google Colab."""

import os
from pathlib import Path
import subprocess
import sys

from huggingface_hub import snapshot_download

DRIVE_ROOT = Path("/content/drive/MyDrive/audiobook-workspace")
CHECKPOINTS_DIR = DRIVE_ROOT / "checkpoints" / "IndexTTS-2.5"
PROMPTS_DIR = DRIVE_ROOT / "prompts"
SCRIPTS_DIR = DRIVE_ROOT / "scripts"
OUTPUT_DIR = DRIVE_ROOT / "output"
CONFIG_DIR = DRIVE_ROOT / "config"

for p in [CHECKPOINTS_DIR, PROMPTS_DIR, SCRIPTS_DIR, OUTPUT_DIR, CONFIG_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# 1. Check & download IndexTTS-2.5 weights
required_files = ["config.yaml", "codec.pth", "gpt.pth", "s2mel.pth", "wav2vec2bert_stats.pt"]
if not all((CHECKPOINTS_DIR / f).exists() for f in required_files):
    print("⏳ Auto-downloading IndexTTS-2.5 checkpoints from Hugging Face (~4.3 GB)...")
    snapshot_download(
        repo_id="IndexTeam/IndexTTS-2.5",
        local_dir=str(CHECKPOINTS_DIR),
        local_dir_use_symlinks=False,
    )
    print("✅ IndexTTS-2.5 checkpoints downloaded.")

# 2. Ensure config exists
config_path = CONFIG_DIR / "colab-cuda.toml"
if not config_path.exists():
    config_path.write_text("""[defaults]
language = "ZH"
device = "cuda"
max_chunk_chars = 400
max_text_tokens_per_segment = 100
interval_silence_ms = 250
inter_chunk_pause_ms = 450
emotion_span_pause_ms = 80
text_normalization = true
use_random = false
use_qwen_emo = false
sample_rate = 22050
channels = 1
max_seconds_per_char = 0.8
max_mel_tokens = 800
temperature = 1.0
top_k = 30
top_p = 0.8
repetition_penalty = 10.0
speed = 1.0
seed = 42
memory_limit_gb = 16.0

[defaults.emotion]
vector = [0.30, 0.0, 0.0, 0.0, 0.0, 0.0, 0.15, 0.35]
alpha = 1.0
bold_vector = [0.45, 0.0, 0.0, 0.0, 0.0, 0.20, 0.10]
bold_alpha = 1.0
italic_vector = [0.15, 0.0, 0.0, 0.0, 0.0, 0.20, 0.0, 0.45]
italic_alpha = 1.0
""", encoding="utf-8")

# 3. Ensure sample script exists
sample_script = SCRIPTS_DIR / "sample-chapter.md"
prep_script = SCRIPTS_DIR / "sample-chapter-simplified.md"
if not prep_script.exists():
    if not sample_script.exists():
        sample_script.write_text("# 第一章：啟程\n\n這是一個寧靜的早晨，陽光穿透薄霧，灑在青石街道上。旅人背起行囊，準備迎接未知的冒險。\n\n**「這條路將會通向何方？」** 他心中自問，步伐卻顯得堅定無比。\n", encoding="utf-8")
    subprocess.run(["audiobook", "prepare", "--input", str(sample_script), "--output", str(prep_script)], check=True)

# 4. Check prompt audio
prompt_wavs = list(PROMPTS_DIR.glob("*.wav"))
if not prompt_wavs:
    print(f"❌ Error: Please upload voice.wav into: {PROMPTS_DIR}")
    sys.exit(1)

selected_prompt = prompt_wavs[0]
output_wav = OUTPUT_DIR / "sample-chapter.wav"

print(f"🎙️ Using prompt: {selected_prompt.name}")
print(f"🎯 Output: {output_wav}")
print("🚀 Starting CUDA render...")

env = os.environ.copy()
env["USE_TF"] = "0"
cmd = [
    "audiobook", "render",
    "--backend", "indextts-2.5",
    "--script", str(prep_script),
    "--output", str(output_wav),
    "--project-root", "/content/index-tts",
    "--model-dir", str(CHECKPOINTS_DIR),
    "--prompt", str(selected_prompt),
    "--config", str(config_path),
    "--device", "cuda",
]

subprocess.run(cmd, env=env, check=True)
print("🎉 Render complete!")
