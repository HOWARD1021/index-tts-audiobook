"""IndexTTS-2.5 integration boundary for chapter rendering."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
from typing import Any

from .audio import concatenate_wavs, validate_wav
from .chunking import split_text
from .config import PipelineConfig


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def plan_chapter(script: str | Path, config: PipelineConfig) -> list[dict[str, Any]]:
    text = Path(script).read_text(encoding="utf-8")
    return [
        {"index": chunk.index, "characters": chunk.characters, "text": chunk.text}
        for chunk in split_text(text, config.max_chunk_chars)
    ]


def render_chapter(
    script: str | Path,
    output: str | Path,
    *,
    project_root: str | Path,
    prompt_wav: str | Path,
    config: PipelineConfig,
    model_dir: str | Path | None = None,
) -> Path:
    """Render a chapter using one reused IndexTTS-2.5 model instance."""

    project_root = Path(project_root).resolve()
    script = Path(script).resolve()
    prompt_wav = Path(prompt_wav).resolve()
    output = Path(output).resolve()
    model_dir = Path(model_dir or project_root / "checkpoints").resolve()
    chunk_root = output.parent / f"{output.stem}.chunks"
    text_root = chunk_root / "text"
    chunk_root.mkdir(parents=True, exist_ok=True)
    text_root.mkdir(parents=True, exist_ok=True)

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from indextts.infer_v2_5 import IndexTTS2  # external runtime dependency

    tts = IndexTTS2(
        cfg_path=str(model_dir / "config.yaml"),
        model_dir=str(model_dir),
        device=config.device,
        use_bf16=False,
        use_cuda_kernel=False,
        use_deepspeed=False,
        use_accel=False,
        use_torch_compile=False,
        use_qwen_emo=config.use_qwen_emo,
    )
    text = script.read_text(encoding="utf-8")
    chunks = split_text(text, config.max_chunk_chars)
    records: list[dict[str, Any]] = []
    wavs: list[Path] = []
    for chunk in chunks:
        chunk_text = text_root / f"{chunk.index:04d}.txt"
        chunk_wav = chunk_root / f"{chunk.index:04d}.wav"
        chunk_text.write_text(chunk.text, encoding="utf-8")
        existing = validate_wav(
            chunk_wav,
            expected_sample_rate=config.sample_rate,
            expected_channels=config.channels,
            max_seconds_per_char=config.max_seconds_per_char,
            text_characters=chunk.characters,
        ) if chunk_wav.exists() else None
        if existing is None or not existing.ok:
            tts.infer(
                spk_audio_prompt=str(prompt_wav),
                text=chunk.text,
                output_path=str(chunk_wav),
                lang=config.language,
                emo_vector=list(config.emotion.vector),
                emo_alpha=config.emotion.alpha,
                use_random=config.use_random,
                interval_silence=config.interval_silence_ms,
                max_text_tokens_per_segment=config.max_text_tokens_per_segment,
                duration_factor=1.0,
                text_normalization=config.text_normalization,
            )
            existing = validate_wav(
                chunk_wav,
                expected_sample_rate=config.sample_rate,
                expected_channels=config.channels,
                max_seconds_per_char=config.max_seconds_per_char,
                text_characters=chunk.characters,
            )
        if not existing.ok:
            raise RuntimeError(f"chunk {chunk.index} failed validation: {existing.errors}")
        wavs.append(chunk_wav)
        records.append({
            "index": chunk.index,
            "text": str(chunk_text),
            "wav": str(chunk_wav),
            "characters": chunk.characters,
            "duration_seconds": existing.duration_seconds,
            "sha256": sha256_file(chunk_wav),
            "status": "validated",
        })

    concatenate_wavs(wavs, output, pause_ms=config.inter_chunk_pause_ms, expected_sample_rate=config.sample_rate)
    manifest = {
        "status": "complete",
        "script": str(script),
        "script_sha256": sha256_file(script),
        "prompt_wav": str(prompt_wav),
        "prompt_sha256": sha256_file(prompt_wav),
        "model_dir": str(model_dir),
        "config": config.as_dict(),
        "chunks": records,
        "final_wav": str(output),
        "final_sha256": sha256_file(output),
    }
    output.with_suffix(".manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return output
