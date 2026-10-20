* _2026-10-20 23:28:04 (Claude Opus 5.5/high)_

# Cross-check report — A-011 Colab/backend range

Implementation commit: `98f1201` (range `44cf52f..98f1201`, 27 commits, `.agentflow/` excluded from the code review). Reviewer: independent, read-only; the only file written is this report.

## Commands rerun (exact results)

- `uv run pytest -q` → **9 errors during collection** (`ModuleNotFoundError: No module named 'audiobook_pipeline'`). The project `.venv` has no `dev` extra, so `uv run` fell through to `/Users/howard/miniconda3/bin/pytest`. This is an environment issue, not a code failure.
- `uv run --isolated --extra dev pytest -q` → **35 passed, 1 skipped**. This matches the coordinator's evidence.
- `uvx ruff check .` → **Found 26 errors**: `audiobook_pipeline/backends.py` 2 (BLE001 at :135 and :159), notebooks 23 (`colab_indextts_render.ipynb` 12, `colab_quick_runner.ipynb` 11), `scripts/colab_run.py` 1 (I001). This matches the coordinator's evidence.
- `uvx ruff check .` on a clean export of base `44cf52f` → **All checks passed!** All 26 errors were introduced in this range.
- The new `tests/test_audio.py` (from `98f1201`) run against base `44cf52f`'s `audio.py` → **4 passed** (see F2).

## Findings

### F1 — HIGH — Silent fallback to IndexTTS-2 under the `indextts-2.5` label, which can lead to wrong chunk reuse
`audiobook_pipeline/backends.py:98-106`: when `indextts.infer_v2_5` fails to import, the code now quietly imports `indextts.infer_v2` (IndexTTS-2) instead of raising "IndexTTS-2.5 runtime is unavailable". The manifest identity (`runner.py:158-181`) still records `backend: "indextts-2.5"` and does not record which inference module actually loaded.
- Concrete local trigger: `/Users/howard/index-tts-workspace/index-tts` (the checkout that holds `prompts/voice.wav`, as the colab guide and devlog cite) contains `infer_v2.py` but **no** `infer_v2_5.py`. Before this change, `--project-root` pointed there failed loudly. Now it renders with a different model under the 2.5 label.
- Wrong-reuse path: chunks rendered through the fallback are written as `status: validated` under an identity that is byte-identical to a genuine 2.5 run with the same root/model_dir. If the upstream checkout later gains `infer_v2_5.py`, those IndexTTS-2 chunks get reused as 2.5 audio.
- `ImportError` from inside `infer_v2_5` (for example a missing transitive dependency) also triggers the downgrade, because the fallback runs before the fugashi self-heal at :112-137.

### F2 — HIGH — Duration fix loosens the check twice; the new test does not cover the `audio.py` change; the 9.54 s span has no quality evidence
- `audio.py:60` changes `max(5.0, n*k+5.0)` → `max(12.0, n*k+6.0)`. Separately, `config.py:44`, `config/default.toml:14` and `config/colab-cuda.toml:14` change `k` 0.8 → 1.2. **Either change alone clears the Chapter 12 case**: old formula with k=1.2 gives 11.00 s, new formula with k=0.8 gives 12.00 s, and both exceed 9.54 s. Shipping both widens the limit for a 400-char chunk from 325 s to 486 s (+50%), so long-chunk runaway detection is weaker than the Ask needed.
- `tests/test_audio.py:15-21` (`test_short_emotion_span_with_prosody_padding_passes`) passes `max_seconds_per_char=1.2`. Against the **old** formula it gives an 11.0 s limit, so it passes without the `audio.py` change (verified: 4 passed on base `audio.py`). The 12.0 s floor is untested. No boundary test exists (for example, 12.01 s fails for 5 chars), and nothing covers long chunks. `test_runaway_short_chunk_fails_duration_sanity` was changed from 20 s to 25 s without need; 20 s already fails the 12 s floor.
- Does it still detect runaway generation? Only coarsely. For 1–5 char spans the limit is now 12 s, about 8–10× natural speech for 5 Hanzi (≈1.2–1.8 s). The 9.54 s output for `时间的移除` is itself ~6× natural. RUN-028 asserts "natural cadence and tail padding" but records no listening, waveform, or silence-ratio evidence. Earlier devlog findings (RUN-007, RUN-021) put short isolated spans at the root of the pacing defects. The change therefore turns a correctly-firing gate into a pass without showing the audio is acceptable. Chapter 12 chunk 23 should get a human listen or a trailing-silence measurement before release.

