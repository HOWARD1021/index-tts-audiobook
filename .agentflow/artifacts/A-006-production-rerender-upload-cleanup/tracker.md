# Tracker

## Identity

- **Work key:** A-006-production-rerender-upload-cleanup.

- **Active Ask:** A-011.

- **Goal:** Plan and execute the verified Yuanyuan/IndexTTS-2.5 production rerender, original-destination publication, and allowlisted test cleanup.

- **Last update:** 2026-09-20 20:20:00 Asia/Taipei.

- **Evidence commit:** uncommitted.

## Overall state

- **State:** active.

- **Reason:** Production rerender and publication plan is recorded; destination and accepted pronunciation form are not yet frozen.

- **Total:** 5.

- **Completed:** 1.

- **Remaining:** 4.

## Accepted task checklist

- [x] **T-1:** Resolve and freeze source scripts, production output list, Yuanyuan prompt checksum, accepted pronunciation form, original destination/object keys, and overwrite policy; proof requires production-inputs.json and destination inventory. Source: A-011. Proof: production-inputs.json and requirements-audit.md.
- [ ] **T-2:** Stage a new IndexTTS-2.5 + Yuanyuan production rerender beginning with a chapter-four pilot that contains `伴隨著`; proceed to the remaining chapters only after pilot pronunciation/listening PASS, with resumable manifests and no in-place overwrite; proof requires pilot/full manifests, WAVs, listening verdict, and logs. Source: A-006.
- [ ] **T-3:** Validate staged WAVs, checksums, manifests, headroom, pronunciation fixture, and representative human listening; proof requires production-validation.json and release note. Source: A-006.
- [ ] **T-4:** Publish only after dry-run diff PASS, then verify original destination objects/files, checksums, chapter names, and catalog/feed metadata; proof requires upload receipt and post-upload inventory. Source: A-006.
- [ ] **T-5:** Remove only the explicit test-artifact allowlist after publication verification; preserve production files, canonical source, models, prompts, and final manifests; proof requires cleanup receipt and after-inventory. Source: A-006.

## Accepted scope changes

- Early cleanup of two superseded failed Issue #5 preview directories. Source: A-009. Effect: moved only those directories to recoverable Trash; preserved v3, benchmark, Yuanyuan, and pronunciation evidence.

## Current recovery

- **Current item:** T-2.

- **Last proven result:** T-1 PASS; pilot paused intentionally after 66 validated outer chunks / 119 completed synthesis calls, with manifest and staging artifacts preserved.

- **Active blocker or running process:** Pilot paused by owner request; no process running; staging remains resumable.

- **Next safe action:** Resume the chapter-four pilot from its in-progress manifest; validate/listen before any full rerender/upload/cleanup.

- **Expected changed files:** `.agentflow/artifacts/A-006-production-rerender-upload-cleanup/` and external staged production artifacts; no product source changes expected unless Issue #9 requires a pronunciation fix first.

## Completion proof

- **All accepted tasks checked:** no.

- **Blocking accepted decision:** none.

- **Operation running:** no.

- **Next action remaining:** T-2.

- **Evidence status:** current.

- **Judgment:** active.

## Update meaning

- Saving this tracker is a recovery checkpoint, not a stop signal.

- Work continues with the next unfinished item unless an independent stop condition applies.
