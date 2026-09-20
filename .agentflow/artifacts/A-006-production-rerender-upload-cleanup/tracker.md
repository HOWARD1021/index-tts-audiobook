# Tracker

## Identity

- **Work key:** A-006-production-rerender-upload-cleanup.

- **Active Ask:** A-007.

- **Goal:** Plan and execute the verified Yuanyuan/IndexTTS-2.5 production rerender, original-destination publication, and allowlisted test cleanup.

- **Last update:** 2026-09-20 17:35:00 Asia/Taipei.

- **Evidence commit:** uncommitted.

## Overall state

- **State:** active.

- **Reason:** Production rerender and publication plan is recorded; destination and accepted pronunciation form are not yet frozen.

- **Total:** 5.

- **Completed:** 0.

- **Remaining:** 5.

## Accepted task checklist

- [ ] **T-1:** Resolve and freeze source scripts, production output list, Yuanyuan prompt checksum, accepted pronunciation form, original destination/object keys, and overwrite policy; proof requires production-inputs.json and destination inventory. Source: A-006.
- [ ] **T-2:** Stage a new IndexTTS-2.5 + Yuanyuan production rerender with resumable manifests and no in-place overwrite; proof requires staged manifests, WAVs, and logs. Source: A-006.
- [ ] **T-3:** Validate staged WAVs, checksums, manifests, headroom, pronunciation fixture, and representative human listening; proof requires production-validation.json and release note. Source: A-006.
- [ ] **T-4:** Publish only after dry-run diff PASS, then verify original destination objects/files, checksums, chapter names, and catalog/feed metadata; proof requires upload receipt and post-upload inventory. Source: A-006.
- [ ] **T-5:** Remove only the explicit test-artifact allowlist after publication verification; preserve production files, canonical source, models, prompts, and final manifests; proof requires cleanup receipt and after-inventory. Source: A-006.

## Accepted scope changes

- None.

## Current recovery

- **Current item:** T-1.

- **Last proven result:** T-1 destination inventory PASS: 13 chapter outputs, local audio/feed directory, R2 bucket `howard-audiobooks`, public base, publish script, and Yuanyuan prompt checksum recorded. Pronunciation form remains pending Issue #9 candidate confirmation.

- **Active blocker or running process:** None; planning only.

- **Next safe action:** Freeze the successful Issue #9 pronunciation form, then stage production rerender; no upload or cleanup before that gate.

- **Expected changed files:** `.agentflow/artifacts/A-006-production-rerender-upload-cleanup/` and external staged production artifacts; no product source changes expected unless Issue #9 requires a pronunciation fix first.

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
