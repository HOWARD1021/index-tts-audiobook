# Emotion-aware Markdown narration for IndexTTS audiobooks

## Problem Statement

Audiobook source material is written as Markdown and often contains Traditional
Chinese, Markdown emphasis, quotation delimiters, speech cues, pronunciation
ambiguities, and financial terminology. If the raw source is sent directly to
TTS, the narrator may speak formatting marks such as `**`, `『』`, or brackets,
or produce an unintended pronunciation such as reading the `著` in
`伴隨著` with the wrong tone.

The source also uses emphasis to communicate meaning. In a sentence such as
「價格的小幅上漲是由**巨大的成交量**產生的」, the bold phrase is not merely
visual formatting: it tells the narrator which idea deserves more vocal energy.
The pipeline therefore needs to remove non-spoken syntax without discarding the
semantic emphasis it carries.

The project supports two synthesis backends. IndexTTS-2.5 accepts explicit
emotion vectors on each inference request. MLX IndexTTS 1.5 currently has no
emotion-vector interface, so silently pretending to apply local emotion on that
backend would produce misleading output.

## Solution

Create one canonical narration-preparation and rendering workflow:

1. Load the canonical source without mutating it.
2. Convert Traditional Chinese to Simplified Chinese while protecting explicit
   glossary choices.
3. Capture Markdown bold and italic as narration-span metadata before removing
   their delimiters.
4. Remove non-spoken Markdown, quote and parenthesis delimiters, speech cues,
   filler words, thematic breaks, and other known non-spoken markers.
5. Preserve meaningful punctuation such as `，。！？……——` for natural pauses
   and intonation.
6. Apply reviewed pronunciation overrides, including the light-tone annotation
   for `伴隨著`.
7. Split the prepared narration into resumable chunks without losing an active
   emphasis span at a chunk boundary.
8. Render ordinary, bold, and italic spans with their respective emotion
   vectors through IndexTTS-2.5, then join the validated span WAVs with a short
   local pause.
9. Store clean text, markup identity, sampling parameters, and WAV checksums in
   the manifest so a changed emphasis profile or source marker invalidates
   stale audio.
10. Reject styled source early when the MLX 1.5 backend is selected, because it
    cannot fulfill the local-emotion contract.

## User Stories

1. As an audiobook author, I want to pass a raw Markdown chapter to the render
   command, so that I do not have to remember a separate cleanup command.
2. As an audiobook author, I want Traditional Chinese converted to Simplified
   Chinese before synthesis, so that the selected Mandarin voice receives the
   reviewed language form.
3. As an audiobook author, I want the original manuscript preserved, so that
   narration preparation never destroys my canonical source.
4. As an audiobook author, I want Markdown heading, bold, and italic delimiters
   removed from spoken text, so that the narrator never says formatting syntax.
5. As an audiobook author, I want bold and italic semantics retained as
   metadata, so that visual emphasis can become vocal emphasis.
6. As an audiobook author, I want ordinary text to use a stable base emotion,
   so that local emphasis does not make every sentence sound excited.
7. As an audiobook author, I want bold text to use a configurable stronger
   emotion vector, so that phrases such as 「巨大的成交量」 receive deliberate
   emphasis.
8. As an audiobook author, I want italic text to use a configurable reflective
   or restrained emotion vector, so that italic commentary does not sound like
   shouting.
9. As an audiobook author, I want punctuation that carries prosody preserved,
   so that commas, questions, exclamations, ellipses, and dashes guide natural
   delivery.
10. As an audiobook author, I want quotation and bracket delimiters removed
    while their meaningful contents remain, so that `『震盪』` becomes
    「震盪」 in speech without losing the term.
11. As an audiobook author, I want speech cues and filler words removed, so
    that `（嘆氣）`, `【音效】`, and unnecessary `嗯` do not become awkward
    spoken artifacts.
12. As an audiobook author, I want known polyphonic pronunciations corrected,
    so that `伴隨著` uses the intended light-tone `zhe` pronunciation.
13. As an audiobook author, I want long emphasis spans to cross chunk
    boundaries safely, so that chunk size does not change their emotion state.
14. As an audiobook author, I want each styled span rendered through the same
    speaker reference, so that local emotion changes do not change the narrator
    identity.
15. As an audiobook author, I want local span joins to use a small predictable
    pause, so that separate emotion renders do not collapse into unintelligible
    words.
16. As an audiobook author, I want chunk WAVs validated before joining, so that
    one failed span cannot produce a corrupt chapter.
17. As an audiobook author, I want manifests to include the cleaned text and
    markup identity, so that changing Markdown style or an emotion vector
    regenerates the affected audio.
