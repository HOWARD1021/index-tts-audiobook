# MLX IndexTTS 1.5 vs IndexTTS-2.5 benchmark plan

## Problem Statement

The current IndexTTS-2.5 MPS preview is objectively valid, but human
listening found the delivery too excited for audiobook narration. The project
already has an external MLX IndexTTS 1.5 runtime and converted model for Apple
Silicon, but it has not been compared against the current IndexTTS-2.5
runtime using the same narration material, speaker reference, and measured
performance criteria.

The comparison must answer two separate questions:

1. Is MLX IndexTTS 1.5 faster for the same audiobook workload on Apple
   Silicon?
2. Does its pause-only, non-local-emotion path produce a more suitable
   audiobook delivery than the current IndexTTS-2.5 local-emotion path?

The current host reports Apple M4 with 16 GB memory. A result from this host
must not be described as an M3 result. The external MLX source contains
experimental v2 code, but the available converted model is IndexTTS 1.5; no
usable MLX IndexTTS-2.5 model is present in the current workspace.

## Solution

Add a reproducible, opt-in benchmark and listening workflow at the existing
CLI/backend-neutral render seam. The workflow uses the same cleaned preview
text, speaker reference, seed policy, chunking limits, and pause policy where
the two runtimes can support them, then writes a machine-readable comparison
report outside the repository.

The primary comparison has two pause-only runs:

1. MLX IndexTTS 1.5 using the available Apple Silicon model, with no local
   emotion vector and short boundary pauses.
2. IndexTTS-2.5 on MPS using a neutral/no-extra-emotion configuration and the
   same cleaned text and reference.

An optional secondary run uses the current IndexTTS-2.5 local Markdown emotion
path. This isolates the cost and acoustic effect of splitting styled spans
into separate synthesis calls; it is not treated as an apples-to-apples model
comparison with MLX 1.5, because the MLX 1.5 adapter has no local
emotion-vector interface.

The report records hardware identity, runtime and model identity, prompt
checksum, cold model-load time, warm synthesis time, per-chunk time, final
audio duration, real-time factor, output format, peak/headroom observation,
warnings, and human listening notes. Each run gets a distinct output stem and
can resume without regenerating valid artifacts.

The benchmark does not select a default backend automatically. The result is
used to choose a follow-up policy under the user's priorities: audiobook
naturalness first, then speed and operational cost.

## User Stories

1. As an audiobook author, I want to compare MLX IndexTTS 1.5 and
   IndexTTS-2.5 on the same preview passage, so that I can choose a narrator
   runtime using evidence rather than assumptions.
2. As an audiobook author, I want the comparison to use the same speaker
   reference, so that speaker identity does not decide the result accidentally.
3. As an audiobook author, I want the comparison to use the same cleaned
   narration text, so that Markdown cleanup and pronunciation preparation do
   not differ between backends.
4. As an audiobook author, I want a pause-only baseline, so that I can test a
   calm audiobook path without confusing local emotion with ordinary
   narration.
5. As an audiobook author, I want the current IndexTTS-2.5 local-emotion path
   recorded as a secondary run, so that I can separate model speed from the
   cost of per-span rendering.
6. As an audiobook author, I want cold model-load time separated from warm
   generation time, so that startup cost does not hide steady-state speed.
7. As an audiobook author, I want at least repeated warm measurements, so that
   one cache warm-up or scheduling spike does not decide the winner.
8. As an audiobook author, I want real-time factor and wall-clock time
   reported together, so that short and long passages remain comparable.
9. As an audiobook author, I want per-chunk timings, so that a long or failed
   chunk can be diagnosed without rerunning the whole preview.
10. As an audiobook author, I want the report to identify the actual Apple
    Silicon chip and memory, so that an M4 result is not incorrectly presented
    as an M3 result.
11. As an audiobook author, I want runtime commits, model paths, and prompt
    checksums recorded, so that a later benchmark can reproduce the same
    conditions.
