# STATUS

Project: index-tts-audiobook

Notebook: .agentflow/devlog.md — root.

Current commit: 1b5683f — requirements audit complete; chapter-four pilot remains gated by Issue #9 pronunciation form.

Tests/scenarios: 31 passed, 1 opt-in MLX skip; Ruff/compileall PASS; 32 chunk WAVs and 8 final WAVs validated.

Configuration: ag.json — validated; MLX 1.5 and IndexTTS-2.5 external runtimes; primary runs used same script/prompt identity.

Proven: Requirements audit confirms destination, outputs, reference, backend preference, and cleanup boundaries; frontend monitor is out of scope.

Open: Freeze Issue #9 pronunciation form before chapter-four pilot; Issue #6 emotion policy; Issue #7 headroom.

Next: lock the successful pronunciation candidate, then stage only chapter 04; no full rerender/upload/cleanup before pilot validation.

Artifacts: A-002 through A-006 Agentflow records; benchmark audio in `/Users/howard/index-tts-workspace/previews/`; production destination remains to be resolved in A-006 T-1.

Archived eras: none.

Streams: none.

---

# → Ask / A-001

sure godev

## [RUN-001] Event (during round A-001)

- Ask: `sure godev` authorizes direct implementation of Markdown emphasis metadata and local emotion rendering.
- Route: direct; scope is limited to text parsing, render segmentation, emotion-vector propagation, tests, and workflow records.
- Design: capture emphasis before cleanup; never send Markdown delimiters to a backend; preserve meaningful punctuation.
- Proof: add red-first tests for span parsing and per-span emotion requests, then run the complete pytest suite.

## [RUN-002] Event (during round A-001)

- Implementation: added PreparedNarration/NarrationSpan metadata, bold/italic emotion profiles, per-span backend requests, short local joins, and markup-aware manifest hashes.
- Verification: `uv run pytest -q` passed with 24 tests and 1 opt-in skip; compileall passed; chapter 04 planning produced 149 clean chunks with `ZHE5` retained.
- Scope: no model checkpoints, prompts, generated audio, or source manuscripts were modified.

## [RUN-003] Event (during round A-001)

- Review: an independent read-only reviewer found and blocked on cross-chunk emphasis state and silent MLX emotion loss; both defects were fixed with regression tests.
- Review result: corrected implementation received Outcome PASS and Minimality PASS; the remaining conformance record issue was fixed by adding the frozen cross-check artifacts to the exact inventory and reconciling the cumulative line delta.
- Evidence: final product suite remains 26 passed, 1 skipped; real-model acoustic rendering remains not-tested.

# ← Reply / A-001
* _2026-09-19 23:14:42 (gpt-5.4/high)_

## [SUMMARY]

- 已完成 `godev` 要求的局部情緒整合：Markdown 粗體／斜體先轉成 metadata，再清除標記並分段生成。
- 普通文字使用 base emotion vector；粗體使用 `bold_vector`；斜體使用 `italic_vector`。
- 長粗體跨 chunk 時會保留情緒狀態；MLX 1.5 沒有情緒向量介面，因此會明確拒絕局部情緒來源。
- `uv run pytest -q`: 26 passed, 1 skipped。

## [FINAL REPORT]

原始 Markdown 現在依序經過：繁體轉簡體、朗讀清理、發音修正、Markdown emphasis metadata 擷取、局部情緒渲染、WAV 合併與驗證。`**巨大的成交量**` 的 `**` 不會送入模型，但該 span 會使用可設定的 bold emotion vector；`*斜體*` 同理。

主要修改：

- `audiobook_pipeline/text.py`: `PreparedNarration`、`NarrationSpan`、跨 chunk marker state。
- `audiobook_pipeline/runner.py`: per-span synthesis、短停頓合併、markup hash resume identity。
- `audiobook_pipeline/backends.py` / `config.py`: per-request emotion vector 與 bold/italic preset。
- `README.md`、`docs/quality-gates.md`、全域 IndexTTS workflow 文件：記錄新的工作流程。

已驗證：完整 pytest、compileall、第 4 章 149 chunks planning、長 emphasis 跨 chunk、MLX 明確拒絕 styled source。沒有修改原始稿、模型、prompt 或生成音檔。

限制：尚未用真實 IndexTTS-2.5 對含多個 styled span 的完整章節做聲音聆聽；短粗體片段若接縫不自然，應改成句子級強調。

Cross-check review: `.agentflow/artifacts/A-001-local-emotion/cross-check-report.md`
Cross-check implementation: 0dbd5b3d3be9a0b71e67f142b54e14b19313ca58

## Questions (batched — each with a suggested default)

- None.

---

# → Ask / A-002

godev 生成 執行計劃

已生成並固定 execution plan。

  - Plan：.agentflow/artifacts/A-002-execution-plan/plan.md
  - Tracker：.agentflow/artifacts/A-002-execution-plan/tracker.md
  - Commit：c7da029
  - Tracker validation：PASS

  執行順序：

  1. Preflight IndexTTS-2.5 runtime、MPS 與 reference WAV
  2. 建立隔離 preview 稿
  3. 使用指定 speaker reference 生成真實 styled preview
  4. 驗證 WAV、manifest、prompt checksum 與 resume
  5. 人工聽感驗收，必要時交給 Issue #6 調整策略

  目前下一個安全動作是 T-1：確認 runtime 與 /Users/howard/orca/workspaces/index-tts/horseshoe/prompts/voice.wav。尚未開始生成音檔或
  修改產品程式。 godev

為何停止

keep  going  godev

## [RUN-001] Event (during round A-002)

- Route: direct execution plan for frontier GitHub Issue #5; no product source changes or model generation started.
- Plan: five tasks cover preflight, isolated preparation, real IndexTTS-2.5 generation, objective validation/resume, and human listening gate.
- Boundary: Issue #6 owns phrase-level versus sentence-level policy; Issue #7 owns the release-quality gate.
- Evidence: tracker validated; plan and tracker are stored under `.agentflow/artifacts/A-002-execution-plan/`.

## [RUN-002] Event (during round A-002)

- Route: direct operational execution of frozen plan c7da029; owner said `keep  going  godev`. No product implementation or preset changes.
- Recovery: previous turn was interrupted; no model process or partial render exists. Corrected notebook path to configured `.agentflow/devlog.md`.
- T-1: runtime/checkpoint/reference exist; torch 2.8.0 MPS allocation passes; prompt is finite mono PCM16/22050 Hz, 9.612 seconds, SHA-256 dd077517ab6558b5aab2cb785a2c6e47bf9450f94982cad35cf5f9a1f5366297.
- Runtime imports pass using existing pure-Python OpenCC loaded by explicit package path; no dependency installation or environment changes. FP32, MPS fallback, QwenEmotion disabled are retained.
- Ownership: preserve unrelated untracked docs/apple-audiobook-conversion.md. Only task records and external isolated preview artifacts will change; no stream needed for these disjoint operational paths.

