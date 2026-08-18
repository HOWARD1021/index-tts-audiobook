import sys
from types import ModuleType

import numpy as np
import soundfile as sf

from audiobook_pipeline.backends import (
    INDEXTTS_25,
    MLX_15,
    MLX15Backend,
    output_format_for,
)
from audiobook_pipeline.config import PipelineConfig


def test_backend_output_formats_differ():
    config = PipelineConfig()
    assert output_format_for(INDEXTTS_25, config).sample_rate == 22_050
    assert output_format_for(MLX_15, config).sample_rate == 24_000
    assert output_format_for(MLX_15, config).subtype == "PCM_16"


def test_mlx_model_and_speaker_conditioning_are_reused(monkeypatch, tmp_path):
    calls = {"loads": 0, "speakers": 0, "generations": 0}

    class FakeModel:
        @classmethod
        def load_model(cls, model_dir, **kwargs):
            calls["loads"] += 1
            return cls()

        def save_speaker(self, prompt, output):
            calls["speakers"] += 1
            output.write_bytes(b"speaker cache")

        def generate(self, **kwargs):
            calls["generations"] += 1
            return np.zeros(240, dtype=np.float32)

        def save_audio(self, audio, output):
            sf.write(output, audio, 24_000, subtype="PCM_16")

    package = ModuleType("mlx_indextts")
    generate = ModuleType("mlx_indextts.generate")
    generate.IndexTTS = FakeModel
    monkeypatch.setitem(sys.modules, "mlx_indextts", package)
    monkeypatch.setitem(sys.modules, "mlx_indextts.generate", generate)

    prompt = tmp_path / "prompt.wav"
    prompt.write_bytes(b"prompt")
    cache = tmp_path / "speaker.npz"
    backend = MLX15Backend(
        model_dir=tmp_path / "model",
        prompt_wav=prompt,
        speaker_cache=cache,
        config=PipelineConfig(),
    )
    backend.synthesize("第一段。", tmp_path / "one.wav", chunk_index=1)
    backend.synthesize("第二段。", tmp_path / "two.wav", chunk_index=2)

    assert calls == {"loads": 1, "speakers": 1, "generations": 2}

    MLX15Backend(
        model_dir=tmp_path / "model",
        prompt_wav=prompt,
        speaker_cache=cache,
        config=PipelineConfig(),
    )
    assert calls["speakers"] == 1
