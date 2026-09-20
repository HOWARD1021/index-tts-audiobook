# Execution plan — MLX IndexTTS 1.5 vs IndexTTS-2.5 benchmark

## Goal

Produce a reproducible comparison of the available MLX IndexTTS 1.5 runtime
and the IndexTTS-2.5 PyTorch/MPS runtime for audiobook narration. Establish
whether MLX is faster on the actual Apple Silicon host and whether its
pause-only path is more suitable than the current excited local-emotion path.

## Frozen source of truth

- GitHub Issue: #8, `Benchmark MLX IndexTTS 1.5 against IndexTTS-2.5 on Apple Silicon`.
- Spec commit: `420aabf`.
- Existing Issue #5 preview and listening result: current IndexTTS-2.5 local-emotion delivery is too excited for audiobook narration.
- Current host identity must be recorded from the benchmark host. Existing inspection reports Apple M4 / 16 GB; do not label it M3.

## Scope boundary

In scope:

- One fixed cleaned Simplified-Chinese preview passage and one identical speaker reference.
- MLX IndexTTS 1.5 pause-only primary run.
- IndexTTS-2.5 MPS neutral/pause-only primary run.
- Optional IndexTTS-2.5 local-emotion secondary diagnostic run.
- Cold load and repeated warm synthesis timing, per-chunk timing, audio duration, RTF, format, checksums, warnings, resume, and human listening.
- A comparison report and recommendation that remain external to the repository for private runtime/audio artifacts.

Out of scope:

- Porting IndexTTS-2.5 to MLX or obtaining a new MLX 2.0/2.5 model.
- Adding local emotion-vector support to MLX 1.5.
- Changing default backend, emotion profiles, chunk policy, or audiobook product behavior.
- Full chapter/book generation, hardware purchasing, or claiming M3 performance from an M4 host.
- Resolving peak/headroom policy owned by Issue #7.

## Seams

Use the existing CLI render entry point and backend-neutral runner as the
highest seam. Reuse canonical narration preparation, chunk planning, manifest
identity, WAV validation, concatenation, and resume. Add benchmark timing and
report aggregation around that seam; do not add model-specific timing code
unless an adapter cannot expose a required measurement.

## Tasks

1. **Freeze benchmark inputs and preflight**
   - Select the fixed preview text and the same reference WAV for both primary runs.
   - Verify MLX 1.5 model/runtime and IndexTTS-2.5 runtime/checkpoint availability.
   - Record actual chip, memory, OS/runtime commits, model identity, prompt checksum, and output boundary.
   - Proof: preflight report with explicit PASS/SKIP reasons and no generated artifacts in Git.

2. **Implement or prepare benchmark report orchestration**
   - Define externally visible report fields for cold load, warm runs, per-chunk timings, RTF, duration, format, checksums, warnings, call count, and resume.
   - Reuse existing fake-backend seams for deterministic metric and identity tests.
   - Keep the current product defaults unchanged.
   - Proof: focused report/runner tests pass; schema and aggregation behavior are deterministic.

3. **Run the real primary and secondary comparisons**
   - Run MLX 1.5 pause-only and IndexTTS-2.5 neutral/pause-only with the same cleaned text, prompt, chunk limits, and seed policy where supported.
   - Optionally run current IndexTTS-2.5 local emotion to expose per-span segmentation overhead.
   - Perform one cold run and at least three warm runs per available backend; preserve raw logs and distinct output stems.
   - Proof: external run records, validated WAVs, manifest identities, and no silent fallback between model families.

4. **Validate objective metrics and resume**
   - Validate mono PCM16 WAVs, native sample rates, finite samples, duration sanity, peak/headroom observations, and final checksums.
   - Calculate median/spread warm RTF separately from cold model-load time.
   - Rerun unchanged inputs and prove valid chunks are reused without synthesis.
   - Proof: comparison report, validation report, resume report, and complete relevant test suite.

5. **Perform listening gate and hand off the decision**
   - Listen in a backend-blind order for speaker identity, pacing, pauses, pronunciation, vocal fatigue, artifacts, and clipping.
   - Record whether the faster backend is also suitable for audiobook narration.
   - Hand emotion-policy choices to Issue #6 and headroom choices to Issue #7; do not change presets in this benchmark ticket.
   - Proof: listening note with timestamps, PASS/FAIL per criterion, recommendation, and unresolved limits.

## Acceptance evidence

- Frozen input and runtime preflight.
- Focused tests plus complete existing suite.
- Raw cold/warm timing records and calculated RTF.
- Native-format WAV, finite-sample, duration, checksum, and resume evidence.
- Explicit capability note that MLX 1.5 has no local emotion-vector interface.
- Human listening note and recommendation that prioritizes audiobook naturalness before speed.

## Safe stopping points

- Stop before model load if either required runtime, model, prompt, or host identity is unavailable.
- Mark a backend SKIP when its external prerequisite is missing; never treat SKIP as a speed result.
- Stop after objective validation if the two outputs require an Issue #6 policy decision.
- Do not silently modify product defaults, source manuscripts, presets, model files, prompts, or generated audio already used as evidence.

## Completion condition

The benchmark plan is complete only when both primary backends have either a
valid measured run or an explicit prerequisite SKIP, the report is internally
consistent, resume behavior is proven, and the listening recommendation is
recorded. Completion does not automatically select a default backend.

Self-check: plan is limited to Issue #8 comparison evidence and preserves Issue #6 emotion policy and Issue #7 headroom policy as downstream decisions.