12. As an audiobook author, I want the sample-rate and PCM format difference
    between MLX 1.5 and IndexTTS-2.5 made explicit, so that format differences
    are not mistaken for voice-quality differences.
13. As an audiobook author, I want both outputs to be checked for empty,
    malformed, non-finite, or implausibly long audio, so that speed cannot
    reward a broken output.
14. As an audiobook author, I want peak/headroom observations recorded, so
    that possible clipping is not hidden by a successful WAV validation.
15. As an audiobook author, I want the same preview to be listenable in a
    blind-ish order, so that I can judge naturalness without knowing which
    backend produced each file.
16. As an audiobook author, I want to compare speaker continuity, pacing,
    pronunciation, pauses, pitch movement, and audible artifacts, so that a
    faster but tiring narrator is not selected.
17. As an audiobook author, I want the report to state that MLX 1.5 lacks the
    current local emotion-vector interface, so that a capability difference is
    not mistaken for a failed benchmark.
18. As an audiobook author, I want a clear result when a real external runtime
    or model is unavailable, so that a skipped benchmark is not reported as a
    speed win or loss.
19. As an audiobook author, I want interrupted benchmark runs to resume valid
    chunks, so that expensive Apple Silicon generation is not discarded.
20. As an audiobook author, I want prior outputs protected from overwrite, so
    that a new backend or policy cannot destroy an earlier listening reference.
21. As an audiobook author, I want benchmark artifacts outside the repository,
    so that private prompts, model files, and generated audio are not committed.
22. As an audiobook author, I want the benchmark to leave the default backend
    and emotion presets unchanged, so that measurement does not silently become
    a product behavior change.
23. As an audiobook author, I want the comparison to identify when the MLX
    model is faster but acoustically worse, so that speed alone cannot close
    the decision.
24. As an audiobook author, I want the comparison to identify when MLX 1.5 is
    both faster and calmer, so that it can become a deliberate follow-up
    candidate for pause-only audiobook narration.
25. As an audiobook author, I want a follow-up recommendation tied to the
    recorded evidence, so that Issue #6 can choose a restrained emotion policy
    or pause-only policy without repeating the entire investigation.

## Implementation Decisions

- Reuse the existing CLI render entry point, backend selection, canonical
  narration preparation, chunk planner, manifest identity, WAV validator, and
  resumable chunk workspace. Add benchmark orchestration at the highest seam
  that already owns these concerns; do not add timing logic separately inside
  each model implementation unless an existing backend API cannot expose a
  required measurement.
- Keep the two runtime adapters independent. MLX IndexTTS 1.5 remains an
  external runtime with its converted model; IndexTTS-2.5 remains the external
  PyTorch/MPS checkout. Do not port IndexTTS-2.5 to MLX as part of this work.
- Use the same cleaned Simplified-Chinese preview passage and the same
  speaker-reference WAV for the primary runs. Record the prompt checksum and
  source-text checksum in every report.
- Define the primary baseline as pause-only narration. For IndexTTS-2.5,
  neutral means no additional local emotion profile. For MLX 1.5, neutral is
  the supported path because the current adapter has no local emotion-vector
  interface.
- Treat the current IndexTTS-2.5 bold/italic vector path as a secondary
  diagnostic run. Its per-span synthesis count and local span pause must be
  visible in the report so that segmentation overhead is not attributed to
  the emotion-vector arithmetic alone.
- Measure cold load separately from warm generation. Run one cold measurement
  and at least three warm measurements per backend, report median and spread,
  and keep the raw per-run records. If the external runtime cannot provide a
  valid run, report SKIP with the exact prerequisite failure.
- Use `use_random=false`, a fixed seed where supported, FP32/MPS settings for
  IndexTTS-2.5, and the documented MLX settings for IndexTTS 1.5. Record all
  settings rather than assuming cross-runtime bit identity.
