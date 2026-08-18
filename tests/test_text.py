from audiobook_pipeline.text import (
    convert_traditional_to_simplified,
    prepare_narration_text,
)


def test_traditional_text_is_converted_without_reordering_paragraphs():
    source = "# 第一章\n\n交易市場中沒有新鮮事。\n\nVolume Price Analysis"
    prepared = prepare_narration_text(source)
    assert prepared == "第一章\n\n交易市场中没有新鲜事。\n\nVolume Price Analysis\n"


def test_glossary_entry_is_protected_from_conversion():
    source = "量價分析與自訂術語"
    result = convert_traditional_to_simplified(
        source, {"量價分析": "量价分析", "自訂術語": "VPA"}
    )
    assert result == "量价分析与VPA"
