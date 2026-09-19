# Tracker

## Identity

- **Work key:** A-002-execution-plan.

- **Active Ask:** A-002.

- **Goal:** Execute the Issue #5 real IndexTTS-2.5 styled preview with the selected speaker reference and collect objective plus listening evidence.

- **Last update:** 2026-09-20 00:00:00 Asia/Taipei.

- **Evidence commit:** uncommitted.

## Overall state

- **State:** active.

- **Reason:** Execution plan is ready; preview work has not started.

- **Total:** 5.

- **Completed:** 0.

- **Remaining:** 5.

## Accepted task checklist

- [ ] **T-1:** Preflight the IndexTTS-2.5 runtime, checkpoint, MPS device, selected speaker reference, prompt checksum, and isolated output boundary; do not modify source or load the model until every prerequisite is proven. Source: A-002.
- [ ] **T-2:** Prepare an isolated chapter-four preview containing ordinary, bold, italic, pronunciation-override, and cross-chunk emphasis cases; prove the backend text is clean and the expected span metadata/vectors are selected. Source: A-002.
- [ ] **T-3:** Generate the real IndexTTS-2.5 preview with one model session, the selected prompt, deterministic settings, per-span vectors, and inspectable span/join WAVs; keep all private/generated artifacts outside Git. Source: A-002.
- [ ] **T-4:** Validate span and joined WAV format, finite samples, duration, manifest identity, prompt/model/vector metadata, and unchanged-input resume behavior. Source: A-002.
- [ ] **T-5:** Perform and record the human listening gate; pass Issue #5 or hand seam/profile decisions to Issue #6 without changing policy in this ticket. Source: A-002.

## Accepted scope changes

- None.

## Current recovery

- **Current item:** T-1.

- **Last proven result:** The code-level suite has 26 passed and 1 skipped; no real multi-span acoustic preview has run.

- **Active blocker or running process:** None.

- **Next safe action:** Preflight the external IndexTTS-2.5 runtime and selected speaker reference.

- **Expected changed files:** `.agentflow/artifacts/A-002-execution-plan/` and external preview artifacts only; no product source or canonical manuscript changes expected.

## Completion proof

- **All accepted tasks checked:** no.

- **Blocking accepted decision:** none.

- **Operation running:** no.

- **Next action remaining:** T-1.

- **Evidence status:** current.

- **Judgment:** active.

## Update meaning

- Saving this tracker is a recovery checkpoint, not a stop signal.

- Work continues with the next unfinished item unless an independent stop condition applies.
