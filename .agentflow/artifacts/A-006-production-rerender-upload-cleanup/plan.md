# Execution plan — regenerate, publish, and clean the audiobook outputs

## Goal

Regenerate the previously delivered audiobook outputs with the accepted
IndexTTS-2.5 + Yuanyuan configuration and the accepted pronunciation form,
publish the verified production files to the exact original destination, then
remove only superseded test artifacts after publication is independently
verified.

## Frozen facts

- Human listening prefers IndexTTS-2.5 for audiobook narration over MLX 1.5.
- The accepted speaker reference is
  `/Users/howard/index-tts-workspace/index-tts/prompts/voice.wav`, byte-identical
  to `prompts/yuanyuan/yuanyuan_vocals_30s.wav`.
- The pronunciation requirement is `伴隨著` → `ㄓㄜ` / `ZHE5`. The exact
  backend form must be frozen from the successful Issue #9 test before the
  production render.
- The current test/benchmark artifacts live outside the repository under
  `/Users/howard/index-tts-workspace/previews/`.
- A read-only scan found prior chapter WAVs in
  `/Users/howard/Music/Music/Media.localized/Music/Unknown Artist/Unknown Album/`.
  The canonical upload destination and object/file naming must still be
  resolved from prior manifests, Music library records, or the original upload
  log. Do not assume this folder is the only destination.

## Scope boundary

In scope:

- The previously generated production chapters/files identified in the
  destination inventory.
- IndexTTS-2.5 with Yuanyuan, accepted emotion policy, accepted pronunciation
  form, and production chunk/manifest settings.
- Staged generation, objective validation, destination upload/copy, checksum
  verification, and allowlisted test-artifact cleanup.

Out of scope:

- Choosing a new voice, emotion policy, or pronunciation form during the
  production rerender.
- Uploading before destination and checksum gates pass.
- Deleting canonical manuscripts, model checkpoints, prompts, production files,
  Music library records outside the replacement allowlist, or unrelated tests.
- Re-running the MLX comparison or changing the default backend.

## Tasks

1. **Resolve and freeze production inputs**
   - Identify the exact previous production chapters, source scripts, output
     names, upload destination, object keys, and accepted Issue #9 pronunciation
     form.
   - Record Yuanyuan prompt SHA-256, source-script SHA-256, model/runtime
     identity, emotion policy, and expected output list.
   - Stop if the pronunciation winner or destination is ambiguous.
   - Proof: frozen `production-inputs.json` and destination inventory.

2. **Stage the production rerender**
   - First render only `04-chapter-four`, because it contains `伴隨著`, the
     Issue #9 pronunciation gate, and the previously reviewed styled passage.
   - Render into a new external staging directory with a new run identity;
     never overwrite the old production files in place.
   - Use one IndexTTS-2.5 model session, production chunking, deterministic
     settings, pronunciation fixture coverage, and resumable manifests.
   - Stop after the chapter-four pilot if pronunciation, pacing, or voice
     quality fails; render the remaining 12 chapters only after the pilot
     listening PASS.
   - Keep private prompts, checkpoints, generated WAVs, and caches outside Git.
   - Proof: staged pilot manifest, per-chunk WAVs, final WAV, generation logs,
     and a pilot listening verdict before full-book staging.

3. **Run objective and acoustic release checks**
   - Validate every staged file as non-empty finite mono PCM16 at the expected
     sample rate, with duration, checksum, peak/headroom, and manifest identity.
   - Confirm the pronunciation fixture is present in the actual backend text and
     the accepted Yuanyuan real-model pronunciation evidence is attached.
   - Listen to representative production outputs before publication.
   - Proof: `production-validation.json` and a human release note.

4. **Publish to the original destination**
   - Perform a dry-run destination diff first: list source path/object key,
     target path/key, old checksum, new checksum, and overwrite action.
   - Upload/copy only after the staged validation PASS and exact destination
     identity are frozen.
   - Verify the destination by listing/statting each uploaded object/file and
     recalculating or reading its checksum where the destination supports it.
   - Update the original feed/catalog/metadata only if the original workflow
     requires it, preserving chapter order and names.
   - Proof: upload receipt, destination inventory, and post-upload checksum map.

5. **Clean superseded test artifacts**
   - Build an explicit deletion allowlist from the test-run manifest, including
     old benchmark directories, candidate pronunciation WAVs, temporary logs,
     and staging leftovers that are no longer needed.
   - Confirm production destination verification and retain the final production
     manifest before cleanup.
   - Move allowlisted local test files to Trash or use the project cleanup path;
     do not use broad recursive deletion or pattern-only cleanup.
   - Proof: before/after inventory, cleanup receipt, and confirmation that
     production files and canonical inputs remain present.

## Safe stopping points

- Stop before rendering if the accepted pronunciation form, source script,
  output list, or original destination cannot be proven.
- Stop before upload if any staged WAV, manifest, checksum, pronunciation, or
  listening gate fails.
- Stop before cleanup if destination verification is incomplete or an artifact
  cannot be classified as test-only.
- Any overwrite, remote delete, or irreversible cleanup requires an explicit
  final dry-run inventory and target allowlist.

## Completion condition

The plan is complete only when the chapter-four pilot passes pronunciation and
listening, the remaining production rerender is verified and published to the
original destination, destination checksums/catalog are recorded, and the
allowlisted test artifacts are removed without touching production or canonical
inputs. The final report must name any artifacts intentionally retained.

Self-check: plan separates input freeze, staged rendering, validation, publish, and cleanup; it does not assume the original destination or authorize broad deletion.
