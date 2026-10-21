# Design — A-011 Colab repair + Colab-vs-Gemini TTS comparison

Status: DRAFT — awaiting `Design Go: <commit>`. No source changes before Design Go.

## Original Ask (verbatim)

- `godev 繼續開發`
- (re: notebook conflict) `這是為什麼 打架`
- `yes make a plan for it and I want to make sure that we can both use colab and gemnitts right , or maybe we should compare this two method ?`

## Normal journey

1. Owner opens either Colab notebook → Chapter 12 resumes from its 22 validated chunks (no identity reset) → finishes → produces 12 WAV.
2. Owner can render a short comparison passage with Colab IndexTTS-2.5 (Yuanyuan clone) and with Gemini TTS (AI Studio, built-in voice), listen side by side, and choose per use case.

## Part A — Repair the BLOCKING cross-check (F1–F6, ruff, F8)

| # | Change | Observable need | Rejected smaller alternative |
|---|---|---|---|
| A1 | Remove `infer_v2` fallback in `backends.py`; import failure of `infer_v2_5` raises the old "IndexTTS-2.5 runtime is unavailable" error | F1: IndexTTS-2 audio can be validated/reused under the 2.5 label | Record loaded module in identity — adds a concept; fallback has no owner need |
| A2 | Keep the 12 s floor in `audio.py`; revert `max_seconds_per_char` to 0.8 in `config.py`, `default.toml`, `colab-cuda.toml`; tests: 5 chars/9.54 s passes at k=0.8 (fails on old formula), 5 chars/12.01 s fails, long-chunk limit unchanged | F2 double loosening; untested floor | Keep k=1.2 and drop floor — would reset Ch12 identity (F3) |
| A3 | Both notebooks + `scripts/colab_run.py` write/keep 0.8; delete the regex patch to 1.2 in quick runner | F3: Ch12 22 chunks re-rendered; notebooks flip identity | — |
| A4 | Fix 7→8-element `bold_vector` in quick runner + `colab_run.py`; `load_config` rejects vectors whose length ≠ 8 | F4 silent emotion-dimension shift | Fix writers only — Drive copy may already be wrong; loader check catches it |
| A5 | Remove pip/HF self-heal from `backends.py` (notebooks already install/download); missing files raise a clear error | F5 side effects in library, swallowed errors, BLE001 | Make it raise but keep it — still installs on Mac |
| A6 | Quick runner: `subprocess.run(..., check=True)`, skip only when manifest `status == "complete"`, install pinned to a commit SHA | F6 failures hidden; partial WAV skipped forever | — |
| A7 | `ruff check .` clean; STATUS commit/lint claims corrected | F8 / 26 lint errors | — |

Out of scope (parked proposals): `docs/apple-audiobook-conversion.md`, `ag.json` tier change, span-merge tests (F7), merging the two notebooks into one.

Owner check required (not code): open the Drive `colab-cuda.toml` and confirm `bold_vector` has 8 values (decides whether 00–11 bold spans were affected).

Proof: failing tests first for A1/A2/A4/A5; full suite + ruff + compileall; targeted cross-check PASS on implementation commit.

## Part B — Compare Colab IndexTTS-2.5 vs Gemini TTS (evaluation, no new backend yet)

Key constraint found: Gemini TTS here is `AiStudioTts` skill = ego-browser CDP automation of the AI Studio web UI. It offers only built-in voices (Aoede/Kore/…), **cannot clone the Yuanyuan reference**, outputs 24 kHz mono, and depends on a logged-in browser + UI selectors.

Comparison set (same Simplified-Chinese text for both):
1. Chapter 4 opening incl. `第四章` heading (known slow-pacing spot, ~00:01)
2. Chapter 4 `藝術，它不是一門硬性科學。` passage (~01:30, isolated `不是`)
3. Chapter 12 chunk 23 `时间的移除` span (the 9.54 s case)
4. One `伴随着` sentence (pronunciation gate)
5. ~3-minute continuous passage (long-form consistency)

Measured per method: wall time per minute of audio, failures/retries, duration per char, trailing silence, rail-sample ratio, sample-rate/format; plus owner blind listening score (naturalness, pacing, pronunciation, voice fit). Output: `comparison.md` + paired WAVs under `/Users/howard/index-tts-workspace/previews/` (no production paths, no R2).

Decision after comparison (owner): (a) keep Colab only; (b) add Gemini as third backend in `backends.py` for specific uses; (c) switch. Building a Gemini backend before this evidence is rejected (Minimality).

Risk notes for (b): web-UI automation is fragile and may conflict with AI Studio terms; an official Gemini API TTS path would be the maintainable backend if chosen.

## Order

A (repair) → owner resumes Ch12 in Colab → B (comparison) can run in parallel with Ch12 since Gemini runs locally in browser.
