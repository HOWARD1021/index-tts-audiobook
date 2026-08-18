"""Backend-neutral orchestration for resumable chapter rendering."""

from __future__ import annotations

import hashlib
import json
import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

from .audio import AudioValidation, concatenate_wavs, validate_wav
from .backends import (
    INDEXTTS_25,
    MLX_15,
    SynthesisBackend,
    create_backend,
    output_format_for,
    sampling_parameters_for,
)
from .chunking import TextChunk, split_text
from .config import PipelineConfig

BackendFactory = Callable[..., SynthesisBackend]


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def plan_chapter(script: str | Path, config: PipelineConfig) -> list[dict[str, Any]]:
    text = Path(script).read_text(encoding="utf-8")
    return [
        {"index": chunk.index, "characters": chunk.characters, "text": chunk.text}
        for chunk in split_text(text, config.max_chunk_chars)
    ]


def _write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    temporary = path.with_name(f"{path.name}.partial")
    temporary.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _run_identity(
    *,
    backend: str,
    script: Path,
    prompt_wav: Path,
    model_dir: Path,
    project_root: Path | None,
    config: PipelineConfig,
) -> dict[str, Any]:
    output_format = output_format_for(backend, config)
    return {
        "format_version": 2,
        "backend": backend,
        "script": str(script),
        "script_sha256": sha256_file(script),
        "prompt_wav": str(prompt_wav),
        "prompt_sha256": sha256_file(prompt_wav),
        "model_dir": str(model_dir),
        "runtime_root": str(project_root) if backend == INDEXTTS_25 else None,
        "sampling_parameters": sampling_parameters_for(backend, config),
        "chunking": {
            "max_chunk_chars": config.max_chunk_chars,
            "inter_chunk_pause_ms": config.inter_chunk_pause_ms,
            "max_seconds_per_char": config.max_seconds_per_char,
        },
        "output_format": output_format.as_dict(),
    }


def _identity_matches(previous: dict[str, Any], identity: dict[str, Any]) -> bool:
    return all(previous.get(key) == value for key, value in identity.items())


def _validated_chunk(
    chunk_wav: Path,
    chunk: TextChunk,
    *,
    sample_rate: int,
    channels: int,
    subtype: str,
    max_seconds_per_char: float,
) -> AudioValidation:
    return validate_wav(
        chunk_wav,
        expected_sample_rate=sample_rate,
        expected_channels=channels,
        expected_subtype=subtype,
        max_seconds_per_char=max_seconds_per_char,
        text_characters=chunk.characters,
    )


