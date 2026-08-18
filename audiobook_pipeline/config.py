"""Configuration loading with explicit, serializable generation settings."""

from __future__ import annotations

import tomllib
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class EmotionConfig:
    vector: tuple[float, ...] = (0.30, 0.0, 0.0, 0.0, 0.0, 0.0, 0.15, 0.35)
    alpha: float = 1.0


@dataclass(frozen=True)
class PipelineConfig:
    language: str = "ZH"
    device: str = "mps"
    max_chunk_chars: int = 400
    max_text_tokens_per_segment: int = 100
    interval_silence_ms: int = 250
    inter_chunk_pause_ms: int = 450
    text_normalization: bool = True
    use_random: bool = False
    use_qwen_emo: bool = False
    sample_rate: int = 22050
    channels: int = 1
    max_seconds_per_char: float = 0.8
    max_mel_tokens: int = 800
    temperature: float = 1.0
    top_k: int = 30
    top_p: float = 0.8
    repetition_penalty: float = 10.0
    speed: float = 1.0
    seed: int = 42
    memory_limit_gb: float = 8.0
    quantize_bits: int | None = None
    emotion: EmotionConfig = field(default_factory=EmotionConfig)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_config(path: str | Path | None = None) -> PipelineConfig:
    """Load TOML configuration, falling back to safe project defaults."""

    if path is None:
        return PipelineConfig()

    raw = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    values = dict(raw.get("defaults", {}))
    emotion_values = values.pop("emotion", {})
    if "vector" in emotion_values:
        emotion_values["vector"] = tuple(float(x) for x in emotion_values["vector"])
    emotion = EmotionConfig(**emotion_values)
    return PipelineConfig(emotion=emotion, **values)


def with_overrides(config: PipelineConfig, **overrides: Any) -> PipelineConfig:
    """Return a config with scalar CLI overrides without losing nested types."""

    return replace(config, **overrides)
