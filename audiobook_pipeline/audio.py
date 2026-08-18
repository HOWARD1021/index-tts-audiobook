"""Audio validation and safe chapter concatenation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import soundfile as sf


@dataclass(frozen=True)
class AudioValidation:
    path: str
    ok: bool
    duration_seconds: float
    sample_rate: int | None
    channels: int | None
    subtype: str | None
    errors: tuple[str, ...] = ()


def validate_wav(
    path: str | Path,
    *,
    expected_sample_rate: int = 22050,
    expected_channels: int = 1,
    expected_subtype: str = "PCM_16",
    max_seconds_per_char: float | None = None,
    text_characters: int | None = None,
) -> AudioValidation:
    """Validate a generated WAV and optionally reject duration outliers."""

    path = Path(path)
    errors: list[str] = []
    sample_rate = channels = None
    subtype = None
    duration = 0.0
    try:
        info = sf.info(path)
        sample_rate = info.samplerate
        channels = info.channels
        subtype = info.subtype
        duration = float(info.duration)
        samples, _ = sf.read(path, always_2d=False)
        if samples.size == 0:
            errors.append("empty audio")
        elif not np.isfinite(samples).all():
            errors.append("audio contains non-finite samples")
    except Exception as exc:  # pragma: no cover - exact decoder errors vary
        errors.append(f"unreadable WAV: {exc}")

    if sample_rate != expected_sample_rate:
        errors.append(f"sample rate {sample_rate} != {expected_sample_rate}")
    if channels != expected_channels:
        errors.append(f"channels {channels} != {expected_channels}")
    if subtype != expected_subtype:
        errors.append(f"subtype {subtype} != {expected_subtype}")
    if max_seconds_per_char is not None and text_characters is not None:
        maximum = max(5.0, text_characters * max_seconds_per_char + 5.0)
        if duration > maximum:
            errors.append(
                f"duration {duration:.2f}s exceeds {maximum:.2f}s sanity limit"
            )

    return AudioValidation(
        path=str(path),
        ok=not errors,
        duration_seconds=duration,
        sample_rate=sample_rate,
        channels=channels,
        subtype=subtype,
        errors=tuple(errors),
    )


def concatenate_wavs(
    inputs: list[str | Path],
    output: str | Path,
    *,
    pause_ms: int = 450,
    expected_sample_rate: int = 22050,
    expected_channels: int = 1,
    expected_subtype: str = "PCM_16",
) -> None:
    """Concatenate validated mono PCM-16 WAV files with a fixed pause."""

    if not inputs:
        raise ValueError("at least one WAV is required")
    arrays: list[np.ndarray] = []
    for path in inputs:
        validation = validate_wav(
            path,
            expected_sample_rate=expected_sample_rate,
            expected_channels=expected_channels,
            expected_subtype=expected_subtype,
        )
        if not validation.ok:
            raise ValueError(f"invalid chunk {path}: {'; '.join(validation.errors)}")
        samples, sample_rate = sf.read(path, dtype="float32")
        if sample_rate != expected_sample_rate:
            raise ValueError(f"unexpected sample rate for {path}")
        arrays.append(np.asarray(samples, dtype=np.float32))
    pause = np.zeros(round(expected_sample_rate * pause_ms / 1000), dtype=np.float32)
    merged: list[np.ndarray] = []
    for index, array in enumerate(arrays):
        if index:
            merged.append(pause)
        merged.append(array)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    sf.write(
        output, np.concatenate(merged), expected_sample_rate, subtype=expected_subtype
    )
