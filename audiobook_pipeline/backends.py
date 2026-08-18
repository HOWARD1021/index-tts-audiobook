"""Lazy-loaded synthesis backends for chapter rendering."""

from __future__ import annotations

import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol

from .config import PipelineConfig

INDEXTTS_25 = "indextts-2.5"
MLX_15 = "mlx-1.5"
BACKEND_NAMES = (INDEXTTS_25, MLX_15)


@dataclass(frozen=True)
class AudioFormat:
    sample_rate: int
    channels: int = 1
    subtype: str = "PCM_16"

    def as_dict(self) -> dict[str, int | str]:
        return asdict(self)


class SynthesisBackend(Protocol):
    def synthesize(self, text: str, output: Path, *, chunk_index: int) -> None:
        """Synthesize one text chunk to ``output``."""


def output_format_for(backend: str, config: PipelineConfig) -> AudioFormat:
    if backend == INDEXTTS_25:
        return AudioFormat(sample_rate=config.sample_rate, channels=config.channels)
    if backend == MLX_15:
        return AudioFormat(sample_rate=24_000)
    raise ValueError(f"unknown backend: {backend}")


def sampling_parameters_for(backend: str, config: PipelineConfig) -> dict[str, object]:
    if backend == INDEXTTS_25:
        return {
            "language": config.language,
            "device": config.device,
            "max_text_tokens_per_segment": config.max_text_tokens_per_segment,
            "interval_silence_ms": config.interval_silence_ms,
            "text_normalization": config.text_normalization,
            "use_random": config.use_random,
            "use_qwen_emo": config.use_qwen_emo,
            "emotion": {
                "vector": list(config.emotion.vector),
                "alpha": config.emotion.alpha,
            },
        }
    if backend == MLX_15:
        return {
            "max_text_tokens_per_segment": config.max_text_tokens_per_segment,
            "max_mel_tokens": config.max_mel_tokens,
            "interval_silence_ms": config.interval_silence_ms,
            "temperature": config.temperature,
            "top_k": config.top_k,
            "top_p": config.top_p,
            "repetition_penalty": config.repetition_penalty,
            "speed": config.speed,
            "seed": config.seed,
            "quantize_bits": config.quantize_bits,
        }
    raise ValueError(f"unknown backend: {backend}")


class IndexTTS25Backend:
    def __init__(
        self,
        *,
        project_root: Path,
        model_dir: Path,
        prompt_wav: Path,
        config: PipelineConfig,
    ) -> None:
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        try:
            from indextts.infer_v2_5 import IndexTTS2
        except ImportError as exc:
            raise RuntimeError(
                f"IndexTTS-2.5 runtime is unavailable under {project_root}"
            ) from exc

        self._prompt_wav = prompt_wav
        self._config = config
        self._model = IndexTTS2(
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

    def synthesize(self, text: str, output: Path, *, chunk_index: int) -> None:
        config = self._config
        self._model.infer(
            spk_audio_prompt=str(self._prompt_wav),
            text=text,
            output_path=str(output),
            lang=config.language,
            emo_vector=list(config.emotion.vector),
            emo_alpha=config.emotion.alpha,
            use_random=config.use_random,
            interval_silence=config.interval_silence_ms,
            max_text_tokens_per_segment=config.max_text_tokens_per_segment,
            duration_factor=1.0,
            text_normalization=config.text_normalization,
        )


class MLX15Backend:
    def __init__(
        self,
        *,
        model_dir: Path,
        prompt_wav: Path,
        speaker_cache: Path,
        config: PipelineConfig,
    ) -> None:
        try:
            from mlx_indextts.generate import IndexTTS
        except ImportError as exc:
            raise RuntimeError(
                "MLX IndexTTS 1.5 runtime is unavailable; install the external "
                "mlx-indextts package in the active environment"
            ) from exc

        self._config = config
        self._model = IndexTTS.load_model(
            model_dir,
            memory_limit_gb=config.memory_limit_gb,
            quantize_bits=config.quantize_bits,
        )
        speaker_cache.parent.mkdir(parents=True, exist_ok=True)
        if not speaker_cache.is_file():
            self._model.save_speaker(prompt_wav, speaker_cache)
        self._speaker_cache = speaker_cache

    def synthesize(self, text: str, output: Path, *, chunk_index: int) -> None:
        config = self._config
        audio = self._model.generate(
            text=text,
            ref_audio=self._speaker_cache,
            max_mel_tokens=config.max_mel_tokens,
            max_text_tokens_per_segment=config.max_text_tokens_per_segment,
            interval_silence=config.interval_silence_ms,
            temperature=config.temperature,
            top_k=config.top_k,
            top_p=config.top_p,
            repetition_penalty=config.repetition_penalty,
            seed=config.seed + chunk_index - 1,
            speed=config.speed,
        )
        self._model.save_audio(audio, output)


def create_backend(
    backend: str,
    *,
    project_root: Path | None,
    model_dir: Path,
    prompt_wav: Path,
    speaker_cache: Path,
    config: PipelineConfig,
) -> SynthesisBackend:
    """Construct one backend session; external runtimes are imported lazily."""

    if backend == INDEXTTS_25:
        if project_root is None:
            raise ValueError("--project-root is required for indextts-2.5")
        return IndexTTS25Backend(
            project_root=project_root,
            model_dir=model_dir,
            prompt_wav=prompt_wav,
            config=config,
        )
    if backend == MLX_15:
        return MLX15Backend(
            model_dir=model_dir,
            prompt_wav=prompt_wav,
            speaker_cache=speaker_cache,
            config=config,
        )
    raise ValueError(f"unknown backend: {backend}")
