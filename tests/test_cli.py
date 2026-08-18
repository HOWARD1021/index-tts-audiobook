import pytest

from audiobook_pipeline.cli import build_parser


def test_render_accepts_mlx_backend_without_project_root():
    args = build_parser().parse_args(
        [
            "render",
            "--backend",
            "mlx-1.5",
            "--script",
            "chapter.md",
            "--output",
            "chapter.wav",
            "--model-dir",
            "/external/model",
            "--prompt",
            "/external/prompt.wav",
        ]
    )
    assert args.backend == "mlx-1.5"
    assert args.project_root is None


def test_render_rejects_unknown_backend():
    with pytest.raises(SystemExit):
        build_parser().parse_args(
            [
                "render",
                "--backend",
                "unknown",
                "--script",
                "chapter.md",
                "--output",
                "chapter.wav",
                "--prompt",
                "prompt.wav",
            ]
        )
