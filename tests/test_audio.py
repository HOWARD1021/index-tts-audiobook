import numpy as np
import soundfile as sf

from audiobook_pipeline.audio import validate_wav


def test_valid_pcm16_mono_wav_passes(tmp_path):
    path = tmp_path / "valid.wav"
    sf.write(path, np.zeros(22050, dtype=np.float32), 22050, subtype="PCM_16")
    result = validate_wav(path, text_characters=20, max_seconds_per_char=0.8)
    assert result.ok
    assert result.duration_seconds == 1.0


def test_runaway_short_chunk_fails_duration_sanity(tmp_path):
    path = tmp_path / "runaway.wav"
    sf.write(path, np.zeros(22050 * 20, dtype=np.float32), 22050, subtype="PCM_16")
    result = validate_wav(path, text_characters=5, max_seconds_per_char=0.8)
    assert not result.ok
    assert any("sanity limit" in error for error in result.errors)


def test_wrong_format_fails(tmp_path):
    path = tmp_path / "stereo.wav"
    sf.write(path, np.zeros((22050, 2), dtype=np.float32), 16000, subtype="PCM_16")
    result = validate_wav(path)
    assert not result.ok
    assert "sample rate 16000 != 22050" in result.errors
    assert "channels 2 != 1" in result.errors
