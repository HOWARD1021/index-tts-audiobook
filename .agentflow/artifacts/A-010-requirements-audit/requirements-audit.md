# A-006 requirements audit

Audit date: 2026-09-20. Frontend monitoring UI is explicitly out of scope.

| Requirement | Status | Evidence / remaining action |
| --- | --- | --- |
| Prefer IndexTTS-2.5 for audiobook delivery | PASS | Human listening prefers 2.5 for smoother delivery and fewer wrong characters. |
| Use Yuanyuan reference | PASS | Prompt path and SHA-256 are frozen in `production-inputs.json`. |
| Recover original local destination | PASS | `.../zh-simplified-tts/audio` with WAV/M4A/manifests/feed.xml. |
| Recover original remote destination | PASS | R2 bucket `howard-audiobooks`, public base and feed URL recovered from `publish_podcast.py`/`feed.xml`. |
| Freeze pronunciation form for `伴隨著` | BLOCKED | Issue #9 requires choosing the successful candidate; current/direct/plain candidates remain external. |
| Freeze production emotion policy | PARTIAL | Pilot can use the accepted 2.5 neutral/pause-only path; Issue #6 remains open for final local-emotion policy. |
| Run chapter-four pilot | NOT STARTED | Starts only after pronunciation form freeze. |
| Validate pilot WAV/manifest/checksum/headroom/listening | NOT STARTED | Follows pilot render. |
| Regenerate remaining 12 chapters | NOT STARTED | Blocked by pilot PASS. |
| Upload R2/feed/catalog | NOT STARTED | Blocked by full production validation and dry-run diff. |
| Remove remaining test artifacts | PARTIAL | Two failed previews moved to Trash; final cleanup waits for publication verification. |
| Frontend execution monitor | OUT OF SCOPE | No frontend needed for current delivery path. |

## Decision

Do not load the model or start chapter-four generation yet. Freeze the Issue #9
candidate first; then run only chapter 04 as the production pilot. If it passes
pronunciation and listening, continue to the remaining 12 chapters.

## Next action

Record the accepted pronunciation candidate and its Yuanyuan audio evidence as
the T-1 frozen input. Then stage the chapter-four pilot in a new external
directory without touching the existing production files.
