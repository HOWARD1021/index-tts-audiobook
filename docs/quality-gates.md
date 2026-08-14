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
- mono PCM 16-bit at 22,050 Hz;
- non-empty with finite samples;
- within the broad duration sanity limit for its text length.

The duration check is deliberately broad. It is a runaway detector, not a
speaking-rate evaluator.

## Resume gate

A chunk may be skipped only when its text identity and generation settings still
match the current run and its WAV passes the audio gate. Otherwise it must be
regenerated.
