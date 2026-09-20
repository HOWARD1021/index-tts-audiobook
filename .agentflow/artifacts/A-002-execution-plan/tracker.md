# Tracker

## Identity

- **Work key:** A-002-execution-plan.

- **Active Ask:** A-002.

- **Goal:** Execute the Issue #5 real IndexTTS-2.5 styled preview with the selected speaker reference and collect objective plus listening evidence.

- **Last update:** 2026-09-20 08:57:34 Asia/Taipei.

- **Evidence commit:** uncommitted.

## Overall state

- **State:** active.

- **Reason:** Preflight and isolated preparation pass; starting real render.

- **Total:** 5.

- **Completed:** 2.

- **Remaining:** 3.

## Accepted task checklist

- [x] **T-1:** Preflight the IndexTTS-2.5 runtime, checkpoint, MPS device, selected speaker reference, prompt checksum, and isolated output boundary; do not modify source or load the model until every prerequisite is proven. Source: A-002. Proof: preflight.json.
- [x] **T-2:** Prepare an isolated chapter-four preview containing ordinary, bold, italic, pronunciation-override, and cross-chunk emphasis cases; prove the backend text is clean and the expected span metadata/vectors are selected. Source: A-002. Proof: preflight.json.
- [ ] **T-3:** Generate the real IndexTTS-2.5 preview with one model session, the selected prompt, deterministic settings, per-span vectors, and inspectable span/join WAVs; keep all private/generated artifacts outside Git. Source: A-002.
- [ ] **T-4:** Validate span and joined WAV format, finite samples, duration, manifest identity, prompt/model/vector metadata, and unchanged-input resume behavior. Source: A-002.
- [ ] **T-5:** Perform and record the human listening gate; pass Issue #5 or hand seam/profile decisions to Issue #6 without changing policy in this ticket. Source: A-002.

## Accepted scope changes

- None.

## Current recovery

- **Current item:** T-3.

- **Last proven result:** MPS allocation and runtime imports pass; reference checksum recorded; isolated preview has 4 chunks / 9 spans with base, bold, italic, ZHE5, and bold state across chunks.

- **Active blocker or running process:** Real render session 99754 is running in issue-5-20260920-v3; first of nine spans validated.

- **Next safe action:** Render using external run-preview.py, then validate WAVs and resume.

- **Expected changed files:** `.agentflow/artifacts/A-002-execution-plan/` and external preview artifacts only; no product source or canonical manuscript changes expected.

## Completion proof

- **All accepted tasks checked:** no.

- **Blocking accepted decision:** none.

- **Operation running:** yes.

- **Next action remaining:** T-3.

- **Evidence status:** current.

- **Judgment:** active.

## Update meaning

- Saving this tracker is a recovery checkpoint, not a stop signal.

- Work continues with the next unfinished item unless an independent stop condition applies.
