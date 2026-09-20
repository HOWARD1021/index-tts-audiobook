# Tracker

## Identity

- **Work key:** A-002-execution-plan.

- **Active Ask:** A-002.

- **Goal:** Execute the Issue #5 real IndexTTS-2.5 styled preview with the selected speaker reference and collect objective plus listening evidence.

- **Last update:** 2026-09-20 09:11:41 Asia/Taipei.

- **Evidence commit:** uncommitted.

## Overall state

- **State:** blocked.

- **Reason:** T-1 through T-4 pass; T-5 needs a human listening verdict, including potential clipping.

- **Total:** 5.

- **Completed:** 4.

- **Remaining:** 1.

## Accepted task checklist

- [x] **T-1:** Preflight the IndexTTS-2.5 runtime, checkpoint, MPS device, selected speaker reference, prompt checksum, and isolated output boundary; do not modify source or load the model until every prerequisite is proven. Source: A-002. Proof: preflight.json.
- [x] **T-2:** Prepare an isolated chapter-four preview containing ordinary, bold, italic, pronunciation-override, and cross-chunk emphasis cases; prove the backend text is clean and the expected span metadata/vectors are selected. Source: A-002. Proof: preflight.json.
- [x] **T-3:** Generate the real IndexTTS-2.5 preview with one model session, the selected prompt, deterministic settings, per-span vectors, and inspectable span/join WAVs; keep all private/generated artifacts outside Git. Source: A-002. Proof: validation.json.
- [x] **T-4:** Validate span and joined WAV format, finite samples, duration, manifest identity, prompt/model/vector metadata, and unchanged-input resume behavior. Source: A-002. Proof: validation.json.
- [ ] **T-5:** Perform and record the human listening gate; pass Issue #5 or hand seam/profile decisions to Issue #6 without changing policy in this ticket. Source: A-002.

## Accepted scope changes

- None.

## Current recovery

- **Current item:** T-5.

- **Last proven result:** 67.3579-second preview; 14 WAVs and manifest pass; one model session / nine syntheses; resume loads zero models and reuses four chunks; final checksum unchanged.

- **Active blocker or running process:** No render running; human listening verdict pending. Potential clipping: 2.2701% of samples at amplitude rails.

- **Next safe action:** Listen to preview.wav using listening.md, record verdict, and hand acoustic policy findings to Issue #6 if needed.

- **Expected changed files:** `.agentflow/artifacts/A-002-execution-plan/` and external preview artifacts only; no product source or canonical manuscript changes expected.

## Completion proof

- **All accepted tasks checked:** no.

- **Blocking accepted decision:** Human listening verdict required by T-5.

- **Operation running:** no.

- **Next action remaining:** T-5.

- **Evidence status:** current.

- **Judgment:** blocked.

## Update meaning

- Saving this tracker is a recovery checkpoint, not a stop signal.

- Work continues with the next unfinished item unless an independent stop condition applies.
