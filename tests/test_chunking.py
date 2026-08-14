from audiobook_pipeline.chunking import split_text


def test_chunking_preserves_paragraph_order_and_avoids_empty_chunks():
    text = "第一段。\n\n第二段。\n\n第三段。"
    chunks = split_text(text, max_chars=20)
    assert [chunk.index for chunk in chunks] == [1, 2, 3]
    assert [chunk.text for chunk in chunks] == ["第一段。", "第二段。", "第三段。"]


def test_long_sentence_is_hard_split_at_limit():
    chunks = split_text("甲" * 25, max_chars=10)
    assert [chunk.text for chunk in chunks] == ["甲" * 10, "甲" * 10, "甲" * 5]