- Report real-time factor as elapsed synthesis wall time divided by generated
  audio duration. Report model-load time separately and do not include it in
  warm RTF. Include output sample rate because MLX 1.5 and IndexTTS-2.5 use
  different native rates.
- Preserve the existing output-boundary rule: prompts, checkpoints, caches,
  manifests, WAVs, and benchmark reports remain outside Git unless a small
  sanitized fixture is needed for tests.
- Do not change the default narrator, emotion vectors, chunk size, local pause
  policy, or backend selection based on benchmark output. A separate Issue #6
  decision is required for any user-visible policy change.
- Treat the Apple Silicon chip identity as a required report field. Results
  from the current M4 host are labelled M4; an M3 run is only claimed when it
  was actually executed on M3 hardware.
- Preserve the existing artifact identity and resume behavior. A benchmark
  rerun with unchanged backend, model, prompt, text, and settings must reuse
  valid chunks; a changed identity must create a new output stem.

## Testing Decisions

- Tests should assert externally visible benchmark behavior: stable report
  fields, correct backend/model/prompt identity, timing aggregation, RTF
  calculation, output-format validation, skip reasons, and resume decisions.
  They should not assert private model-layer calls or implementation-specific
  tensor shapes.
- Extend the existing backend and runner unit-test seams to cover benchmark
  identity, warm/cold timing records, neutral versus styled run metadata,
  sample-rate reporting, and unchanged-input reuse.
- Use the current fake-backend tests as prior art for deterministic orchestration
  tests. The current backend tests already verify one MLX model load and speaker
  conditioning reuse; preserve that contract.
- Add a report-level test using synthetic timing records to verify median,
  spread, RTF, and model-load separation without loading either external model.
- Keep real MLX and real IndexTTS-2.5 tests opt-in. The existing MLX smoke-test
  pattern is the precedent: missing runtime, missing model, or missing prompt
  must produce an explicit skip, never a false pass.
- Add one opt-in end-to-end benchmark scenario on the actual Apple Silicon
  host. It must produce validated WAVs, manifest identity, raw timing records,
  and a human-listening checklist for both primary runs.
- Require a manual listening record for speaker continuity, perceived pacing,
  pause naturalness, pronunciation, vocal fatigue, artifacts, and clipping.
  A faster run fails acceptance if it is less suitable for audiobook narration.
- Run the complete existing test suite plus focused benchmark tests before
  publishing a result. Do not treat the upstream README's RTF claim as local
  benchmark evidence.

## Out of Scope

- Porting IndexTTS-2.5 or its checkpoints to MLX.
- Installing or converting a new MLX IndexTTS-2.0/2.5 model as part of the
  first comparison.
- Adding local Markdown emotion-vector support to the MLX 1.5 adapter.
- Choosing or changing the final audiobook emotion policy; that belongs to
  Issue #6.
- Making MLX 1.5 the default backend automatically.
- Generating a full chapter or full book before the short comparison passes.
- Purchasing hardware, claiming M3 performance from an M4 run, or running a
  remote benchmark without recording the actual host.
- Solving peak/headroom or clipping policy; that belongs to Issue #7, although
  the benchmark must expose the measurements.
- Rewriting the canonical manuscript or changing pronunciation policy.

## Further Notes

- The current local MLX workspace already contains a generated 24 kHz test
  audiobook, but its report does not contain reliable wall-clock timing. It is
  useful as a runtime-presence check, not as a speed comparison.
- The current IndexTTS-2.5 preview used nine synthesis calls because local
  styles were rendered separately. A pause-only comparison must report call
  count so that this architectural overhead is visible.
- A likely decision rule is: prefer the backend that passes human audiobook
  listening and produces acceptable headroom; among those, prefer the lower
  median warm RTF and simpler operational path. This is a recommendation for
  Issue #6, not an automatic acceptance rule in the benchmark implementation.
