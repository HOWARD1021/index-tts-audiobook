import json

import numpy as np
import pytest
import soundfile as sf

from audiobook_pipeline.config import PipelineConfig
from audiobook_pipeline.runner import render_chapter


class FakeBackend:
    def __init__(self, sample_rate, calls):
        self.sample_rate = sample_rate
        self.calls = calls

    def synthesize(self, text, output, *, chunk_index):
        self.calls.append((chunk_index, text))
        sf.write(
            output, np.zeros(self.sample_rate // 10), self.sample_rate, subtype="PCM_16"
        )


def fixture_inputs(tmp_path):
    script = tmp_path / "chapter.md"
    script.write_text("第一段。\n\n第二段。", encoding="utf-8")
    prompt = tmp_path / "prompt.wav"
    sf.write(prompt, np.zeros(2205), 22_050, subtype="PCM_16")
    model = tmp_path / "external-model"
    return script, prompt, model


def test_mlx_manifest_identity_model_reuse_and_resume(tmp_path):
    script, prompt, model = fixture_inputs(tmp_path)
    output = tmp_path / "chapter.wav"
    factory_calls = []
    synthesis_calls = []

    def factory(backend, **kwargs):
        factory_calls.append((backend, kwargs))
        return FakeBackend(24_000, synthesis_calls)

    render_chapter(
        script,
        output,
        backend="mlx-1.5",
        prompt_wav=prompt,
        model_dir=model,
        config=PipelineConfig(),
        backend_factory=factory,
    )

    manifest = json.loads(output.with_suffix(".manifest.json").read_text())
    assert len(factory_calls) == 1
    assert [call[0] for call in synthesis_calls] == [1, 2]
    assert manifest["backend"] == "mlx-1.5"
    assert manifest["model_dir"] == str(model.resolve())
    assert len(manifest["prompt_sha256"]) == 64
    assert manifest["sampling_parameters"]["seed"] == 42
    assert manifest["output_format"] == {
        "sample_rate": 24_000,
        "channels": 1,
        "subtype": "PCM_16",
    }

    def must_not_load(*args, **kwargs):
        raise AssertionError("a fully resumed run must not load the model")

    render_chapter(
        script,
        output,
        backend="mlx-1.5",
        prompt_wav=prompt,
        model_dir=model,
        config=PipelineConfig(),
        backend_factory=must_not_load,
    )
    resumed = json.loads(output.with_suffix(".manifest.json").read_text())
    assert all(record["reused"] for record in resumed["chunks"])


def test_manifest_identity_change_prevents_stale_chunk_reuse(tmp_path):
    script, prompt, model = fixture_inputs(tmp_path)
    output = tmp_path / "chapter.wav"
    first_calls = []
    second_calls = []

    render_chapter(
        script,
        output,
        backend="mlx-1.5",
        prompt_wav=prompt,
        model_dir=model,
        config=PipelineConfig(),
        backend_factory=lambda *args, **kwargs: FakeBackend(24_000, first_calls),
    )
    prompt.write_bytes(b"a different prompt")
    render_chapter(
        script,
        output,
        backend="mlx-1.5",
        prompt_wav=prompt,
        model_dir=model,
        config=PipelineConfig(),
        backend_factory=lambda *args, **kwargs: FakeBackend(24_000, second_calls),
    )
    assert len(second_calls) == 2


def test_model_change_invalidates_chunks_and_speaker_cache(tmp_path):
    script, prompt, first_model = fixture_inputs(tmp_path)
    output = tmp_path / "chapter.wav"
    speaker_caches = []

    def factory(backend, **kwargs):
        speaker_caches.append(kwargs["speaker_cache"])
        return FakeBackend(24_000, [])

    render_chapter(
        script,
        output,
        backend="mlx-1.5",
        prompt_wav=prompt,
        model_dir=first_model,
        config=PipelineConfig(),
        backend_factory=factory,
    )
    render_chapter(
        script,
        output,
        backend="mlx-1.5",
        prompt_wav=prompt,
        model_dir=tmp_path / "different-model",
        config=PipelineConfig(),
        backend_factory=factory,
    )
    assert len(speaker_caches) == 2
    assert speaker_caches[0] != speaker_caches[1]


def test_indextts_25_default_format_manifest_and_resume(tmp_path):
    script, prompt, _ = fixture_inputs(tmp_path)
    project_root = tmp_path / "indextts-runtime"
    output = tmp_path / "chapter.wav"
    factory_calls = []

    def factory(backend, **kwargs):
        factory_calls.append(backend)
        return FakeBackend(22_050, [])

    render_chapter(
        script,
        output,
        project_root=project_root,
        prompt_wav=prompt,
        config=PipelineConfig(),
        backend_factory=factory,
    )
    manifest = json.loads(output.with_suffix(".manifest.json").read_text())
    assert factory_calls == ["indextts-2.5"]
    assert manifest["runtime_root"] == str(project_root.resolve())
    assert manifest["output_format"]["sample_rate"] == 22_050

    render_chapter(
        script,
        output,
        project_root=project_root,
        prompt_wav=prompt,
        config=PipelineConfig(),
        backend_factory=lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("resumed 2.5 run loaded the model")
        ),
    )


def test_indextts_25_requires_project_root(tmp_path):
    script, prompt, _ = fixture_inputs(tmp_path)
    with pytest.raises(ValueError, match="--project-root is required for indextts-2.5"):
        render_chapter(
            script,
            tmp_path / "chapter.wav",
            prompt_wav=prompt,
            config=PipelineConfig(),
        )


def test_dry_run_does_not_construct_backend_or_write_manifest(tmp_path):
    script, prompt, model = fixture_inputs(tmp_path)
    output = tmp_path / "chapter.wav"

    def must_not_load(*args, **kwargs):
        raise AssertionError("dry-run loaded the model")

    render_chapter(
        script,
        output,
        backend="mlx-1.5",
        prompt_wav=prompt,
        model_dir=model,
        config=PipelineConfig(),
        dry_run=True,
        backend_factory=must_not_load,
    )
    assert not output.exists()
    assert not output.with_suffix(".manifest.json").exists()