## [RUN-003] Event (during round A-002)

- T-1/T-2 PASS: required checkpoints and auxiliary resources exist; runtime imports and MPS allocation pass. Output is /Users/howard/index-tts-workspace/previews/issue-5-20260920, outside the repository.
- Prepared chapter-four lines 125, 127, 129; only isolated copy adds italic to the final clause of line 127 and bold around line 129. max_chunk_chars=120 creates four chunks and nine spans, including cross-chunk bold. Source wording and canonical manuscript remain unchanged.
- Exact defaults retained for all emotion vectors/alpha and 80 ms local pauses. Clean-text checks and ZHE5 annotation PASS; prepared.json and preparation.json hold private evidence externally.
- T-3 starts with one instrumented backend factory and seed 42; existing runtime Python loads only the existing pure-Python OpenCC package by explicit path. No dependency changes. Resume mode will fail if any backend load is attempted.

## [RUN-004] Event (during round A-002)

- Preparation correction: added italic marker produced one comma-only span. Interrupted first generation gracefully (exit 130) before reaching it; preserved attempt under issue-5-20260920.
- Moved only the isolated italic opening marker before its comma, preserving narration text, canonical source, and all profiles. Revised output root: /Users/howard/index-tts-workspace/previews/issue-5-20260920-v2. Four chunks / eight spans; every span now contains spoken characters; all T-2 checks pass.
- Verification: pytest 26 passed, 1 opt-in MLX skip; compileall and offline Ruff PASS. No product-source changes. Tracker mechanical proof-field omission corrected and validation PASS.

## [RUN-005] Event (during round A-002)

- Correction to RUN-004: v2 preparation did NOT pass. Adjacent closing bold/opening italic markers formed a triple-star sequence and left a raw star; the preparation assertion caught this. A shell sequencing mistake nevertheless started the v2 process; it was interrupted (exit 130), and is no longer running.
- v3 moves the italic marker after the ordinary words 這是, preventing both punctuation-only and adjacent-marker cases. Direct assertions now PASS for all styles, no raw markers, every span containing spoken characters, ZHE5, and cross-chunk bold. Final fixture: four chunks / nine spans.
- Runtime/output root is /Users/howard/index-tts-workspace/previews/issue-5-20260920-v3. Prior attempts retained for diagnosis. No product or canonical manuscript changes; only isolated test marker placement changed.

## [RUN-006] Event (during round A-002)

- WIP scope comparison: actual owned changes are .agentflow/devlog.md, tracker.md, preflight.json, and external preview artifacts. These match task records plus external outputs; unrelated docs/apple-audiobook-conversion.md is untouched. No product code, preset, or canonical source changes.
- T-1/T-2 complete; T-3 session 99754 is rendering v3 with one loaded backend; first span validated (3.31 s). T-4 and human T-5 remain.
- Tracker validation PASS; pytest 26 passed / 1 skipped, Ruff and compileall PASS. Next: complete generation, objective WAV/manifest checks, unchanged-input resume, then human listening.

## [WIP-001] Checkpoint (during round A-002)

- **Finished:** T-1 runtime/MPS/reference preflight and T-2 isolated preparation; code suite and static checks pass.
- **Running now:** T-3 real MPS render in external issue-5-20260920-v3; two of nine spans generated.
- **Still to do:** Complete render, validate WAVs/manifest/checksums/resume, and obtain human listening verdict.
- **Next work action:** Monitor current model session through completion and execute validate-preview.py.
- **Checks:** [x] tracker.md | [x] devlog RUN | [x] scope matches tracker

## [RUN-007] Event (during round A-002)

- T-3/T-4 PASS: real IndexTTS-2.5 v3 render exited 0; one model session made nine synthesis calls. Final preview is 67.3579138322 s; all fourteen span/chunk/final WAVs are finite, non-empty mono PCM16/22050 Hz and meet existing duration/join checks.
- Identity PASS: clean text, per-chunk markup, styled source, prompt SHA-256, runtime/config identity, actual per-call vectors/alpha, and final checksum. Source manuscript and runtime file/config remain unchanged.
- Resume PASS: exit 0; all four chunks reused; zero model loads or syntheses; thirteen span/chunk files retain hashes and mtimes; joined final checksum remains d35111901e757046349ba134d890b3a8170ed5bf46ddc6ac9160b2926a5d8c62.
- Quality warning: 33,716 of 1,485,242 final samples (2.2701%) reach ±32,767; external runtime clamps at that amplitude. Format checks pass but clipping/distortion requires human listening. Runtime also emitted GenerationMixin and past_key_values deprecation warnings; no truncation warning observed.
- T-5 pending: owner was given the audio link and listening question. No human verdict yet, so Issue #5 is not complete. listening.md provides timestamps and Issue #6 / #7 handoff boundaries; no external messages were sent.
- Scope comparison: all current owned changes are task records under .agentflow and external preview artifacts; unrelated docs/apple-audiobook-conversion.md remains untouched. No source, preset, canonical manuscript, dependency, or product-document changes in this execution. Tracker validation PASS.

## [RUN-008] Event (during round A-002)

- Required final cross-check completed via external-runner-v1, codex-default / gpt-5.6-terra / high, independent no-remote clone, closed stdin, exit 0. Exact reviewed commit: df99169a860066d6da096c51ca6f9cd3bc981a55.
- Outcome PASS; Minimality PASS; Conformance PASS; Verdict PASS for objective execution and honest pending human gate. Reviewer reran 26 passing tests / 1 skip and independently checked all WAV inventory/hashes. Human listening was explicitly not performed.
- Host gate: PASS. Read full report; verified trusted report SHA-256 and clone boundary (only declared cross-check-report.md changed). Imported report without altering substantive conclusions. Clone is not an OS sandbox; inherited credential/network confinement remains unproven.
- T-5 remains blocked only on human listening. No further model work is running, no product changes are pending, and no extra review cycle is required for record-only closeout.

# ← Reply / A-002
* _2026-09-20 09:15:22 (GPT-6)_

## [SUMMARY]

