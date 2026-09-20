# Tracker

## Identity

- **Work key:** A-004-mlx-vs-indextts-benchmark.

- **Active Ask:** A-005.

- **Goal:** Record and execute the Issue #8 MLX 1.5 versus IndexTTS-2.5 benchmark plan.

- **Last update:** 2026-09-20 16:53:00 Asia/Taipei.

- **Evidence commit:** 889d27829dcf5a6103663800786f1370d4287352.

## Overall state

- **State:** complete.

- **Reason:** Primary comparison, objective validation, resume evidence, and human listening are complete; pronunciation follow-up is handed to a separate issue.

- **Total:** 5.

- **Completed:** 5.

- **Remaining:** 0.

## Accepted task checklist

- [x] **T-1:** Freeze identical preview text/reference inputs, verify both external runtimes and models, record actual Apple Silicon host identity, and keep outputs outside Git; proof requires a PASS/SKIP preflight report. Source: A-005. Proof: preflight.json.
- [x] **T-2:** Prepare the benchmark report schema and metric aggregation at the existing runner seam, with deterministic fake-backend tests and no product-default changes; proof requires focused tests and stable report fields. Source: A-005. Proof: tests/test_benchmark.py and 31 passed / 1 skipped.
- [x] **T-3:** Run MLX 1.5 pause-only and IndexTTS-2.5 neutral/pause-only, plus optional 2.5 local-emotion diagnostic, with cold and repeated warm measurements; proof requires raw external logs and validated per-run artifacts. Source: A-005. Proof: comparison-report.json and backend reports.
- [x] **T-4:** Validate native WAV formats, finite samples, durations, checksums, RTF calculations, headroom observations, and unchanged-input resume; proof requires comparison, validation, and resume reports. Source: A-005. Proof: objective-validation.json and resume-validation.json.
- [x] **T-5:** Perform the backend-blind listening gate and record a naturalness-first recommendation, handing emotion decisions to Issue #6 and headroom decisions to Issue #7; proof requires listening.md with timestamped verdicts. Source: A-005. Proof: listening.md.

## Accepted scope changes

- None.

## Current recovery

- **Current item:** none.

- **Last proven result:** Yuanyuan human listening prefers IndexTTS-2.5 for smoother delivery and fewer wrong characters; `伴隨著` pronunciation remains wrong and is a follow-up requirement.

- **Active blocker or running process:** None.

- **Next safe action:** None.

- **Expected changed files:** `.agentflow/artifacts/A-004-mlx-vs-indextts-benchmark/` and external benchmark artifacts; no product source or canonical manuscript changes expected during preflight.

## Completion proof

- **All accepted tasks checked:** yes.

- **Blocking accepted decision:** none.

- **Operation running:** no.

- **Next action remaining:** none.

- **Evidence status:** complete.

- **Judgment:** complete.

## Update meaning

- Saving this tracker is a recovery checkpoint, not a stop signal.

- Work continues with the next unfinished item unless an independent stop condition applies.
