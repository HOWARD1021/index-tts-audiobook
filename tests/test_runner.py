import json

import numpy as np
import pytest
import soundfile as sf

from audiobook_pipeline.config import PipelineConfig
from audiobook_pipeline.runner import plan_chapter, render_chapter


class FakeBackend:
    def __init__(self, sample_rate, calls):
        self.sample_rate = sample_rate
        self.calls = calls

    def synthesize(
        self,
        text,
        output,
        *,
        chunk_index,
        emotion_vector=None,
        emotion_alpha=None,
    ):
        self.calls.append(
            (chunk_index, text, emotion_vector, emotion_alpha)
        )
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


def test_render_prepares_source_markdown_before_synthesis(tmp_path):
    script = tmp_path / "raw-chapter.md"
    script.write_text(
        "價格的小幅上漲是由**巨大的成交量**產生的，伴隨著『震盪』。",
        encoding="utf-8",
    )
    prompt = tmp_path / "prompt.wav"
    sf.write(prompt, np.zeros(2205), 22_050, subtype="PCM_16")
    calls = []

    render_chapter(
        script,
        tmp_path / "chapter.wav",
        prompt_wav=prompt,
        project_root=tmp_path / "indextts-runtime",
        config=PipelineConfig(),
        backend_factory=lambda *args, **kwargs: FakeBackend(22_050, calls),
    )

    assert [call[1] for call in calls] == [
        "价格的小幅上涨是由",
        "巨大的成交量",
        "产生的，伴随着震荡。",
    ]


def test_render_applies_local_emotion_to_markdown_emphasis(tmp_path):
    script = tmp_path / "raw-chapter.md"
    script.write_text(
        "價格的小幅上漲是由**巨大的成交量**產生的。",
        encoding="utf-8",
    )
    prompt = tmp_path / "prompt.wav"
    sf.write(prompt, np.zeros(2205), 22_050, subtype="PCM_16")
    calls = []
    config = PipelineConfig()

    render_chapter(
        script,
        tmp_path / "chapter.wav",
        prompt_wav=prompt,
        project_root=tmp_path / "indextts-runtime",
        config=config,
        backend_factory=lambda *args, **kwargs: FakeBackend(22_050, calls),
    )

    assert [call[1] for call in calls] == [
        "价格的小幅上涨是由",
        "巨大的成交量",
        "产生的。",
    ]
    assert calls[0][2] == config.emotion.vector
    assert calls[1][2] == config.emotion.bold_vector
    assert calls[2][2] == config.emotion.vector


def test_short_emphasis_falls_back_to_sentence_context(tmp_path):
    script = tmp_path / "short-emphasis.md"
    script.write_text("这是一段**不是**普通文字。", encoding="utf-8")
    prompt = tmp_path / "prompt.wav"
    sf.write(prompt, np.zeros(2205), 22_050, subtype="PCM_16")
    calls = []
    config = PipelineConfig(min_emphasis_characters=3)

    render_chapter(
        script,
        tmp_path / "chapter.wav",
        prompt_wav=prompt,
        project_root=tmp_path / "indextts-runtime",
        config=config,
        backend_factory=lambda *args, **kwargs: FakeBackend(22_050, calls),
    )

    assert len(calls) == 1
    assert calls[0][1] == "这是一段不是普通文字。"
    assert calls[0][2] == config.emotion.vector


def test_neutral_styled_spans_render_once_without_local_emotion(tmp_path):
    script = tmp_path / "neutral-styled.md"
    script.write_text(
        "價格的小幅上漲是由**巨大的成交量**產生的。",
        encoding="utf-8",
    )
    prompt = tmp_path / "prompt.wav"
    sf.write(prompt, np.zeros(2205), 22_050, subtype="PCM_16")
    calls = []
    config = PipelineConfig(render_local_emotion=False)

    render_chapter(
        script,
        tmp_path / "chapter.wav",
        prompt_wav=prompt,
        project_root=tmp_path / "indextts-runtime",
        config=config,
        backend_factory=lambda *args, **kwargs: FakeBackend(22_050, calls),
    )

    assert len(calls) == 1
    assert calls[0][1] == "价格的小幅上涨是由巨大的成交量产生的。"
    assert calls[0][2] == config.emotion.vector


def test_plan_handles_emphasis_that_crosses_chunk_boundaries(tmp_path):
    script = tmp_path / "long-emphasis.md"
    emphasized = "很長的強調文字" * 20
    script.write_text(f"**{emphasized}**", encoding="utf-8")

    chunks = plan_chapter(script, PipelineConfig(max_chunk_chars=20))

    assert "".join(chunk["text"] for chunk in chunks) == "很长的强调文字" * 20


def test_mlx_render_rejects_local_emotion_until_backend_supports_it(tmp_path):
    script = tmp_path / "styled.md"
    script.write_text("普通文字**強調文字**。", encoding="utf-8")
    prompt = tmp_path / "prompt.wav"
    sf.write(prompt, np.zeros(2205), 22_050, subtype="PCM_16")

    with pytest.raises(ValueError, match="local Markdown emotion requires"):
        render_chapter(
            script,
            tmp_path / "chapter.wav",
            backend="mlx-1.5",
            prompt_wav=prompt,
            model_dir=tmp_path / "model",
            config=PipelineConfig(),
            backend_factory=lambda *args, **kwargs: FakeBackend(24_000, []),
        )