18. As an audiobook author, I want a clear error when I select MLX 1.5 with
    styled source, so that I do not mistake a plain rendering for an emotional
    rendering.
19. As an audiobook author, I want the workflow to remain resumable, so that a
    long chapter does not need to restart after one failed span.
20. As an audiobook maintainer, I want text parsing, chunk orchestration, and
    backend invocation separated by small interfaces, so that pronunciation
    and emotion behavior can be tested without loading a model.
21. As an audiobook maintainer, I want deterministic vector selection with
    `use_random=false`, so that preview comparisons are repeatable.
22. As an audiobook maintainer, I want a real-model preview gate, so that
    passing unit tests is not confused with natural-sounding audio.
23. As an audiobook maintainer, I want short emphasis spans to be reviewable
    for seam artifacts, so that sentence-level emphasis can replace phrase-level
    rendering when it sounds more natural.

## Implementation Decisions

- The text-preparation module exposes a prepared narration document composed of
  clean text spans and optional `bold` or `italic` emphasis metadata. The flat
  prepared-text interface remains available for review files and compatibility.
- Markdown semantics are extracted before cleanup. Delimiters are never passed
  to a backend; the metadata is carried separately through chunk planning.
- The runner is the highest existing seam for local emotion application. It
  creates one backend session, renders each styled span with a selected vector,
  validates the span WAV, and joins the span WAVs into one chunk WAV.
- The backend synthesis interface accepts an optional emotion vector and alpha.
  IndexTTS-2.5 maps these values to `emo_vector` and `emo_alpha` on every
  inference request.
- Base, bold, and italic profiles are explicit configuration values. The
  default bold profile is bright and energetic; the default italic profile is
  calm and reflective. Profiles can be changed without changing parsing logic.
- A short local join pause is configuration, not a hidden constant in the
  backend adapter.
- Meaningful punctuation remains text. The pipeline does not reinterpret every
  exclamation mark or question mark as an emotion vector; punctuation supplies
  prosody, while Markdown emphasis supplies explicit local emotion metadata.
- Pronunciation overrides remain deterministic and reviewed. The `伴隨著`
  override uses IndexTTS-2.5's supported light-tone annotation rather than
  changing the visible spoken wording.
- Chunk manifests include both clean text identity and styled-source identity,
  so a formatting-only emotion change cannot reuse stale WAV output.
- MLX 1.5 remains supported for plain narration, but styled source is rejected
  until its adapter exposes a real emotion-control interface.

## Testing Decisions

- Tests assert observable narration behavior, not private regular-expression
  structure. A good text test verifies the resulting clean text and the span
  style metadata.
- Text-module tests cover Traditional-to-Simplified conversion, Markdown and
  delimiter cleanup, speech-cue removal, pronunciation overrides, bold/italic
  span extraction, and unmatched/nested marker behavior.
- Runner tests use the existing fake synthesis adapter to verify that ordinary,
  bold, and italic spans receive the expected vectors and that joined chunks are
  validated.
- Runner tests cover emphasis spans that cross chunk boundaries and verify the
  local style is carried into subsequent chunks.
- Manifest tests verify that styled-source identity affects resume behavior.
- Backend tests verify that IndexTTS-2.5 receives the selected vector and alpha;
  MLX tests verify its explicit local-emotion rejection path.
- Existing project prior art is the fake-backend render suite, WAV validation
  suite, text-preparation regression suite, and opt-in real MLX smoke test.
- The release gate requires at least one real IndexTTS-2.5 preview containing
  ordinary text, a bold span, an italic span, a pronunciation override, and a
  span crossing a chunk boundary. Human listening must assess joins and whether
  the chosen vectors sound intentional.

## Out of Scope

- Automatically inferring emotion from arbitrary punctuation.
- Using QwenEmotion text inference as the default path.
- Making MLX IndexTTS 1.5 emulate emotion vectors without a supported model
  interface.
- Automatic waveform gain or loudness normalization as a substitute for vocal
  emotion.
- Rewriting sentence meaning, correcting translation quality, or inventing
  missing prose during narration preparation.
- Mutating source manuscripts, private prompts, model checkpoints, or generated
  full-book audio as part of preparation.
- Treating every short bold phrase as acoustically ideal; sentence-level
  fallback remains a listening-driven quality decision.

## Further Notes

The current implementation already contains the core span metadata, local
vector routing, chunk-boundary state, pronunciation cleanup, and MLX guard. The
next practical step is a real IndexTTS-2.5 preview render and listening review
using the chapter-four passage with `**巨大的成交量**`, `伴隨著`, and a second
italic span. The result should determine whether the default 80 ms local join
and phrase-level rendering need to be replaced by sentence-level emphasis.