### F3 — HIGH — The `max_seconds_per_char` change resets Chapter 12 resume, and the two notebooks disagree
`max_seconds_per_char` is part of the run identity (`runner.py:178`), and `_identity_matches` (`runner.py:184-185`) discards **all** prior chunk records on any mismatch.
- `colab_quick_runner.ipynb` cell 8 regex-patches the Drive `colab-cuda.toml` to 1.2. Chapter 12's manifest was written under 0.8, so the identity no longer matches and chunks 0000–0022 are all re-synthesized. RUN-028's claim "resume Chapter 12 instantly" is false for this notebook. The cost is GPU time, not wrong reuse.
- `colab_indextts_render.ipynb` cell 10 unconditionally **rewrites** the Drive config with `max_seconds_per_char = 0.8`. Its Step 10 (cell 20) has none of the RUN-028 changes: no config patch, no skip-completed, no package upgrade. RUN-028 says "Optimized Step 10 batch loop in notebooks", but that is only true for the quick runner. Because of the 12 s floor, this notebook does resume Chapter 12 correctly. Running the two notebooks alternately flips the identity and re-renders everything each time.
- Changing `config/default.toml` and `config.py` defaults likewise invalidates every existing Mac-side manifest under the default profile. The Ask did not require that (see F2).

### F4 — MEDIUM — Wrong emotion vector length in two Colab config writers, and the loader does not validate it
`notebooks/colab_quick_runner.ipynb` cell 4 and `scripts/colab_run.py:61` write `bold_vector = [0.45, 0.0, 0.0, 0.0, 0.0, 0.20, 0.10]`, which is **7** elements; the canonical vector at `config/colab-cuda.toml:27` / `config.py:15` has 8. `load_config` (`config.py:69-72`) accepts any length. Upstream `infer_v2_5.normalize_emo_vec` uses `zip(emo_vector, emo_bias)`, which truncates silently, so bold spans shift the 0.20 weight into a different emotion dimension. This bites only when one of these writers creates the Drive config first. The owner should check the live Drive `colab-cuda.toml` to see whether chapters 00–11 bold spans were affected.

### F5 — MEDIUM — Network and install side effects in library code, with failures swallowed
`backends.py:112-137`: backend construction runs `python -m pip install fugashi unidic-lite` on **every** host, including the local Mac/uv path, whenever the import fails. uv venvs ship without pip, so there it fails. `except Exception` (ruff BLE001) only prints a warning and continues.
`backends.py:139-159`: if any of five files is missing from `model_dir`, it runs `snapshot_download("IndexTeam/IndexTTS-2.5", local_dir=model_dir)` into the user-supplied directory, again with `except Exception` → print → continue. The default `model_dir` is `<project_root>/checkpoints` (`runner.py:234`). Pointing at the IndexTTS-2 checkout from F1 (no `codec.pth`/`gpt.pth`/`s2mel.pth`) would download ~4 GB+ into that checkout and overwrite its `config.yaml`. The `IndexTeam/IndexTTS-2.5` repo id matches the notebooks and RUN-026; I could not verify the repo contents offline. The real Mac 2.5 checkout (`/Users/howard/orca/workspaces/index-tts/horseshoe/checkpoints`) has all five files, so the self-heal stays dormant on the normal path. `huggingface_hub` is not a project dependency, so on a minimal install this step degrades to a printed warning. The notebooks already download checkpoints and install fugashi, so the library self-heal duplicates them.

### F6 — MEDIUM — Quick-runner batch loop hides failures and uses a weak completion test
`colab_quick_runner.ipynb` cell 8 runs render and validate through IPython `!{cmd}`, which ignores non-zero exit codes. A failed chapter render (exactly the Chapter 12 situation) moves on to the next chapter and still prints "🎉 所有章節批次合成完成！". Skip-completed tests `st_size > 100_000` rather than the manifest's `status == "complete"`. The final WAV is written non-atomically (`audio.py:112` `sf.write` straight to the target), so an interrupted concatenation leaves a >100 KB partial that is then skipped permanently. Cell 8 also re-installs from unpinned `git+https://github.com/HOWARD1021/index-tts-audiobook.git`, which drops the `[indextts]` extra and is not pinned to a reviewed commit, so production renders run whatever is on remote main.

