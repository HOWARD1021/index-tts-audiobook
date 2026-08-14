"""Canonical-source to reviewed-narration text preparation."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Mapping

from opencc import OpenCC


HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s*", re.MULTILINE)


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


def prepare_narration_text(
    text: str,
    glossary: Mapping[str, str] | None = None,
    *,
    remove_headings: bool = True,
) -> str:
    """Create the narration representation without changing paragraph order."""

    prepared = convert_traditional_to_simplified(text, glossary)
    if remove_headings:
        prepared = remove_speech_headings(prepared)
    prepared = prepared.replace("\r\n", "\n").replace("\r", "\n")
    return prepared.strip() + "\n"


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
