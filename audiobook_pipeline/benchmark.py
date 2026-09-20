"""Pure timing and report aggregation for cross-backend benchmarks."""

from __future__ import annotations

import json
import math
import os
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import median
from typing import Any


@dataclass(frozen=True)
class ChunkTiming:
    """Timing and audio duration for one rendered chunk."""

    index: int
    characters: int
    wall_seconds: float
    audio_duration_seconds: float

    def __post_init__(self) -> None:
        if self.index < 1:
            raise ValueError("chunk index must be positive")
        if self.characters < 1:
            raise ValueError("chunk characters must be positive")
        for name in ("wall_seconds", "audio_duration_seconds"):
            value = getattr(self, name)
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f"chunk {name} must be finite and positive")


@dataclass(frozen=True)
class BenchmarkRun:
    """One externally measured cold or warm backend run."""

    backend: str
    run_kind: str
    run_index: int
    wall_seconds: float
    audio_duration_seconds: float
    model_load_seconds: float = 0.0
    chunk_count: int = 0
    synthesis_calls: int = 0
    chunk_timings: tuple[ChunkTiming, ...] = ()

    def __post_init__(self) -> None:
        if not self.backend.strip():
            raise ValueError("backend must be non-empty")
        if self.run_kind not in {"cold", "warm"}:
            raise ValueError("run_kind must be 'cold' or 'warm'")
        if self.run_index < 1:
            raise ValueError("run_index must be positive")
        for name in ("wall_seconds", "audio_duration_seconds", "model_load_seconds"):
            value = getattr(self, name)
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and non-negative")
        if self.audio_duration_seconds <= 0:
            raise ValueError("audio_duration_seconds must be positive")
        for name in ("chunk_count", "synthesis_calls"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be non-negative")
        if self.chunk_timings and len(self.chunk_timings) != self.chunk_count:
            raise ValueError("chunk_timings must match chunk_count")

    @property
    def rtf(self) -> float:
        """Elapsed synthesis wall time divided by generated audio duration."""

        return self.wall_seconds / self.audio_duration_seconds

    def as_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["chunk_timings"] = [asdict(timing) for timing in self.chunk_timings]
        result["rtf"] = self.rtf
        return result


def summarize_runs(runs: Iterable[BenchmarkRun]) -> dict[str, Any]:
    """Return stable cold-load and warm-RTF aggregates for one backend."""

    records = list(runs)
    cold = [run for run in records if run.run_kind == "cold"]
    warm = [run for run in records if run.run_kind == "warm"]
    warm_rtf = [run.rtf for run in warm]
    if warm_rtf:
        minimum = min(warm_rtf)
        maximum = max(warm_rtf)
        warm_summary: dict[str, float] | None = {
            "median": median(warm_rtf),
            "minimum": minimum,
            "maximum": maximum,
            "spread": maximum - minimum,
        }
    else:
        warm_summary = None
    return {
        "run_count": len(records),
        "cold_load_seconds": [run.model_load_seconds for run in cold],
        "warm_rtf": warm_summary,
        "warm_run_count": len(warm),
    }


def build_benchmark_report(
    *,
    benchmark_id: str,
    hardware: dict[str, Any],
    identity: dict[str, Any],
    runs: Iterable[BenchmarkRun],
    capability_notes: list[str] | None = None,
) -> dict[str, Any]:
    """Build a JSON-safe comparison report without touching runtime state."""

    run_list = list(runs)
    grouped: dict[str, list[BenchmarkRun]] = {}
    for run in run_list:
        grouped.setdefault(run.backend, []).append(run)
    return {
        "schema_version": 1,
        "benchmark_id": benchmark_id,
        "hardware": dict(hardware),
        "identity": dict(identity),
        "runs": [run.as_dict() for run in run_list],
        "summaries": {
            backend: summarize_runs(backend_runs)
            for backend, backend_runs in sorted(grouped.items())
        },
        "capability_notes": list(capability_notes or []),
    }


def write_benchmark_report(path: str | Path, report: dict[str, Any]) -> None:
    """Atomically write one benchmark report for resumable inspection."""

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_name(f"{destination.name}.partial")
    partial.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(partial, destination)
