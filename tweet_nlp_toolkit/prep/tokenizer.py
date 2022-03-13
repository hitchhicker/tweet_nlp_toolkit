"""
Tokenizers.
"""
import logging
from typing import List, Callable

from mosestokenizer import MosesDetokenizer

from tweet_nlp_toolkit.constants import CJK, JP_CHARACTERS, THAI_CHARACTERS
from tweet_nlp_toolkit.prep.regexes import (
    TWEET_TOKENIZE,
    WEIBO_TOKENIZE,
)
from tweet_nlp_toolkit.prep.token import WeiboToken, Token
from tweet_nlp_toolkit.prep.word_segmentation import segment

log = logging.getLogger(__name__)


class Detokenizer:
    """
    Using MosesDetokenizer: https://pypi.org/project/mosestokenizer/
    https://github.com/moses-smt/mosesdecoder/blob/master/scripts/tokenizer/detokenizer.perl
    First, create an instance of the tokenizer for the required language, then call it for each
    list of tokens
    Languages with built-in rules: cs|en|fr|it|fi
    """

    def __init__(self, lang="en"):
        self._lang = lang
        self._detokenizer = MosesDetokenizer(lang)
        log.info(f"Detokenizer for lang {lang} initialized")

    def detokenize(self, tokens):
        return self._detokenizer(tokens)


def tweet_tokenize(text: str) -> List[Token]:
    return [Token(tok) for tok in TWEET_TOKENIZE.findall(text)]


def _weibo_tokenize(text: str) -> List[WeiboToken]:
    return [WeiboToken(tok) for tok in WEIBO_TOKENIZE.findall(text)]


def white_space_tokenize(text: str) -> List[Token]:
    """White space tokenize with simple cleaning."""
    text = text.strip()
    if not text:
        return []
    tokens = text.split()
    return [Token(tok) for tok in tokens]


# reference: https://stackoverflow.com/questions/9166130/what-are-the-upper-and-lower-bound-for-chinese-char-in-utf-8
def _is_chinese(cp: int) -> bool:
    """
    Is Chinese character
    :param cp: unicode code point
    """
    return cp in CJK


# reference: http://www.rikai.com/library/kanjitables/kanji_codes.unicode.shtml
def _is_japanese(cp: int) -> bool:
    """
    Is Japanese character
    :param cp: unicode code point
    """
    return cp in JP_CHARACTERS or _is_chinese(cp)


# reference: https://en.wikipedia.org/wiki/Thai_(Unicode_block)
def _is_thai(cp: int):
    """
    Is Thai character
    :param cp: unicode code point
    """
    return cp in THAI_CHARACTERS


def _asian_language_tokenize(text: str, language: str, char_check_func: Callable) -> List[Token]:
    """
    :param char_check_func: a function verifying whether a given character unicode code point matches the language
    """
    output = []
    chars = []
    for ch in text:
        val_unicode = ord(ch)
        if char_check_func(val_unicode):
            chars.append(ch)
        else:
            if chars:
                output.append(segment(language=language, text="".join(chars)))
                chars = []
            output.append(ch)
    if chars:
        output.append(segment(language=language, text="".join(chars)))
    return tweet_tokenize("".join(output))


def chinese_tokenize(text: str) -> List[Token]:
    return _asian_language_tokenize(text=text, language="zh", char_check_func=_is_chinese)


def japanese_tokenize(text: str) -> List[Token]:
    return _asian_language_tokenize(text=text, language="ja", char_check_func=_is_japanese)


def thai_tokenize(text: str) -> List[Token]:
    return _asian_language_tokenize(text=text, language="th", char_check_func=_is_thai)


def weibo_tokenize(text: str, segment_hashtag=False) -> List[WeiboToken]:
    """Weibo tokenizer utils function."""
    output = []
    tokens = _weibo_tokenize(text)

    for token in tokens:
        if token.is_mention:
            output.append(token)
        elif token.is_hashtag:
            if segment_hashtag:
                output.append(WeiboToken("#"))
                output.extend(list(map(lambda x: WeiboToken(str(x)), chinese_tokenize(token.value[1:-1]))))
                output.append(WeiboToken("#"))
            else:
                output.append(token)
        else:
            output.extend(list(map(lambda x: WeiboToken(str(x)), chinese_tokenize(token.value))))
    return output
