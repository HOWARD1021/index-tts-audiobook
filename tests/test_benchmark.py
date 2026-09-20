import json

import pytest

from audiobook_pipeline.benchmark import (
    BenchmarkRun,
    build_benchmark_report,
    summarize_runs,
    write_benchmark_report,
)


def run(kind, index, wall, duration, *, load=0.0):
    return BenchmarkRun(
        backend="mlx-1.5",
        run_kind=kind,
        run_index=index,
        wall_seconds=wall,
        audio_duration_seconds=duration,
        model_load_seconds=load,
        chunk_count=2,
        synthesis_calls=2,
    )


def test_summarize_runs_separates_cold_load_and_warm_rtf():
    summary = summarize_runs(
        [
            run("cold", 1, 12.0, 4.0, load=5.0),
            run("warm", 1, 4.0, 4.0),
            run("warm", 2, 5.0, 4.0),
            run("warm", 3, 3.0, 4.0),
        ]
    )

    assert summary == {
        "run_count": 4,
        "cold_load_seconds": [5.0],
        "warm_rtf": {"median": 1.0, "minimum": 0.75, "maximum": 1.25, "spread": 0.5},
        "warm_run_count": 3,
    }


def test_report_contains_identity_runs_and_summary(tmp_path):
    runs = [run("warm", 1, 4.0, 2.0)]
    report = build_benchmark_report(
        benchmark_id="issue-8-preview",
        hardware={"chip": "Apple M4", "memory_gb": 16},
        identity={"script_sha256": "script", "prompt_sha256": "prompt"},
        runs=runs,
        capability_notes=["MLX 1.5 has no local emotion-vector interface"],
    )

    path = tmp_path / "comparison.json"
    write_benchmark_report(path, report)
    loaded = json.loads(path.read_text())
    assert loaded["schema_version"] == 1
    assert loaded["benchmark_id"] == "issue-8-preview"
    assert loaded["hardware"]["chip"] == "Apple M4"
    assert loaded["runs"][0]["backend"] == "mlx-1.5"
    assert loaded["summaries"]["mlx-1.5"]["warm_run_count"] == 1
    assert loaded["capability_notes"] == [
        "MLX 1.5 has no local emotion-vector interface"
    ]


def test_timing_records_reject_invalid_values():
    with pytest.raises(ValueError, match="wall_seconds"):
        run("warm", 1, -1.0, 2.0)
    with pytest.raises(ValueError, match="audio_duration_seconds"):
        run("warm", 1, 1.0, 0.0)
    with pytest.raises(ValueError, match="run_kind"):
        run("hot", 1, 1.0, 2.0)