- 固定計畫已執行至 T-4：真實 styled preview 長 67.36 秒，WAV／manifest／checksum／resume 檢查通過。
- T-5 等待人工聽感；Issue #5 尚未完成。
- 約 2.27% 樣本達振幅上限，可能削波；未改 presets 或產品程式。

## [FINAL REPORT]

### 固定 execution plan 與 keep going godev

已接續 plan commit c7da029，完成 T-1 至 T-4。證據 commit 為 df99169a860066d6da096c51ca6f9cd3bc981a55。

音檔：[preview.wav](/Users/howard/index-tts-workspace/previews/issue-5-20260920-v3/preview.wav)，長 67.3579138322 秒。全部私人稿件、音檔與生成 log 保存在該外部目錄，不進 Git。

T-1 通過：torch 2.8.0、MPS 實際運算、checkpoint 與 runtime import 正常；指定 `/Users/howard/orca/workspaces/index-tts/horseshoe/prompts/voice.wav` 是 9.612 秒 mono PCM16/22050 Hz。SHA-256：dd077517ab6558b5aab2cb785a2c6e47bf9450f94982cad35cf5f9a1f5366297。Runtime 使用已有 Python 環境及指定路徑的既有 pure-Python OpenCC，未安裝依賴。

T-2 通過：隔離複製第 4 章 125、127、129 行，加入斜體／長粗體；max_chunk_chars=120，4 chunks／9 spans。普通、粗體、斜體、ZHE5、跨 chunk 粗體、無 raw markers 的檢查全部通過。首次產生獨立逗號；第二次相鄰標記留下 raw star，而且 shell sequencing 錯誤讓 assertion 失敗後仍啟動模型，已中止；第三版調整副本標記位置後通過。兩次中止記錄保留，canonical manuscript 文字未改。

T-3 通過：IndexTTS-2.5／MPS／FP32／QwenEmotion off、use_random=false、seed=42；維持全部既有 emotion vectors／alpha、80 ms local pause 與 450 ms chunk pause。一次模型載入，九次 synthesis，exit 0；不宣稱跨硬體重新生成必然 bit-identical。

T-4 通過：全部 14 WAV 非空、finite、mono PCM16/22050 Hz，duration 與 joins 長度檢查通過。Manifest clean-text／markup／styled-source／prompt／runtime/config／實際 vectors 與 checksum 一致。Resume exit 0，4 chunks 全部 reused、0 模型載入、0 synthesis；13 個 span/chunk WAV 的 checksum 與 mtime 不變，final checksum 不變：d35111901e757046349ba134d890b3a8170ed5bf46ddc6ac9160b2926a5d8c62。

重現 resume：在 `/Users/howard/orca/workspaces/index-tts/horseshoe` 執行 `PYTORCH_ENABLE_MPS_FALLBACK=1 .venv/bin/python -u /Users/howard/index-tts-workspace/previews/issue-5-20260920-v3/run-preview.py resume`。實際 command、config、preparation、per-call vectors、model identity、WAV hashes 與 log 指標都留在外部目錄及本地 validation.json。

T-5 尚待人工：粗體在 00:03.39、00:24.27；斜體在 00:29.25；長粗體跨 chunk 接縫在 00:49.68。請依 listening.md 確認人聲、伴隨著發音、標記洩漏、情緒強度、接縫及失真。未收到人工判定，不關閉 Issue #5。

風險：33,716／1,485,242 樣本（2.2701%）到達 ±32,767，上游 runtime 在此 clamp，可能有削波；既有客觀檢查不包含 peak gate。另有 GenerationMixin／past_key_values 棄用警告，未觀察到 max_mel truncation 警告。接縫／情緒策略交 Issue #6；peak/headroom release gate 屬 Issue #7；沒有發送外部 issue 訊息。

驗證：26 pytest passed、1 opt-in MLX skipped；Ruff、compileall、tracker validation PASS。此輪只修改 `.agentflow/devlog.md` 與 A-002 task records（tracker、preflight、validation、listening 及 review evidence）；重用現有管線，未新增產品抽象或依賴。原有 untracked `docs/apple-audiobook-conversion.md` 未修改。

Cross-check review: .agentflow/artifacts/A-002-execution-plan/cross-check-report.md
Cross-check implementation: df99169a860066d6da096c51ca6f9cd3bc981a55
Host gate: PASS

### 為何先前停止

先前回合遭外部中斷，並非等待重新授權或模型生成失敗；最初 notebook 路徑填錯也已修正。收到 keep going 後持續執行至客觀驗證完成。目前唯一未完成的 accepted task 是人工聽感。

## Questions (batched — each with a suggested default)

- 請聽 preview 後回覆上述項目是否通過，若有問題請附大約秒數。
- Suggested default: 尚未聽則保留 T-5 pending，不關閉 Issue #5、不調整 presets。
- ans:

---

# → Ask / A-003

godev 驗收完成 整體 聲音太過亢奮 不適合 擔任有聲書的配音 或許可以調用其他情緒 像是肯定 或是想要引起閱聽人注意的 或是就不要特定強掉 停頓即可

## [RUN-001] Event (during round A-003)

- Owner completed the human listening gate for the Issue #5 preview: overall delivery is too excited and unsuitable for audiobook narration.
- Acoustic acceptance result: objective generation/format/resume evidence remains PASS; listening quality is FAIL for the current emotion profile. This is valid completion evidence for Issue #5 and a handoff to Issue #6, not a reason to alter presets in this ticket.
- Owner's proposed Issue #6 decision space: restrained affirmative/confident emotion for selective emphasis; light attention cues only where needed; or no explicit emotion vector for most narration with short pauses only.
- T-5 is checked with listening.md as proof. Tracker is complete with 5/5 tasks; Issue #7 retains peak/headroom release policy. No source, preset, manuscript, model, prompt, or generated audio was changed.

# ← Reply / A-003
* _2026-09-20 09:36:00 (GPT-5)_

## [SUMMARY]

- 人工聽感驗收已完成：目前聲音整體過度亢奮，不適合直接作為有聲書配音。
- T-1 至 T-4 的 runtime、生成、WAV、manifest、checksum 與 resume 證據仍然通過。
- T-5 已記錄為 listening quality FAIL，Issue #5 執行完成並交由 Issue #6 決定新的情緒策略。

## [FINAL REPORT]

這次 preview 的問題不是模型、speaker reference、格式或 resume 機制，而是目前局部情緒設定造成整體聲音太亢奮。這份音檔不應直接用於有聲書成品。

Issue #6 的候選方向已記錄在 `listening.md`：

