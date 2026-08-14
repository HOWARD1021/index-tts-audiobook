# Contributing

## Branch policy

`main` is the primary development branch for this repository and is also the
GitHub default branch. Put all durable audiobook-pipeline work there:

- pipeline program code;
- checked-in configuration and packaging metadata;
- automated tests; and
- developer and user documentation.

For work that benefits from review, create a short-lived branch from `main`
and merge it back into `main` when complete. Do not create or maintain a
separate long-lived `develop` branch. The repository is intentionally kept
small and reviewable, so a clean `main` is the source of truth for future
development.

## What stays out of Git

The following are local or private runtime inputs and outputs, not project
source:

- IndexTTS checkpoints, downloaded model files, and virtual environments;
- private speaker-reference WAV files and narration prompts;
- generated chunk WAVs, chapter audio, and manifests from local renders;
- source manuscripts and book corpora; and
- temporary work directories, caches, agent checkpoints, and session prompts.

Pass the external IndexTTS checkout with `--project-root` at render time. Keep
manuscripts, speaker references, and generated audio outside this repository;
the ignore rules are a safety net, not a replacement for that boundary.

## Verification before commit

Run the repository checks from the project root:

```bash
uv run pytest -q
uv run python -m compileall -q audiobook_pipeline
git diff --check
```

Keep commits focused on the pipeline and include the relevant tests and
documentation with the implementation.
