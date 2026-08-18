import os
import sys
from pathlib import Path

import pytest

from audiobook_pipeline.config import PipelineConfig
from audiobook_pipeline.runner import render_chapter


@pytest.mark.skipif(
    os.environ.get("RUN_MLX_SMOKE") != "1",
    reason="set RUN_MLX_SMOKE=1 with external MLX paths to enable",
)
def test_real_mlx_model_generates_short_simplified_chinese(tmp_path):
    runtime_root = Path(os.environ["MLX_INDEXTTS_RUNTIME_ROOT"])
    sys.path.insert(0, str(runtime_root))
    model_dir = Path(os.environ["MLX_INDEXTTS_MODEL_DIR"])
    prompt = Path(os.environ["MLX_INDEXTTS_PROMPT"])
    script = tmp_path / "short-chinese.txt"
    script.write_text("这是一次简短的中文语音测试。", encoding="utf-8")

    output = render_chapter(
        script,
        tmp_path / "short-chinese.wav",
        backend="mlx-1.5",
        prompt_wav=prompt,
        model_dir=model_dir,
        config=PipelineConfig(max_chunk_chars=40, max_mel_tokens=300),
    )
    assert output.is_file()