- 只在需要強調時使用較克制的肯定／自信情緒；
- 只在需要抓住注意力的位置使用輕微 attention cue；
- 大部分 narration 不指定額外情緒，只保留短停頓。

目前沒有選定其中一個方案，也沒有修改 presets、產品程式、canonical manuscript、model、prompt 或生成音檔。Issue #7 仍負責 peak/headroom 與削波 release gate。

Evidence：`.agentflow/artifacts/A-002-execution-plan/listening.md`、`validation.json`、`cross-check-report.md`。原始 preview：[preview.wav](/Users/howard/index-tts-workspace/previews/issue-5-20260920-v3/preview.wav)。

Cross-check review: .agentflow/artifacts/A-003-acceptance/cross-check-report.md
Cross-check implementation: df99169a860066d6da096c51ca6f9cd3bc981a55
Host gate: PASS

## Questions (batched — each with a suggested default)

- None. Issue #6 owns the next emotion-policy experiment.

---

# → Ask / A-004

godev 紀錄計劃

## [RUN-001] Event (during round A-004)

- Route: direct planning record for GitHub Issue #8; user requested `godev 紀錄計劃`. No benchmark process, model load, product implementation, preset change, or generated audio started.
- Frozen plan: compare MLX IndexTTS 1.5 pause-only against IndexTTS-2.5 MPS neutral/pause-only, with optional 2.5 local-emotion diagnostic. Measure cold load, repeated warm RTF, per-chunk timings, audio duration, native format, checksums, resume, and human listening.
- Seam: existing CLI render entry point and backend-neutral runner; reuse canonical preparation, chunking, manifest identity, WAV validation, concatenation, and resume.
- Boundary: current host is Apple M4/16 GB; do not claim M3 results. Local workspace has MLX 1.5 model and IndexTTS-2.5 PyTorch runtime; no usable MLX 2.5 model. Issue #6 owns emotion policy and Issue #7 owns peak/headroom policy.
- Artifacts: `.agentflow/artifacts/A-004-mlx-vs-indextts-benchmark/plan.md` and `tracker.md`; source spec committed as `420aabf`, GitHub Issue #8 published with `ready-for-agent`.
- Tracker validation: PASS. Actual changed paths are the new A-004 planning records and devlog; unrelated `docs/apple-audiobook-conversion.md` remains untouched.

# ← Reply / A-004
* _2026-09-20 10:05:00 (GPT-5)_

## [SUMMARY]

- 已將 Issue #8 的 MLX 1.5 vs IndexTTS-2.5 比較 spec 轉成 Agentflow 可恢復 execution plan。
- Plan 與 tracker 已建立，現階段只完成 planning record，尚未載入模型、執行 benchmark 或修改產品程式。
- T-1 是下一個安全動作：固定相同文字／prompt，確認兩個 runtime，並記錄實際 Apple Silicon host。

## [FINAL REPORT]

計畫位置：`.agentflow/artifacts/A-004-mlx-vs-indextts-benchmark/plan.md`。

Tracker 位置：`.agentflow/artifacts/A-004-mlx-vs-indextts-benchmark/tracker.md`，validation PASS。

