from audiobook_pipeline.text import (
    convert_traditional_to_simplified,
    prepare_narration_document,
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


def test_prepare_narration_removes_markdown_emphasis_and_speech_fillers():
    source = (
        "**巨大的成交量**會改變判斷。嗯，這句話不該有狀聲詞。"
        "……嗯，我們繼續。——嗯現在看圖。\n\n***\n\n（嘆氣）接著看圖。"
    )

    prepared = prepare_narration_text(source)

    assert prepared == (
        "巨大的成交量会改变判断。这句话不该有状声词。……我们继续。——现在看图。\n\n"
        "接著看图。\n"
    )


def test_prepare_narration_marks_light_tone_for_ban_sui_zhe():
    source = "伴隨著大實體 K 線。"

    prepared = prepare_narration_text(source)

    assert prepared == "伴随着大实体 K 线。\n"


def test_prepare_narration_removes_nonspoken_quote_and_parenthesis_marks():
    source = "『震盪』與（結果）以及「測試」。"

    prepared = prepare_narration_text(source)

    assert prepared == "震荡与结果以及测试。\n"


def test_prepare_narration_document_keeps_emphasis_as_metadata():
    source = "普通文字**巨大成交量**与*弱势信号*。"

    document = prepare_narration_document(source)

    assert document.text == "普通文字巨大成交量与弱势信号。\n"
    assert [(span.text, span.emphasis) for span in document.spans] == [
        ("普通文字", None),
        ("巨大成交量", "bold"),
        ("与", None),
        ("弱势信号", "italic"),
        ("。\n", None),
    ]
