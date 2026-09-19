* _2026-09-20 00:00:00 (gpt-5.4/high)_

# Execution plan — Issue #5 styled IndexTTS-2.5 preview

## Goal

Produce one repeatable, real-model preview that proves the current local-emotion
pipeline with the selected speaker reference, without committing private audio,
prompts, checkpoints, or source manuscripts.

## Scope boundary

In scope:

- The chapter-four test passage already used in the conversation.
- One ordinary span, one bold span, one italic span, the `伴隨著` pronunciation
  override, and one emphasis span long enough to cross a chunk boundary.
- IndexTTS-2.5 on MPS with the existing external runtime and reference WAV.
- Clean narration text, per-span emotion vectors, manifest identity, WAV
  validation, and a listening note.

Out of scope:

- Changing the base/bold/italic emotion profiles.
- Choosing phrase-level versus sentence-level emphasis policy; that is Issue #6.
- Building the final release gate; that is Issue #7.
- Full chapter or full-book generation.

## Steps

1. **Preflight the real inputs**
   - Confirm the IndexTTS-2.5 runtime contains `infer_v2_5.py` and the model
     checkpoint configuration.
   - Confirm the selected speaker reference WAV exists and record its SHA-256.
   - Confirm MPS availability, FP32/MPS fallback settings, and no stale model
     process is holding the device.
   - Confirm the output directory is outside Git-tracked source and audio paths.

2. **Prepare an isolated preview script**
   - Extract the agreed chapter-four passage without editing the canonical
     manuscript.
   - Add one short italic marker and one deliberately long emphasis marker only
     in the isolated preview copy if the source passage lacks them.
   - Run the canonical preparation path and inspect the resulting spans:
     ordinary text uses the base vector, bold uses `bold_vector`, italic uses
     `italic_vector`, and `伴隨著` retains `ZHE5`.
   - Confirm no Markdown delimiters, spoken brackets, or cue markers remain in
     backend text.

3. **Generate the real preview**
   - Use backend `indextts-2.5`, the selected speaker reference, `use_random=false`,
     and the configured base/bold/italic vectors.
   - Reuse one loaded model session while rendering the styled spans.
   - Keep each span and the joined chunk available for inspection.
   - Record the exact command settings, model path, prompt path/checksum, vectors,
     alpha values, local pause, device, and runtime warnings.

4. **Run objective validation**
   - Confirm every span WAV and the joined preview are non-empty mono PCM16 at
     22,050 Hz.
   - Confirm all samples are finite and duration sanity checks pass.
   - Confirm the manifest records clean text identity, styled-source identity,
     prompt checksum, model/runtime identity, vectors, and final WAV checksum.
   - Confirm a rerun with unchanged inputs reuses valid artifacts rather than
     regenerating them.

5. **Perform the listening gate**
   - Listen for speaker identity continuity across ordinary, bold, and italic
     spans.
   - Listen for the intended `伴隨著` pronunciation.
   - Listen for Markdown/bracket/cue leakage.
   - Listen for unnatural seams, excessive pauses, abrupt pitch changes, or
     emotion that is too weak or too aggressive.
   - Record pass/fail evidence and stop without changing presets if the result
     requires a policy decision for Issue #6.

## Acceptance evidence

- Prepared preview text and span metadata inspection.
- Real IndexTTS-2.5 generation log with selected prompt and vector settings.
- `ffprobe` and finite-sample validation output.
- Manifest and resume evidence.
- Human listening note with explicit results for pronunciation, cleanup, local
  emotion, speaker continuity, and joins.

## Safe stopping points

- Stop before model load if runtime, checkpoint, prompt, or MPS preflight fails.
- Stop after objective validation if the preview needs an emotion-policy choice;
  hand the decision to Issue #6.
- Do not silently alter source text, profiles, or backend behavior during this
  ticket.

## Completion condition

Issue #5 is complete only when the real preview is generated with the selected
speaker reference, all objective checks pass, the manifest is internally
consistent, and the listening note is recorded. A failed listening gate is valid
evidence for Issue #6, not a reason to force a pass.

Self-check: plan is limited to Issue #5 and preserves #6/#7 as downstream gates.
