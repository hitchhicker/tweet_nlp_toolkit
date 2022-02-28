""""
Word Segmentation utils for those languages where words are not delimited by space, such as chinese and japanese.

Usage Example:

    from tweet_nlp_toolkit.prep.word_segmentation import segment

    segment(language='zh', text='这是一个测试') --> '这是 一个 测试'
"""
import logging
from abc import abstractmethod
from typing import Dict, Type

import MeCab
import jieba
from pythainlp import word_tokenize
from pythainlp.util import normalize

from tweet_nlp_toolkit.constants import (
    JAPANESE_LANGUAGE_CODE,
    CHINESE_LANGUAGE_CODE,
    SUPPORTED_LANGUAGES,
    THAI_LANGUAGE_CODE,
)

logger = logging.getLogger(__name__)


def segment(language: str, text: str) -> str:
    """Segment asian languages."""
    if language is None:
        raise ValueError(f"language is not specified! expected one of {SUPPORTED_LANGUAGES}")
    if text is None:
        raise ValueError("text is not a valid string")
    try:
        segmentation_tool = _get_segmentation_tool(language=language)
    except KeyError:
        logger.warning(f"Language not supported for segmentation, supported languages: {SUPPORTED_LANGUAGES}")
        return text

    return segmentation_tool.segment(text)


def _get_segmentation_tool(language: str):
    """
    Segmentation tool factory.

    :return: SegmentationTool instance
    """
    segmentation_tools: Dict[str, Type[AbstractSegmentationTool]] = {
        JAPANESE_LANGUAGE_CODE: JapaneseSegmentationTool,
        CHINESE_LANGUAGE_CODE: ChineseSegmentationTool,
        THAI_LANGUAGE_CODE: ThaiSegmentationTool,
    }
    return segmentation_tools[language]()


class Singleton(type):
    _instances: Dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AbstractSegmentationTool(metaclass=Singleton):
    @abstractmethod
    def segment(self, text):
        raise NotImplementedError


class ChineseSegmentationTool(AbstractSegmentationTool):
    def segment(self, text: str) -> str:
        return " ".join(jieba.cut(text, cut_all=False))


class JapaneseSegmentationTool(AbstractSegmentationTool):
    def __init__(self):
        self.wakati = MeCab.Tagger("-Owakati")

    def segment(self, text: str) -> str:
        return " ".join(self.wakati.parse(text).split())


class ThaiSegmentationTool(AbstractSegmentationTool):
    def segment(self, text):
        # newmm: Maximum Matching algorithm for Thai word segmentation.
        # Developed by Korakot Chaovavanich (https://www.facebook.com/groups/408004796247683/permalink/431283740586455/)
        # Please refer to https://github.com/PyThaiNLP/pythainlp/wiki/PyThaiNLP-1.4#thai-segment for other engines
        if text is None or len(text) == 0:
            return ""

        return " ".join(word_tokenize(normalize(text), engine="newmm"))
