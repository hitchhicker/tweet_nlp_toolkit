from unittest.mock import patch

import pytest

from tweet_nlp_toolkit.prep.word_segmentation import _get_segmentation_tool, segment, AbstractSegmentationTool, \
    ChineseSegmentationTool, JapaneseSegmentationTool


@pytest.fixture
def mocked_read_stats():
    def _mocked_read_stats(language, ngram):
        if ngram == 1:
            return {"unit": 5, "test": 10}
        if ngram == 2:
            return {"unit_test": 2, "hello_world": 4}

    return _mocked_read_stats


def test_get_segmentation_tool_when_language_is_chinese():
    assert isinstance(_get_segmentation_tool(language='zh'), ChineseSegmentationTool)


def test_get_segmentation_tool_when_language_is_japanese():
    assert isinstance(_get_segmentation_tool(language='ja'), JapaneseSegmentationTool)


def test_get_segmentation_tool_when_language_is_not_supported():
    with pytest.raises(KeyError):
        _get_segmentation_tool(language='ab')


@pytest.mark.parametrize(('text', 'expected_segmented_words'),
                         [('这是一个测试', '这是 一个 测试'),
                          ('', '')])
def test_segment_chinese(text, expected_segmented_words):
    assert segment(language='zh', text=text) == expected_segmented_words


@pytest.mark.parametrize(('text', 'expected_segmented_words'),
                         [('pythonが大好きです', 'python が 大好き です'),
                          ('', '')])
def test_segment_japanese(text, expected_segmented_words):
    assert segment(language='ja', text=text) == expected_segmented_words


@pytest.mark.parametrize(('text', 'expected_segmented_words'),
                         [('ผมรักคุณนะครับโอเคบ่พวกเราเป็นคนไทยรักภาษาไทยภาษาบ้านเกิด',
                           'ผม รัก คุณ นะ ครับ โอเค บ่ พวกเรา เป็น คนไทย รัก ภาษาไทย ภาษา บ้านเกิด'),
                          ('', '')])
def test_segment_thai(text, expected_segmented_words):
    assert segment(language='th', text=text) == expected_segmented_words


@pytest.mark.parametrize(('text', 'expected_segmented_words'),
                         [('abc edf', 'abc edf'),
                          ('', '')])
def test_segment_unsupported_language(text, expected_segmented_words):
    assert segment(language='ab', text=text) == expected_segmented_words


def test_AbstractSegmentationTool_with_NotImplementedError_raised():
    abst_segmentation_tool = AbstractSegmentationTool()
    with pytest.raises(NotImplementedError):
        abst_segmentation_tool.segment('test')


def test_AbstractSegmentationTool_singleton():
    seg1 = AbstractSegmentationTool()
    seg2 = AbstractSegmentationTool()
    assert seg1 is seg2
