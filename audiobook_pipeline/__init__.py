"""Long-form audiobook orchestration for an external IndexTTS checkout."""

from .audio import AudioValidation, validate_wav
from .chunking import TextChunk, split_text
from .text import (
    NarrationSpan,
    PreparedNarration,
    prepare_narration_document,
    prepare_narration_text,
)

__all__ = [
    "AudioValidation",
    "NarrationSpan",
    "PreparedNarration",
    "TextChunk",
    "prepare_narration_document",
    "prepare_narration_text",
    "split_text",
    "validate_wav",
]
