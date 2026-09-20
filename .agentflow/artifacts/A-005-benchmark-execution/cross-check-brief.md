# Frozen benchmark seam cross-check

Stage: cross-check; route: external-runner-v1; profile: codex-default; tier: better.
Review implementation commit `08691b2572018ecb70fbacf3eca479e3ef3f810b` in a disposable no-remote clone.
Read the benchmark module and tests, Issue #8 spec, A-004 plan/tracker, and
the existing runner/backend tests. Confirm that the new report seam correctly
separates cold model-load time from warm RTF, validates timing values, groups
backends, preserves identity fields, writes atomically, and tests only
external behavior. Confirm no product defaults or runtime behavior changed.

The real external benchmark artifacts are at
`/Users/howard/index-tts-workspace/previews/issue-8-benchmark-20260920`; do not
load models or modify those artifacts. The current host is Apple M4/16 GB;
never describe it as M3. MLX 1.5 has no local emotion-vector interface.

Do not modify source, configuration, dependencies, notebooks, runtime files,
or live artifacts. Do not invoke Agentflow, delegate, commit, or push. Only
write `cross-check-report.md` in the disposable clone.

Scope discipline — implement exactly the ask; park everything else as a proposal. The ask's scope is the Issue #8 benchmark report seam and tests. Do not refactor, rename, reformat, add dependencies, or repair adjacent behavior unless the ask requires it.

Report first line: fresh Asia/Taipei `* _YYYY-MM-DD HH:MM:SS (gpt-5.6-terra/high)_`.
Include `Reviewed implementation commit: 08691b2572018ecb70fbacf3eca479e3ef3f810b`
when reporting. Include exactly one each of Outcome, Minimality, Conformance,
and Verdict with PASS or BLOCKING. End with exactly one Self-check line.
