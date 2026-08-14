from audiobook_pipeline.config import load_config


def test_default_config_loads(tmp_path):
    path = tmp_path / "config.toml"
    path.write_text(
        """
[defaults]
language = "ZH"
max_chunk_chars = 120

[defaults.emotion]
vector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8]
alpha = 0.6
""",
        encoding="utf-8",
    )
    config = load_config(path)
    assert config.language == "ZH"
    assert config.max_chunk_chars == 120
    assert config.emotion.vector[-1] == 0.8
    assert config.emotion.alpha == 0.6
