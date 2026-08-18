"""Command-line entry points for preparation, planning, validation, and render."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .audio import validate_wav
from .backends import BACKEND_NAMES, INDEXTTS_25, output_format_for
from .config import load_config, with_overrides
from .runner import plan_chapter, render_chapter
from .text import prepare_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="audiobook")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser(
        "prepare", help="derive a Simplified narration script"
    )
    prepare.add_argument("--input", required=True)
    prepare.add_argument("--output", required=True)
    prepare.add_argument("--keep-headings", action="store_true")

    plan = subparsers.add_parser("plan", help="inspect chunks without loading a model")
    plan.add_argument("--script", required=True)
    plan.add_argument("--config")
    plan.add_argument("--max-chars", type=int)

    validate = subparsers.add_parser("validate", help="validate a generated WAV")
    validate.add_argument("--wav", required=True)
    validate.add_argument("--text-chars", type=int)
    validate.add_argument("--config")
    validate.add_argument("--backend", choices=BACKEND_NAMES, default=INDEXTTS_25)

    render = subparsers.add_parser(
        "render", help="render a chapter with a selected backend"
    )
    render.add_argument("--backend", choices=BACKEND_NAMES, default=INDEXTTS_25)
    render.add_argument("--script", required=True)
    render.add_argument("--output", required=True)
    render.add_argument("--project-root")
    render.add_argument("--prompt", required=True)
    render.add_argument("--config")
    render.add_argument("--model-dir")
    render.add_argument("--device")
    render.add_argument("--dry-run", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "prepare":
        prepare_file(args.input, args.output, remove_headings=not args.keep_headings)
        return 0

    config = load_config(args.config)
    if args.command == "plan":
        if args.max_chars is not None:
            config = with_overrides(config, max_chunk_chars=args.max_chars)
        print(
            json.dumps(plan_chapter(args.script, config), ensure_ascii=False, indent=2)
        )
        return 0

    if args.command == "validate":
        output_format = output_format_for(args.backend, config)
        result = validate_wav(
            args.wav,
            expected_sample_rate=output_format.sample_rate,
            expected_channels=output_format.channels,
            expected_subtype=output_format.subtype,
            max_seconds_per_char=config.max_seconds_per_char
            if args.text_chars
            else None,
            text_characters=args.text_chars,
        )
        print(json.dumps(result.__dict__, ensure_ascii=False, indent=2))
        return 0 if result.ok else 1

    if args.command == "render":
        if args.device:
            config = with_overrides(config, device=args.device)
        render_chapter(
            args.script,
            args.output,
            backend=args.backend,
            project_root=args.project_root,
            prompt_wav=args.prompt,
            config=config,
            model_dir=args.model_dir,
            dry_run=args.dry_run,
        )
        if args.dry_run:
            print(
                json.dumps(
                    {
                        "backend": args.backend,
                        "output": str(Path(args.output).expanduser().resolve()),
                        "chunks": plan_chapter(args.script, config),
                        "output_format": output_format_for(
                            args.backend, config
                        ).as_dict(),
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
        return 0

    return 2