GitHub spec：[#8 Benchmark MLX IndexTTS 1.5 against IndexTTS-2.5 on Apple Silicon](https://github.com/HOWARD1021/index-tts-audiobook/issues/8)，已加上 `ready-for-agent`。Spec commit：`420aabf`。

比較設計如下：

- 主比較：MLX 1.5 pause-only vs IndexTTS-2.5 MPS neutral/pause-only。
- 次要診斷：目前 IndexTTS-2.5 local-emotion，用來分離模型速度與 per-span synthesis overhead。
- 指標：cold model load、三次以上 warm run、per-chunk time、RTF、音檔時長、native format、checksum、resume、peak/headroom 與人工聽感。
- 既有 seam：CLI render、backend-neutral runner、canonical preparation、chunking、manifest、WAV validation、concatenation、resume。

邊界已固定：目前主機是 Apple M4／16 GB，不能把結果稱為 M3；現有 workspace 有 MLX 1.5 model 與 IndexTTS-2.5 PyTorch runtime，沒有可直接使用的 MLX 2.5 model。Issue #6 保留 emotion-policy 決策，Issue #7 保留 peak/headroom release gate。

Cross-check review: `.agentflow/artifacts/A-004-mlx-vs-indextts-benchmark/cross-check-report.md`
Cross-check implementation: 420aabf0571a70a722db871576a65612ec20ae06
Host gate: PASS

## Questions (batched — each with a suggested default)

- None. The next planned action is T-1 preflight.

---

# → Ask / A-005

godev

## [RUN-001] Event (during round A-005)

- Owner said `godev`; resumed A-004 Issue #8 benchmark execution at T-1.
- T-1 PASS: external preflight `/Users/howard/index-tts-workspace/previews/issue-8-benchmark-20260920` confirms MLX 1.5 runtime/model, IndexTTS-2.5 runtime/checkpoints, MPS availability, MLX GPU device, Apple M4/16 GB host, identical horseshoe prompt checksum `dd077517ab6558b5aab2cb785a2c6e47bf9450f94982cad35cf5f9a1f5366297`, and no audio before run.
- Fixed plain-text benchmark script SHA-256 is `09b52c1800afef10018ae1c20be9706c22e7027ffba345a28e301d6bd67b3437`. The prior `<著|ZHE5>` annotation is removed for primary cross-backend parity because MLX 1.5 has no pronunciation-annotation interface; this limitation is recorded in preflight.json.
- No checkpoint was loaded, no benchmark audio was generated, and no product source/preset/manuscript changed. Tracker T-1 checked; T-2 is next.

## [RUN-002] Event (during round A-005)

- T-2 PASS: added pure `BenchmarkRun`/summary/report contract at the backend-neutral seam with atomic JSON output. Focused red test first failed on missing module; implementation then passed 3 focused tests.
- Complete verification: 29 passed, 1 skipped; compileall PASS; offline Ruff PASS. No default backend, emotion vector, chunk setting, prompt, manuscript, or runtime changed.
- T-3 now starts only after tests: real primary runs will use external benchmark root and the T-1 plain-text parity script; all model/audio artifacts stay outside Git.

## [RUN-003] Event (during round A-005)

- T-3 PASS: MLX 1.5 pause-only cold + three warm runs and IndexTTS-2.5 MPS neutral pause-only cold + three warm runs completed in the external benchmark root. Both used identical script SHA-256 `09b52c1800afef10018ae1c20be9706c22e7027ffba345a28e301d6bd67b3437` and prompt SHA-256 `dd077517ab6558b5aab2cb785a2c6e47bf9450f94982cad35cf5f9a1f5366297`.
- MLX 1.5: cold load 0.694 s; warm median RTF 1.863 (range 1.732–2.726); native mono PCM16/24 kHz.
- IndexTTS-2.5 MPS: cold load 25.605 s; warm median RTF 4.105 (range 4.097–4.661); native mono PCM16/22.05 kHz. The measured median RTF ratio is 2.20x in favor of MLX 1.5 on this Apple M4 host.
- T-4 PASS: 32 chunk WAVs and 8 final WAVs pass finite/native-format/duration/checksum validation; objective-validation.json and comparison-report.json are written externally. MLX rail samples are 0%; IndexTTS-2.5 rail samples are 0.2815%.
- Resume evidence: unchanged artifact scan reused 32 validated chunk files with zero model loads and zero synthesis calls; existing render_chapter resume tests remain in the 29 passed / 1 skipped suite. No backend default or emotion preset changed.
- T-5 pending: listening.md names the paired warm outputs and naturalness-first questions. Faster MLX must still pass human audiobook listening before any follow-up recommendation.

## [WIP-001] Checkpoint (during round A-005)

- **Finished:** T-1 preflight, T-2 report seam/tests, T-3 real MLX/IndexTTS primary runs, and T-4 objective validation/resume scan.

  1. MLX 1.5 warm median RTF 1.863; IndexTTS-2.5 MPS warm median RTF 4.105.
  2. 32 chunk WAVs and 8 final WAVs pass native format, finite, duration, and checksum checks.
  3. Same script/prompt identity confirmed; M4/16 GB host recorded.

- **Running now:** No model process; external paired outputs and listening note are ready.

- **Still to do:** Human listening gate and naturalness-first recommendation.

- **Next work action:** Listen to the paired warm-2 outputs and record timestamped verdicts in listening.md.

- **Checks:** [x] tracker.md | [x] devlog RUN | [x] scope matches tracker

## [RUN-004] Event (during round A-005)

- Independent review initially BLOCKED T-2 because aggregate report runs omitted per-chunk timing, despite raw external logs containing it.
- Applied red-to-green correction: added typed `ChunkTiming`, per-chunk validation/serialization, and multi-backend grouping coverage. Focused benchmark tests now 5 passed; complete suite 31 passed / 1 skipped; compileall and Ruff PASS.
- Rebuilt the two external formal reports from unchanged raw model outputs so `runs[].chunk_timings` is now present; no model rerun was needed.
- Follow-up independent cross-check of implementation commit `08691b2572018ecb70fbacf3eca479e3ef3f810b` returned Outcome PASS, Minimality PASS, Conformance PASS, Verdict PASS. Report is stored under A-005 benchmark execution records.
- T-5 remains the only pending task and requires human listening of the paired warm outputs.

## [RUN-005] Event (during round A-005)

- Owner completed human listening on the fresh Yuanyuan-reference outputs. IndexTTS-2.5 is preferred for smoother audiobook delivery and fewer wrong characters; MLX 1.5 is not selected for the current narrator direction.
- Pronunciation failure: `伴隨著` still sounds like `ㄓㄨˋ` / `ZHU4` instead of the required `ㄓㄜ` / `ZHE5`, despite the existing `<著|ZHE5>` prepared-text override.
- Requirement update: future real-model tests must use the default Yuanyuan prompt (`index-tts/prompts/voice.wav`, byte-identical to `yuanyuan_vocals_30s.wav`) and include this exact word in the audio acceptance gate. Text-only assertions are insufficient.
- Candidate audio forms were generated externally: current annotation, direct `ZHE5`, and plain text. No override or runtime file was changed while the acoustic choice remains under review.
- Follow-up GitHub Issue #9 created with `ready-for-agent`: real-model Yuanyuan pronunciation regression and acceptance gate. Issue #6 remains emotion policy; Issue #7 remains headroom.
- T-5 is complete for Issue #8 with the pronunciation follow-up explicitly separated. Tracker validation remains required after final record update.

# ← Reply / A-005
* _2026-09-20 16:53:00 (GPT-5)_

## [SUMMARY]

- A-004/A-005 MLX 1.5 vs IndexTTS-2.5 benchmark 已完成，包含 T-1 至 T-5。
- 人工聽感選擇 IndexTTS-2.5：聲音較順、較適合有聲書，錯別字較少。
- `伴隨著` 發音仍失敗：實際聽到 `ㄓㄨˋ`，要求是 `ㄓㄜ`；已建立 Issue #9 作為獨立 pronunciation follow-up。

## [FINAL REPORT]

本輪比較使用預設圓圓 reference：
`/Users/howard/index-tts-workspace/index-tts/prompts/voice.wav`，與
`prompts/yuanyuan/yuanyuan_vocals_30s.wav` checksum 完全相同。

新生成的比較資料在：
`/Users/howard/index-tts-workspace/previews/issue-8-benchmark-yuanyuan-20260920/`。

- [MLX 1.5 圓圓 output](/Users/howard/index-tts-workspace/previews/issue-8-benchmark-yuanyuan-20260920/mlx-1.5/final.wav)：71.09 秒，RTF 1.54。
- [IndexTTS-2.5 圓圓 output](/Users/howard/index-tts-workspace/previews/issue-8-benchmark-yuanyuan-20260920/indextts-2.5/final.wav)：59.89 秒，RTF 6.54。

人工結果優先於速度結果：IndexTTS-2.5 暫定為較適合的 audiobook backend；MLX 1.5 不作為目前 narrator default。這不是因為速度，而是因為 2.5 聽起來更順、錯誤較少。

Pronunciation follow-up：[Issue #9 Make 伴隨著 pronunciation a real-model acceptance gate](https://github.com/HOWARD1021/index-tts-audiobook/issues/9)。Issue #9 明確要求：

- 所有 real-model pronunciation test 使用 Yuanyuan reference；
- fixture 必須包含 `伴隨著`；
- `ㄓㄜ` 必須透過實際 audio listening 驗收；
- 不能只靠 `ZHE5` 文字 assertion 宣稱通過。

已保存三個 Yuanyuan candidate audio：目前 annotation、direct `ZHE5`、plain text；在選定可聽的正確形式前，沒有修改 override 或 runtime。Issue #6 繼續負責 emotion policy，Issue #7 繼續負責 peak/headroom。

Cross-check review: `.agentflow/artifacts/A-005-benchmark-execution/cross-check-report.md`
Cross-check implementation: 08691b2572018ecb70fbacf3eca479e3ef3f810b
Host gate: PASS

## Questions (batched — each with a suggested default)

- None. Issue #9 owns the pronunciation correction and real-model acceptance gate.

---

# → Ask / A-006

yes 測試是成功的 我們 godev 排定計劃 接下來 該怎麼 重新生成之前生成的檔案 並且上傳到原本上傳的地方 測試檔案 也要移除

## [RUN-001] Event (during round A-006)

- Owner confirmed the pronunciation test successful and requested a godev plan for production rerender, original-destination publication, and test-artifact cleanup.
- Route: planning only. No production render, upload, overwrite, remote mutation, or deletion started.
- Plan boundary: freeze the successful Issue #9 pronunciation form and exact original destination before any generation; stage new output; validate; dry-run destination diff; publish; verify destination checksums; then clean only an explicit test-artifact allowlist.
- Read-only discovery found prior chapter WAVs in `/Users/howard/Music/Music/Media.localized/Music/Unknown Artist/Unknown Album/`, but no authoritative destination/object-key record was found in this repository. T-1 must resolve this ambiguity.
- Tracker validation PASS. Unrelated `docs/apple-audiobook-conversion.md` remains untouched.

# ← Reply / A-006
* _2026-09-20 17:00:00 (GPT-5)_

## [SUMMARY]

- 已建立正式 rerender → destination publish → test cleanup 的 A-006 godev 計劃。
- 目前只完成 planning record；沒有重新生成、上傳、覆蓋或刪除任何檔案。
- 第一個安全動作是 T-1：解析原本正式檔案與原始上傳目的地，並鎖定成功的 pronunciation form。

## [FINAL REPORT]

Plan：[.agentflow/artifacts/A-006-production-rerender-upload-cleanup/plan.md](/Users/howard/orca/index-tts-audiobook/.agentflow/artifacts/A-006-production-rerender-upload-cleanup/plan.md)

Tracker：[tracker.md](/Users/howard/orca/index-tts-audiobook/.agentflow/artifacts/A-006-production-rerender-upload-cleanup/tracker.md)，validation PASS。

流程固定為：

1. 凍結 production source、chapter output list、Yuanyuan prompt、成功 pronunciation form、原始 destination/object keys。
2. 用 IndexTTS-2.5 + Yuanyuan 生成到新的 staging 目錄，不原地覆蓋舊檔。
3. 驗證 WAV、manifest、checksum、headroom、pronunciation 與代表性聽感。
4. 先做 destination dry-run diff，再上傳／複製並逐檔驗證 destination checksum。
5. 只清理明確列出的 test artifacts；production、canonical manuscript、model、prompt、final manifest 保留。

唯讀掃描目前找到過去 chapter WAV 的 Music library 位置：
`/Users/howard/Music/Music/Media.localized/Music/Unknown Artist/Unknown Album/`。
但沒有把它直接假定為唯一原始目的地；T-1 會先從既有檔名、manifest、Music library 或原始 upload record 解析確切目標。若目的地或成功 pronunciation form 不明，會停在 upload 前，不會猜測。

Cross-check review: `.agentflow/artifacts/A-006-production-rerender-upload-cleanup/cross-check-report.md`
Cross-check implementation: 2fc11e9beb3a76573abdf9a568d740ecb64579ed
Host gate: PASS

## Questions (batched — each with a suggested default)

- None. The next planned action is T-1 read-only inventory.

---

# → Ask / A-007

下一步該怎麼做

## [RUN-001] Event (during round A-007)

- User asked for the next action after the A-006 production rerender/upload/cleanup plan.
- T-1 read-only inventory PASS: recovered source/scripts, 13 chapter IDs (00 foreword through 12), local audio/feed directory, publish script, R2 bucket `howard-audiobooks`, public base `https://pub-43dc4106670549999990fa09d26d8316.r2.dev`, and feed URL.
- Existing local destination contains WAV, M4A, manifests, chunks, and feed.xml; Music library copies were observed separately and are not treated as the canonical upload target.
- Yuanyuan reference path and checksum are frozen. Pronunciation form remains the only input gate pending Issue #9 candidate confirmation.
- No render, upload, overwrite, remote mutation, or deletion occurred. Production inventory is recorded in `production-inputs.json`; tracker validation remains required after the record update.

# ← Reply / A-007
* _2026-09-20 17:06:00 (GPT-5)_

## [SUMMARY]

- 下一步已完成 T-1 唯讀盤點：原始本地音訊目錄、13 集輸出清單與 R2 上傳目的地都已找回。
- 目前尚未重新生成、上傳、覆蓋或刪除任何檔案。
- 唯一仍需先鎖定的是 Issue #9 的成功 pronunciation form。

## [FINAL REPORT]

正式本地目錄：
`/Users/howard/Downloads/幽靈的禮物/volume-price-analysis-en-chapters/zh-simplified-tts/audio/`

原始發布設定已從 `publish_podcast.py` 與 `feed.xml` 恢復：

- R2 bucket：`howard-audiobooks`
- Public base：`https://pub-43dc4106670549999990fa09d26d8316.r2.dev`
- Feed：`https://pub-43dc4106670549999990fa09d26d8316.r2.dev/feed.xml`
- Chapter range：`00-foreword` 到 `12-chapter-twelve`，共 13 集
- 本地每集包含 `.wav`、`.m4a`、`.manifest.json`、`.chunks/`
- Yuanyuan prompt：`/Users/howard/index-tts-workspace/index-tts/prompts/voice.wav`
- Yuanyuan prompt SHA-256：`d8ba82bf2f84c2c0ff0ea03d8f9f2fcfef2ac0592a384381a4415fd8f53d71b7`

下一步順序：

1. 在 Issue #9 凍結真正聽對 `ㄓㄜ` 的 pronunciation form。
2. 在新的 staging 目錄重新生成 13 集，不覆蓋現有正式檔。
3. 驗證 WAV、M4A、manifest、checksum 與代表性聽感。
4. 對 `howard-audiobooks` 做 dry-run diff，確認 13 個 object key 與 feed 更新內容。
5. 上傳並逐檔驗證 R2 內容後，才清理明確 allowlist 內的 benchmark/test artifacts。

測試檔案會使用可恢復 Trash／明確 allowlist 清理，不會用廣泛 pattern 刪除，也不會碰 canonical source、model、prompt 或正式 production files。

Plan：[A-006 production rerender/upload/cleanup](/Users/howard/orca/index-tts-audiobook/.agentflow/artifacts/A-006-production-rerender-upload-cleanup/plan.md)

Inventory：[production-inputs.json](/Users/howard/orca/index-tts-audiobook/.agentflow/artifacts/A-006-production-rerender-upload-cleanup/production-inputs.json)

Cross-check review: `.agentflow/artifacts/A-007-destination-inventory/cross-check-report.md`
Cross-check implementation: e23414557d60a312a99faa884f975088a6b1ac2b
Host gate: PASS

## Questions (batched — each with a suggested default)

- None. The next execution gate is pronunciation-form freeze under Issue #9.

---

# → Ask / A-008

我們下一步要做的是不是先生成1集？

## [RUN-001] Event (during round A-008)

- Owner asked whether the next step should be one chapter first.
- Decision: yes. Use `04-chapter-four` as the pilot because it contains `伴隨著`, the Issue #9 pronunciation gate, and the previously reviewed styled passage.
- Pilot gate: freeze pronunciation form, render chapter 04 to new staging, validate and listen; only after PASS proceed to the remaining 12 chapters. No upload, overwrite, or test cleanup before pilot and full destination gates.
- Plan/tracker updated; no model loaded, production render, upload, or deletion occurred in this round.

# ← Reply / A-008
* _2026-09-20 17:10:00 (GPT-5)_

## [SUMMARY]

- 對，下一步先生成 1 集，不直接重生 13 集。
- Pilot 選第 04 章，因為它包含 `伴隨著`、Issue #9 pronunciation gate，以及之前驗收過的代表性內容。
- Pilot 通過 pronunciation、聲音、WAV/manifest/checksum 後，才生成剩餘 12 集。

## [FINAL REPORT]

A-006 plan 已更新為 pilot-first：

1. 凍結成功 pronunciation form、Yuanyuan prompt、chapter-04 source 與 staging output name。
2. 用 IndexTTS-2.5 + Yuanyuan 只生成 `04-chapter-four` 到新的 staging 目錄。
3. 驗證 WAV、manifest、checksum、headroom，並人工聽 `伴隨著` 與整體聲音。
4. Pilot PASS 後才生成其餘 12 集。
5. 全部 production files 驗證及 destination dry-run PASS 後，才上傳 R2。
6. 上傳 checksum 驗證完成後，才清理 allowlist 內的測試檔案。

目前沒有生成、上傳、覆蓋或刪除任何檔案。

Cross-check review: `.agentflow/artifacts/A-008-pilot-plan/cross-check-report.md`
Cross-check implementation: 3828041ba3ce303150bd38720a9b677af1c0db2f
Host gate: PASS

## Questions (batched — each with a suggested default)

- None. The next execution gate is the chapter-four pilot after pronunciation form freeze.

---

# → Ask / A-009

我們一些做測試的這些檔案，是不是可以先移除掉？

## [RUN-001] Event (during round A-009)

- Owner asked to remove some test files before production rerender.
- Cleanup PASS: moved only the two superseded failed Issue #5 preview directories to macOS Trash, preserving recoverability.
- Preserved final v3 evidence, both Issue #8 benchmark directories, and Yuanyuan pronunciation candidates because they remain needed for pilot/Issue #9.
- No production local audio, canonical source, prompt, model, R2 object, feed, or Music library file was touched. Cleanup receipt is `cleanup-receipt.json`.

# ← Reply / A-009
* _2026-09-20 17:26:00 (GPT-5)_

## [SUMMARY]

- 可以先移除已淘汰的測試檔案；兩個失敗 preview 目錄已移到 macOS Trash，可復原。
- 沒有碰 production audio、canonical source、prompt、model、R2、feed 或 Music library。
- Issue #5 v3 evidence、Issue #8 benchmark、Yuanyuan outputs 與 Issue #9 pronunciation candidates 都保留。

## [FINAL REPORT]

已移除到 Trash：

- `/Users/howard/index-tts-workspace/previews/issue-5-20260920`
- `/Users/howard/index-tts-workspace/previews/issue-5-20260920-v2`

保留：

- `issue-5-20260920-v3`：最終 Issue #5 evidence
- `issue-8-benchmark-20260920`：horseshoe prompt benchmark evidence
- `issue-8-benchmark-yuanyuan-20260920`：圓圓 backend comparison
- `issue-8-yuanyuan-pronunciation-20260920`：Issue #9 pronunciation candidates

Cleanup receipt：[cleanup-receipt.json](/Users/howard/orca/index-tts-audiobook/.agentflow/artifacts/A-006-production-rerender-upload-cleanup/cleanup-receipt.json)

原始 production 目錄與 R2 尚未變更。下一步仍是 chapter-four pilot，不會直接重生 13 集。

Cross-check review: `.agentflow/artifacts/A-009-test-cleanup/cross-check-report.md`
Cross-check implementation: 86f0ef26603d3720139519d01ea39fa7edde5e49
Host gate: PASS

## Questions (batched — each with a suggested default)

- None. Cleanup is complete for the superseded failed previews; production work remains gated by Issue #9 pronunciation form and chapter-four pilot.

---

# → Ask / A-010

好像其實也不用做前端業務。OK，我們去審覈一下目前的需求哪些東西還沒有完成吧。然後，如果完成之後，我們就直接來跑第四章的 pilot。

## [RUN-001] Event (during round A-010)

- Owner removed the frontend-monitor idea from scope and requested a requirements audit before chapter-four pilot.
- Audit result: destination, 13-chapter output list, Yuanyuan prompt, backend preference, and safe cleanup boundaries are proven. Pronunciation candidate freeze is the only pre-pilot blocker.
- Issue #6 emotion policy remains downstream; pilot can use IndexTTS-2.5 neutral/pause-only. Issue #7 headroom remains a release gate.
- Decision: do not load the model or start chapter-four generation until Issue #9 candidate form and Yuanyuan evidence are recorded. Requirements audit is `.agentflow/artifacts/A-010-requirements-audit/requirements-audit.md`.

# ← Reply / A-010
* _2026-09-20 17:46:00 (GPT-5)_

## [SUMMARY]

- 需求 audit 已完成；前端監控頁面正式列為 out of scope。
- 目的地、13 集 output list、Yuanyuan reference、IndexTTS-2.5 backend 與 cleanup boundary 都已確認。
- 目前不能直接跑 pilot，唯一缺口是 Issue #9 pronunciation candidate 尚未 frozen。

## [FINAL REPORT]

Audit：[requirements-audit.md](/Users/howard/orca/index-tts-audiobook/.agentflow/artifacts/A-010-requirements-audit/requirements-audit.md)

已完成：

- 找回正式本地 audio/feed 目錄。
- 找回 R2 bucket `howard-audiobooks` 與 public/feed URL。
- 確認 00 foreword 到 12 chapter，共 13 集。
- 確認 Yuanyuan prompt 與 checksum。
- 確認 IndexTTS-2.5 是下一輪 production backend。
- 確認 test cleanup 使用 allowlist + Trash。
- 確認不需要 frontend monitor 才能執行本次 delivery。

尚未完成：

- Issue #9 三種 pronunciation candidate 尚未選出並記錄為正式 production form。
- 第 04 章 pilot 尚未生成。
- Pilot validation、13 集 rerender、R2 upload、feed 更新、最終 cleanup 尚未開始。

因此下一步是：先把成功的 pronunciation candidate 凍結成 T-1 input，接著只生成第 04 章 pilot。Pilot 通過後才生成其餘 12 集。

Cross-check review: `.agentflow/artifacts/A-010-requirements-audit/cross-check-report.md`
Cross-check implementation: 1b5683f9644ff05bd8152a006868105f85d578e3
Host gate: PASS

## Questions (batched — each with a suggested default)

- None. The next execution gate is Issue #9 pronunciation-form freeze.

---

# → Ask / A-011

plain.wav：伴随着高成交量。這個可以

## [RUN-001] Event (during round A-011)

- Owner selected `plain.wav` as the accepted pronunciation candidate: plain text `伴随着高成交量。`.
- Production override was changed from explicit `<著|ZHE5>` annotation to the accepted plain-text `伴随着` form for both simplified source spellings.
- TDD evidence: updated text regression first failed against the old annotation output, then the minimal override fix passed. Runner expectation was updated; complete suite is 31 passed / 1 skipped, Ruff and compileall PASS.
- T-1 is now PASS: production-inputs.json status PASS, Yuanyuan checksum/destination/output list frozen. T-2 is next: stage only chapter 04 pilot.
- No model loaded, production output overwritten, R2 object changed, or test cleanup performed in this round.

## [RUN-002] Event (during round A-011)

- Godev pronunciation audit completed across 13 Simplified-Chinese scripts: 244 `著／着` occurrences; 184 candidate neutral `ㄓㄜ`, 35 clear `ㄓㄨˋ`, 2 `ㄓㄨㄛˊ`/context-review, and 23 unknown contexts.
- Decision: no global character replacement. Future full-book production requires phrase-level lexicon, unknown-context classification, and real Yuanyuan listening evidence per pronunciation class.
- Audit summary is `.agentflow/artifacts/A-011-pronunciation-audit/pronunciation-audit-summary.md`; full JSON remains external. Issue #9 was updated with the counts and gate.
- Chapter-four pilot continues in external staging; its PASS cannot certify the 23 unknown contexts.

## [WIP-001] Checkpoint (during round A-011)

- **Finished:** Frozen plain-text pronunciation override and full 13-script `著／着` audit; audit found 244 occurrences with 23 unknown contexts.

  1. Focused pronunciation regression and full suite pass after the plain-text override.
  2. Issue #9 updated with phrase-level lexicon and unknown-context gate.
  3. Chapter-four pilot staging has model load PASS and five completed chunks.

- **Running now:** IndexTTS-2.5 + Yuanyuan chapter-four pilot in external staging; no production destination mutation.

- **Still to do:** Complete 149-chunk pilot, validate/listen, classify unknown pronunciation contexts before full-book production.

- **Next work action:** Monitor pilot progress and preserve resumable artifacts; do not start remaining chapters.

- **Checks:** [x] tracker.md | [x] devlog RUN | [x] scope matches tracker

## [RUN-003] Event (during round A-011)

- Plain-text pronunciation fix implementation commit `60f2a6b` received independent cross-check PASS (Outcome/Minimality/Conformance/Verdict).
- Full 31-pass suite and lint checks remain green. The phrase-level override is limited to `伴随著`/`伴随着`; no global `著／着` replacement was introduced.
- Audit keeps 23 unknown contexts visible; full-book production remains blocked until those contexts are classified. Chapter-four pilot continues independently as the bounded pilot.

## [RUN-004] Event (during round A-011)

- Owner requested a pause while sleeping.
- Pilot process stopped with SIGINT; staging and manifest are preserved. Pilot-run status is interrupted/failed by intentional pause, not a synthesis error.
- Resume point: 66 validated outer chunks, 119 completed synthesis calls, no partial WAV remains. Next safe action is to resume from the in-progress manifest; do not restart or delete staging.

## [RUN-005] Event (during round A-011)

- Chapter-four pilot resumed and completed successfully after the pause.
- Objective result: 149 outer chunks, 157 synthesis calls, 56:59.21 mono PCM16/22050 WAV, SHA-256 `d3c56434e65ba5888a0173606b09ce669f48a781d8c8effbc99cf7014ad6a847`.
- Manifest/checksum/finite/WAV gates PASS; plain `伴随着` appears 6 times in backend text and `<著|ZHE5>` appears 0 times. Rail samples are 0.0712%.
- No production destination, R2 object, canonical source, or test cleanup was touched. Human listening is now the only T-3 gate before remaining chapters.

## [RUN-006] Event (during round A-011)

- Resumed chapter-four pilot completed successfully after the sleep pause.
- Final staged output: 149 outer chunks / 157 synthesis calls; 56:59.21 mono PCM16/22050 WAV; SHA-256 `d3c56434e65ba5888a0173606b09ce669f48a781d8c8effbc99cf7014ad6a847`.
- Objective validation PASS: manifest complete, all chunk checksums PASS, finite samples PASS, plain `伴随着` present 6 times, `<著|ZHE5>` absent, rail samples 0.0712%.
- No production destination, R2 object, canonical source, or test cleanup touched. Human pilot listening is the only remaining gate before remaining chapters.

## [RUN-007] Event (during round A-011)

- Owner listening located two pacing issues: `第四章` standalone chunk around 00:01 is too slow; isolated bold `不是` around 01:30 is too slow.
- Pilot uses zero emotion vectors and `use_qwen_emo=false`; source has no laughter cue. Pleasant laugh-like prosody is not attributed to configured emotion yet.
- Root-cause direction: short heading/short emphasis span synthesis, not global speed. Issue #6 received timestamped findings and recommendations to merge headings, promote short emphasis to sentence context, and avoid global speed changes until those tests pass.
- Full-book production remains paused; no destination/upload/cleanup changes.