def render_chapter(
    script: str | Path,
    output: str | Path,
    *,
    backend: str = INDEXTTS_25,
    project_root: str | Path | None = None,
    prompt_wav: str | Path,
    config: PipelineConfig,
    model_dir: str | Path | None = None,
    dry_run: bool = False,
    backend_factory: BackendFactory = create_backend,
) -> Path:
    """Render one chapter while sharing resume, validation, and manifest logic."""

    if backend not in {INDEXTTS_25, MLX_15}:
        raise ValueError(f"unknown backend: {backend}")

    script = Path(script).expanduser().resolve()
    output = Path(output).expanduser().resolve()
    prompt_wav = Path(prompt_wav).expanduser().resolve()
    resolved_project_root = (
        Path(project_root).expanduser().resolve() if project_root is not None else None
    )
    if model_dir is None:
        if backend == INDEXTTS_25:
            if resolved_project_root is None:
                raise ValueError("--project-root is required for indextts-2.5")
            resolved_model_dir = (resolved_project_root / "checkpoints").resolve()
        else:
            raise ValueError("--model-dir is required for mlx-1.5")
    else:
        resolved_model_dir = Path(model_dir).expanduser().resolve()

    text = script.read_text(encoding="utf-8")
    chunks = split_text(text, config.max_chunk_chars)
    if not chunks:
        raise ValueError(f"script contains no narration text: {script}")

    identity = _run_identity(
        backend=backend,
        script=script,
        prompt_wav=prompt_wav,
        model_dir=resolved_model_dir,
        project_root=resolved_project_root,
        config=config,
    )
    if dry_run:
        return output

    audio_format = output_format_for(backend, config)
    chunk_root = output.parent / f"{output.stem}.chunks"
    text_root = chunk_root / "text"
    manifest_path = output.with_suffix(".manifest.json")
    text_root.mkdir(parents=True, exist_ok=True)

    previous: dict[str, Any] = {}
    if manifest_path.is_file():
        try:
            previous = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            previous = {}
    identity_matches = _identity_matches(previous, identity)
    previous_records = (
        {
            record.get("index"): record
            for record in previous.get("chunks", [])
            if isinstance(record, dict)
        }
        if identity_matches
        else {}
    )

    manifest: dict[str, Any] = {**identity, "status": "in_progress", "chunks": []}

    session: SynthesisBackend | None = None
    wavs: list[Path] = []
    prompt_sha = identity["prompt_sha256"]
    speaker_cache_key = sha256_text(f"{backend}\n{resolved_model_dir}\n{prompt_sha}")
    speaker_cache = chunk_root / f"speaker-{speaker_cache_key[:16]}.npz"

    for chunk in chunks:
        chunk_text = text_root / f"{chunk.index:04d}.txt"
        chunk_wav = chunk_root / f"{chunk.index:04d}.wav"
        text_sha = sha256_text(chunk.text)
        prior = previous_records.get(chunk.index, {})
        validation = None
        reusable = (
            prior.get("status") == "validated"
            and prior.get("text_sha256") == text_sha
            and chunk_wav.is_file()
        )
        if reusable:
            validation = _validated_chunk(
                chunk_wav,
                chunk,
                sample_rate=audio_format.sample_rate,
                channels=audio_format.channels,
                subtype=audio_format.subtype,
                max_seconds_per_char=config.max_seconds_per_char,
            )
            reusable = validation.ok and prior.get("sha256") == sha256_file(chunk_wav)

        if not reusable:
            if session is None:
                session = backend_factory(
                    backend,
                    project_root=resolved_project_root,
                    model_dir=resolved_model_dir,
                    prompt_wav=prompt_wav,
                    speaker_cache=speaker_cache,
                    config=config,
                )
            partial_wav = chunk_wav.with_name(f"{chunk_wav.stem}.partial.wav")
            session.synthesize(chunk.text, partial_wav, chunk_index=chunk.index)
            validation = _validated_chunk(
                partial_wav,
                chunk,
                sample_rate=audio_format.sample_rate,
                channels=audio_format.channels,
                subtype=audio_format.subtype,
                max_seconds_per_char=config.max_seconds_per_char,
            )
            if not validation.ok:
                raise RuntimeError(
                    f"chunk {chunk.index} failed validation: {validation.errors}"
                )
            os.replace(partial_wav, chunk_wav)

        chunk_text.write_text(chunk.text, encoding="utf-8")
        assert validation is not None
        record = {
            "index": chunk.index,
            "text": str(chunk_text),
            "text_sha256": text_sha,
            "wav": str(chunk_wav),
            "characters": chunk.characters,
            "duration_seconds": validation.duration_seconds,
            "sha256": sha256_file(chunk_wav),
            "status": "validated",
            "reused": reusable,
        }
        manifest["chunks"].append(record)
        _write_manifest(manifest_path, manifest)
        wavs.append(chunk_wav)

    concatenate_wavs(
        wavs,
        output,
        pause_ms=config.inter_chunk_pause_ms,
        expected_sample_rate=audio_format.sample_rate,
        expected_channels=audio_format.channels,
        expected_subtype=audio_format.subtype,
    )
    final_validation = validate_wav(
        output,
        expected_sample_rate=audio_format.sample_rate,
        expected_channels=audio_format.channels,
        expected_subtype=audio_format.subtype,
    )
    if not final_validation.ok:
        raise RuntimeError(
            f"final chapter failed validation: {final_validation.errors}"
        )

    manifest.update(
        status="complete",
        final_wav=str(output),
        final_sha256=sha256_file(output),
        final_duration_seconds=final_validation.duration_seconds,
    )
    _write_manifest(manifest_path, manifest)
    return output