### F7 — LOW — Span-merge runner change committed without its own tests and without disclosure
`runner.py:105-125, 298-311` (span coalescing plus `synthesis_plan_sha256`) arrived inside `c831e83`, whose message describes only the Colab notebook and backend. It was owner-approved in RUN-022, which also states "No tests are being added". The legacy-plan comparison is conservative: legacy records are reused only when merging leaves the call plan unchanged, otherwise they are re-rendered, so I found no wrong-reuse path. `tests/` still has no coverage for merging or the plan-hash compatibility branch.

### F8 — LOW — Record accuracy
STATUS (`.agentflow/devlog.md:7-9`) names `5149bf1` as current although the duration fix is `5f3d525` and HEAD is `98f1201`, and it claims "Ruff/compileall PASS" while ruff reports 26 new errors (the base was clean). The F3 RUN-028 notebook claim is also overstated.

## Concept accounting against the owner's Ask

| Added concept | Serves the Ask? | Note |
|---|---|---|
| `notebooks/colab_indextts_render.ipynb` | Yes (Colab CUDA + Drive resume) | Missing the RUN-028 Step 10 changes; resets config to 0.8 (F3) |
| `notebooks/colab_quick_runner.ipynb` | Partly; a second notebook duplicates the first | 7-dim bold vector, unchecked `!` exits, unpinned reinstall (F4, F6) |
| `scripts/colab_run.py` | Marginal; a third copy of the same bootstrap | Stale 0.8 config, 7-dim bold vector, ruff I001 (F4) |
| `config/colab-cuda.toml` | Yes | Correct 8-dim vectors |
| `backends.py` v2 fallback, kwarg introspection | Introspection yes; fallback no | F1 |
| `backends.py` pip/HF self-heal | Not required (notebooks already do it) | F5 |
| `pyproject.toml` `indextts` extra + `uv.lock` | Yes (fugashi needed by upstream 2.5 ja G2P) | Acceptable dependency addition |
| `cli.py`/`backends.py` `USE_TF=0` setdefault | Yes (Colab protobuf conflict) | Harmless locally |
| `audio.py` 12 s floor + test | Yes, but untested as written | F2 |
| `max_seconds_per_char` 0.8→1.2 in default.toml/config.py | Not needed; resets resume identity | F2, F3 |
| `docs/colab-runner-guide.md`, README section | Yes | Embeds local absolute paths and prompt SHA; fine for a private repo |
| `docs/apple-audiobook-conversion.md` | **No** — WAV→M4A publishing is outside the Ask | Park as proposal |
| `ag.json` worker-tier update (`98f1201`) | **No** — agent routing config, not the Ask | Park as proposal |
| `runner.py` span merge | Owner-approved in RUN-022 (same round) | F7 |

No hostile instructions were found in the repository, devlog, notebooks, or docs.

## Recommended minimal repairs (not applied)
1. Remove the `infer_v2` fallback, or record the loaded module in the run identity and fail loudly when it is not `infer_v2_5` (F1).
2. Keep one loosening only: either the 12 s floor or k=1.2, and preferably scope it to `colab-cuda.toml`. Add a test that fails on the old formula plus a boundary test. Listen to or measure Chapter 12 chunk 23 before release (F2).
3. Make both notebooks agree on the config value so Chapter 12's existing manifest identity is preserved (F3).
4. Fix the 7-element `bold_vector` in `colab_quick_runner.ipynb` and `colab_run.py`, add a length check in `load_config`, and audit the Drive config (F4).
5. Remove the pip/HF self-heal from library code, or make it raise instead of printing (F5). Use `subprocess.run(..., check=True)` and manifest `status == "complete"` in the quick runner, and pin the install to a commit (F6).
6. Fix ruff, and correct the STATUS commit and lint claims (F8).

Outcome: BLOCKING
Minimality: BLOCKING
Conformance: BLOCKING
Verdict: BLOCKING

Self-check: [host mechanical correction — worker emitted an empty Self-check line; all findings and verdict lines above are unchanged worker text]
