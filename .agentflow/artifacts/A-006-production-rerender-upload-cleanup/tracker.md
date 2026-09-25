# Tracker

## Identity

- **Work key:** A-006-production-rerender-upload-cleanup.

- **Active Ask:** A-011.

- **Goal:** Plan and execute the verified Yuanyuan/IndexTTS-2.5 production rerender, original-destination publication, and allowlisted test cleanup.

- **Last update:** 2026-09-24 22:31:00 Asia/Taipei.

- **Evidence commit:** 44cf52f (neutral-mode optimization); current devlog checkpoint is uncommitted.

## Overall state

- **State:** active.

- **Reason:** A macOS watchdog kernel panic/reboot interrupted the eight-chunk patch during its first MPS inference call; original Chapter 4 audio remains intact.

- **Total:** 5.

- **Completed:** 2.

- **Remaining:** 3.

## Accepted task checklist

- [x] **T-1:** Resolve and freeze source scripts, production output list, Yuanyuan prompt checksum, accepted pronunciation form, original destination/object keys, and overwrite policy; proof requires production-inputs.json and destination inventory. Source: A-011. Proof: production-inputs.json and requirements-audit.md.
- [x] **T-2:** Stage a new IndexTTS-2.5 + Yuanyuan production rerender beginning with a chapter-four pilot that contains `伴隨著`; proceed to the remaining chapters only after pilot pronunciation/listening PASS, with resumable manifests and no in-place overwrite; proof requires pilot/full manifests, WAVs, listening verdict, and logs. Source: A-011. Proof: pilot-run.json and completed pilot staging.
- [ ] **T-3:** Validate staged WAVs, checksums, manifests, headroom, pronunciation fixture, and representative human listening; proof requires production-validation.json and release note. Source: A-006.
- [ ] **T-4:** Publish only after dry-run diff PASS, then verify original destination objects/files, checksums, chapter names, and catalog/feed metadata; proof requires upload receipt and post-upload inventory. Source: A-006.
- [ ] **T-5:** Remove only the explicit test-artifact allowlist after publication verification; preserve production files, canonical source, models, prompts, and final manifests; proof requires cleanup receipt and after-inventory. Source: A-006.

## Accepted scope changes

- Early cleanup of two superseded failed Issue #5 preview directories. Source: A-009. Effect: moved only those directories to recoverable Trash; preserved v3, benchmark, Yuanyuan, and pronunciation evidence.

## Current recovery

- **Current item:** T-3.

- **Last proven result:** Original v2 chapter-four pilot remains valid at 148 chunks / 56:36.07 mono PCM16/22050; checksum `bc0450141d0e997c2076265297e0941239d9a737484a412f6eb429b512180765` is unchanged. Runner fix is in the working tree; chunk-6 audio patch is incomplete.

- **Active blocker or running process:** No process running. Panic evidence reports low swap/segment exhaustion; post-reboot check still shows 5.18 of 6.14 GB swap used, so another MPS synthesis is deferred until the host is stable.

- **Next safe action:** Stabilize memory/swap use; then choose an isolated CPU fallback or a much smaller MPS probe before continuing the 8-chunk patch. Preserve all existing audio and do not upload until human listening PASS.

- **Expected changed files:** `audiobook_pipeline/runner.py`, `.agentflow/artifacts/A-006-production-rerender-upload-cleanup/`, and external staged patch artifacts; no production destination, R2, feed, or canonical manuscript changes.

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
