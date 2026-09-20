# Frozen spec cross-check

Stage: cross-check; route: external-runner-v1; profile: codex-default; tier: better.
Review the exact documentation commit `420aabf` in a disposable no-remote clone.
Read the benchmark spec, the existing backend/runner/test documentation, and
the current conversation facts: the local workspace has MLX IndexTTS 1.5 and
IndexTTS-2.5 PyTorch/MPS, no usable MLX 2.5 model, and the current host is
Apple M4/16 GB. Confirm that the spec accurately separates pause-only primary
comparison from the optional IndexTTS-2.5 local-emotion diagnostic.

Check that the plan preserves existing seams, does not promise unmeasured M3
results, keeps private runtime/audio artifacts outside Git, records cold and
warm timing separately, treats MLX 1.5's lack of local emotion vectors as a
capability boundary, and leaves Issue #6 and Issue #7 ownership intact.
Do not modify source, configuration, dependencies, runtime files, benchmark
artifacts, or the live checkout. Do not invoke Agentflow, delegate, commit, or
push. Only write `cross-check-report.md` in the disposable clone.

Scope discipline — implement exactly the ask; park everything else as a proposal. The ask's scope is the spec and planning record for Issue #8. Do not refactor, rename, reformat, add dependencies, or repair adjacent behavior unless the spec requires it.

Report first line: fresh Asia/Taipei `* _YYYY-MM-DD HH:MM:SS (gpt-5.6-terra/high)_`.
Include `Reviewed implementation commit: 420aabf` and exactly one each of
`Outcome: PASS|BLOCKING`, `Minimality: PASS|BLOCKING`, `Conformance: PASS|BLOCKING`,
and `Verdict: PASS|BLOCKING`. End with exactly one `Self-check:` line.
