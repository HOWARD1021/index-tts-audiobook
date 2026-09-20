# Tracker

## Identity

- **Work key:** A-004-mlx-vs-indextts-benchmark.

- **Active Ask:** A-005.

- **Goal:** Record and execute the Issue #8 MLX 1.5 versus IndexTTS-2.5 benchmark plan.

- **Last update:** 2026-09-20 10:35:00 Asia/Taipei.

- **Evidence commit:** uncommitted.

## Overall state

- **State:** active.

- **Reason:** The comparison plan is frozen; no benchmark run has started.

- **Total:** 5.

- **Completed:** 2.

- **Remaining:** 3.

## Accepted task checklist

- [x] **T-1:** Freeze identical preview text/reference inputs, verify both external runtimes and models, record actual Apple Silicon host identity, and keep outputs outside Git; proof requires a PASS/SKIP preflight report. Source: A-005. Proof: preflight.json.
- [x] **T-2:** Prepare the benchmark report schema and metric aggregation at the existing runner seam, with deterministic fake-backend tests and no product-default changes; proof requires focused tests and stable report fields. Source: A-005. Proof: tests/test_benchmark.py and 29 passed / 1 skipped.
- [ ] **T-3:** Run MLX 1.5 pause-only and IndexTTS-2.5 neutral/pause-only, plus optional 2.5 local-emotion diagnostic, with cold and repeated warm measurements; proof requires raw external logs and validated per-run artifacts. Source: A-004.
- [ ] **T-4:** Validate native WAV formats, finite samples, durations, checksums, RTF calculations, headroom observations, and unchanged-input resume; proof requires comparison, validation, and resume reports. Source: A-004.
- [ ] **T-5:** Perform the backend-blind listening gate and record a naturalness-first recommendation, handing emotion decisions to Issue #6 and headroom decisions to Issue #7; proof requires listening.md with timestamped verdicts. Source: A-004.

## Accepted scope changes

- None.

## Current recovery

- **Current item:** T-3.

- **Last proven result:** T-1 PASS; T-2 report schema/aggregation PASS with 29 passed / 1 skipped, compileall and Ruff PASS. Product defaults are unchanged.

- **Active blocker or running process:** None; planning only.

- **Next safe action:** Run MLX 1.5 and IndexTTS-2.5 primary pause-only baselines with cold and repeated warm timing in the external benchmark root.

- **Expected changed files:** `.agentflow/artifacts/A-004-mlx-vs-indextts-benchmark/` and external benchmark artifacts; no product source or canonical manuscript changes expected during preflight.

## Completion proof

- **All accepted tasks checked:** no.

- **Blocking accepted decision:** none.

- **Operation running:** no.

- **Next action remaining:** T-3.

- **Evidence status:** current.

- **Judgment:** active.

## Update meaning

- Saving this tracker is a recovery checkpoint, not a stop signal.

- Work continues with the next unfinished item unless an independent stop condition applies.
