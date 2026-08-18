# Audiobook quality gates

The pipeline must pass these gates before a chapter is packaged.

## Text gate

- The Traditional source is preserved.
- The Simplified narration script is generated deterministically.
- Paragraph order is unchanged.
- English names, quotations, URLs, numbers, and financial notation are reviewed.
- Glossary overrides and Pinyin annotations are reviewed for high-risk terms.

## Preview gate

Listen to representative passages covering:

- ordinary prose;
- chapter headings and quotations;
- English names and book titles;
- numbers and dates;
- financial vocabulary;
- polyphonic characters.

Do not start a full-book render until the preview is intelligible.

## Audio gate

Every chunk must be:

- readable as WAV;
- mono PCM 16-bit at the selected backend's rate: 22,050 Hz for IndexTTS-2.5
  and 24,000 Hz for MLX IndexTTS 1.5;
- non-empty with finite samples;
- within the broad duration sanity limit for its text length.

The duration check is deliberately broad. It is a runaway detector, not a
speaking-rate evaluator.

## Resume gate

A chunk may be skipped only when its text hash, backend, model path, prompt hash,
sampling and chunking settings, and output format still match the current run;
its WAV checksum and audio gate must also pass. Otherwise it is regenerated.
