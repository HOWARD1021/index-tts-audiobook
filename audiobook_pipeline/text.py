"""Canonical-source to reviewed-narration text preparation."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from opencc import OpenCC

HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s*", re.MULTILINE)
THEMATIC_BREAK_RE = re.compile(r"(?m)^[ \t]*(?:\*{3,}|-{3,}|_{3,})[ \t]*$\n?")
PRONUNCIATION_OVERRIDES = {
    "伴随著": "伴随<著|ZHE5>",
    "伴随着": "伴随<着|ZHE5>",
}
MARKDOWN_EMPHASIS_RE = re.compile(
    r"(?<!\*)\*{1,3}([^*\n]+?)\*{1,3}(?!\*)"
    r"|(?<!_)_{1,3}([^_\n]+?)_{1,3}(?!_)"
)
SPEECH_CUE_RE = re.compile(
    r"[\[【（(]\s*(?:笑声?|哭声?|叹气|叹息|咳嗽?|喘气|吸气|呼气|音效|音乐|停顿|沉默)"
    r"\s*[\]】）)]"
)
SPEECH_CUE_LINE_RE = re.compile(
    r"(?m)^[ \t]*"
    r"[\[【（(]\s*(?:笑声?|哭声?|叹气|叹息|咳嗽?|喘气|吸气|呼气|音效|音乐|停顿|沉默)"
    r"\s*[\]】）)]\s*\n?"
)
NON_SPOKEN_DELIMITER_RE = re.compile(r"[『』「」“”‘’（）()【】]")
FILLER_AT_BOUNDARY_RE = re.compile(
    r"(?m)(?:^|(?<=[。！？!?；;：:\n…—]))[ \t]*"
    r"(?:嗯+|呃+|啊+|哦+|喔+|哎+|唉+)"
    r"(?:[ \t]*[，,、：:])?[ \t]*"
)
EMPHASIS_START = "\ue000"
EMPHASIS_END = "\ue001"
EMPHASIS_MARKER_RE = re.compile(
    rf"{re.escape(EMPHASIS_START)}([BI])|{re.escape(EMPHASIS_END)}"
)


@dataclass(frozen=True)
class NarrationSpan:
    """Clean narration text plus optional Markdown-derived emphasis metadata."""

    text: str
    emphasis: str | None = None


@dataclass(frozen=True)
class PreparedNarration:
    """Prepared spans used by both review output and emotion-aware rendering."""

    spans: tuple[NarrationSpan, ...]

    @property
    def text(self) -> str:
        return "".join(span.text for span in self.spans)

    @property
    def marked_text(self) -> str:
        parts: list[str] = []
        for span in self.spans:
            if span.emphasis is None:
                parts.append(span.text)
                continue
            marker = "B" if span.emphasis == "bold" else "I"
            parts.append(f"{EMPHASIS_START}{marker}{span.text}{EMPHASIS_END}")
        return "".join(parts)


def convert_traditional_to_simplified(
    text: str,
    glossary: Mapping[str, str] | None = None,
) -> str:
    """Convert text while protecting explicit glossary entries.

    Glossary keys are protected before conversion so that a deliberate output
    pronunciation or lexical choice is not changed by OpenCC. Longest keys are
    replaced first to avoid a shorter phrase consuming part of a longer one.
    """

    glossary = glossary or {}
    protected: dict[str, str] = {}
    converted = text
    for index, source in enumerate(sorted(glossary, key=len, reverse=True)):
        marker = f"AUDIOGLOSSARYTOKEN{index}AUDIOGLOSSARYTOKEN"
        if source in converted:
            converted = converted.replace(source, marker)
            protected[marker] = glossary[source]

    converted = OpenCC("t2s").convert(converted)
    for marker, replacement in protected.items():
        converted = converted.replace(marker, replacement)
    return converted


def remove_speech_headings(text: str) -> str:
    """Remove Markdown heading markers while retaining heading wording."""

    return HEADING_RE.sub("", text)


def apply_pronunciation_overrides(text: str) -> str:
    """Apply deterministic pronunciation fixes for known ambiguous phrases."""

    for source, replacement in PRONUNCIATION_OVERRIDES.items():
        text = text.replace(source, replacement)
    return text


def _preserve_markdown_emphasis(text: str) -> str:
    """Replace Markdown emphasis delimiters with private span markers."""

    def replace(match: re.Match[str]) -> str:
        raw = match.group(0)
        content = match.group(1) or match.group(2) or ""
        style = "B" if raw.startswith(("**", "__")) else "I"
        return f"{EMPHASIS_START}{style}{content}{EMPHASIS_END}"

    return MARKDOWN_EMPHASIS_RE.sub(replace, text)


def _parse_emphasis_markers(text: str) -> tuple[NarrationSpan, ...]:
    spans: list[NarrationSpan] = []
    cursor = 0
    emphasis: str | None = None
    for match in EMPHASIS_MARKER_RE.finditer(text):
        if match.start() > cursor:
            spans.append(
                NarrationSpan(
                    text[cursor : match.start()],
                    emphasis,
                )
            )
        if match.group(1):
            if emphasis is not None:
                raise ValueError("nested Markdown emphasis is not supported")
            emphasis = "bold" if match.group(1) == "B" else "italic"
        else:
            if emphasis is None:
                raise ValueError("unmatched Markdown emphasis end marker")
            emphasis = None
        cursor = match.end()
    if cursor < len(text):
        spans.append(NarrationSpan(text[cursor:], emphasis))
    if emphasis is not None:
        raise ValueError("unmatched Markdown emphasis start marker")
    return tuple(span for span in spans if span.text)


def parse_narration_markers(text: str) -> tuple[NarrationSpan, ...]:
    """Decode internal emphasis markers without exposing them to a backend."""

    return _parse_emphasis_markers(text)


def prepare_narration_document(
    text: str,
    glossary: Mapping[str, str] | None = None,
    *,
    remove_headings: bool = True,
) -> PreparedNarration:
    """Prepare clean text while retaining emphasis as non-spoken metadata."""

    prepared = convert_traditional_to_simplified(text, glossary)
    if remove_headings:
        prepared = remove_speech_headings(prepared)
    prepared = _preserve_markdown_emphasis(prepared)
    prepared = apply_pronunciation_overrides(prepared)
    prepared = remove_narration_markup(prepared)
    prepared = prepared.replace("\r\n", "\n").replace("\r", "\n")
    spans = _parse_emphasis_markers(prepared.strip() + "\n")
    return PreparedNarration(spans)


def remove_narration_markup(text: str) -> str:
    """Remove non-spoken Markdown emphasis and explicit speech cues."""

    text = THEMATIC_BREAK_RE.sub("", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = MARKDOWN_EMPHASIS_RE.sub(
        lambda match: match.group(1) or match.group(2) or "", text
    )
    text = SPEECH_CUE_LINE_RE.sub("", text)
    text = SPEECH_CUE_RE.sub("", text)
    text = NON_SPOKEN_DELIMITER_RE.sub("", text)
    return FILLER_AT_BOUNDARY_RE.sub("", text)


def prepare_narration_text(
    text: str,
    glossary: Mapping[str, str] | None = None,
    *,
    remove_headings: bool = True,
) -> str:
    """Create the narration representation without changing paragraph order."""

    return prepare_narration_document(
        text,
        glossary,
        remove_headings=remove_headings,
    ).text


def prepare_file(
    source: str | Path,
    destination: str | Path,
    glossary: Mapping[str, str] | None = None,
    *,
    remove_headings: bool = True,
) -> None:
    """Prepare a source file into a separately reviewable narration file."""

    source_path = Path(source)
    destination_path = Path(destination)
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    destination_path.write_text(
        prepare_narration_text(
            source_path.read_text(encoding="utf-8"),
            glossary,
            remove_headings=remove_headings,
        ),
        encoding="utf-8",
    )
