"""Paragraph-preserving text chunking for resumable synthesis."""

from __future__ import annotations

import re
from dataclasses import dataclass

SENTENCE_BOUNDARY_RE = re.compile(r"(?<=[。！？!?；;])\s*")
CHAPTER_HEADING_RE = re.compile(r"第[0-9一二三四五六七八九十百]+章$")


@dataclass(frozen=True)
class TextChunk:
    index: int
    text: str

    @property
    def characters(self) -> int:
        return len(self.text)


def _hard_split(text: str, limit: int) -> list[str]:
    return [text[start : start + limit] for start in range(0, len(text), limit)]


def _split_paragraph(paragraph: str, limit: int) -> list[str]:
    if len(paragraph) <= limit:
        return [paragraph]

    pieces: list[str] = []
    current = ""
    for sentence in SENTENCE_BOUNDARY_RE.split(paragraph):
        if not sentence:
            continue
        candidate = f"{current}{sentence}" if current else sentence
        if len(candidate) <= limit:
            current = candidate
            continue
        if current:
            pieces.append(current)
        if len(sentence) <= limit:
            current = sentence
        else:
            hard_parts = _hard_split(sentence, limit)
            pieces.extend(hard_parts[:-1])
            current = hard_parts[-1]
    if current:
        pieces.append(current)
    return pieces


def split_text(text: str, max_chars: int = 400) -> list[TextChunk]:
    """Split text into stable, non-empty, paragraph-preserving chunks."""

    if max_chars <= 0:
        raise ValueError("max_chars must be positive")

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if (
        len(paragraphs) >= 2
        and CHAPTER_HEADING_RE.fullmatch(paragraphs[0])
        and len(paragraphs[0]) + 1 + len(paragraphs[1]) <= max_chars
    ):
        paragraphs = [f"{paragraphs[0]}\n{paragraphs[1]}", *paragraphs[2:]]
    pieces: list[str] = []
    for paragraph in paragraphs:
        pieces.extend(_split_paragraph(paragraph, max_chars))
    return [TextChunk(index=i, text=piece) for i, piece in enumerate(pieces, start=1)]
