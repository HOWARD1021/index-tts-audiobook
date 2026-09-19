* _2026-09-19 22:56:39 (gpt-5.4/high)_

# Local Markdown emotion design

## Outcome

Markdown emphasis is treated as non-spoken metadata. Ordinary text uses the
base emotion vector, bold spans use `bold_vector`, and italic spans use
`italic_vector`. The delimiters never reach an IndexTTS backend.

## Smallest seam

`audiobook_pipeline.text` owns canonical preparation and returns
`PreparedNarration` with `NarrationSpan` values. `runner` owns span-level audio
segmentation and joins validated span WAVs into one resumable chunk. Backend
adapters receive an optional vector and alpha without changing their model
loading lifecycle.

## Invariants

- Traditional-to-Simplified conversion, speech cleanup, delimiter removal, and
  pronunciation overrides happen before synthesis.
- Meaningful punctuation remains in span text for natural prosody.
- Plain review text contains no Markdown markers or internal span tokens.
- Manifest reuse is invalidated when styled source text changes.
- A styled chunk is validated only after its span WAVs are joined.

## Rejected

- Passing `**` or `*` into IndexTTS | the model does not interpret Markdown as
  local emotion and may speak the symbols.
- Applying one vector to the entire chunk | loses the local emphasis requested
  by the source markup.
- Adding a new dependency for Markdown parsing | the supported syntax is small
  and the existing regex path keeps the pipeline dependency-free.

## Verification plan

- Red/green unit tests for span extraction and per-span emotion propagation.
- Complete `pytest` suite.
- Real chapter planning scan proving no raw markers remain and pronunciation
  annotations survive.

Self-check: design matches the current owner request and limits local emotion to explicit Markdown emphasis.
