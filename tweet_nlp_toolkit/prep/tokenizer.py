"""
Tokenizers.
"""
import html
import logging
import re
from itertools import chain
from typing import List, Callable

from mosestokenizer import MosesDetokenizer

from tweet_nlp_toolkit.prep.regexes import (
    EMAIL,
    MENTION,
    HASHTAG,
    EMOTICONS,
    WORD,
    HTML_TAG,
    ASCII_ARROW,
    DIGIT,
    ELLIPSIS_DOTS,
    URL,
    EMOJI_STRING,
    WEIBO_HASHTAG,
)
from tweet_nlp_toolkit.prep.token import WeiboToken, Token
from tweet_nlp_toolkit.prep.word_segmentation import segment

log = logging.getLogger(__name__)

CJK = frozenset(
    chain(
        range(0x4E00, 0xA000),
        range(0x3400, 0x4DC0),
        range(0x20000, 0x2A6E0),
        range(0x2A700, 0x2B740),
        range(0x2B740, 0x2B820),
        range(0xF900, 0xFB00),
        range(0x2F800, 0x2FA20),
        range(0x9FA6, 0x9FCC),
    )
)

JP_CHARACTERS = frozenset(
    chain(
        range(0x3000, 0x3040),  # Japanese-style punctuation
        range(0x3040, 0x30A0),  # Hiragana
        range(0x30A0, 0x3100),  # Katakana
        range(0xFF00, 0xFFF0),
    )
)  # Full-width roman characters and half-width katakana

THAI_CHARACTERS = frozenset(range(0x0E00, 0x0E80))


class TwitterTokenizer:
    """
    Tokenizer for Twitter.
    """

    def __init__(self, tokenizer="social_media"):
        self._tokenizer = tokenizer
        if tokenizer == "naive":
            self._tknzr = WhiteSpaceTokenizer()
        elif tokenizer == "social_media":
            self._tknzr = SocialMediaTokenizer()
        else:
            raise NotImplementedError(f"Unsupported tokenizer: {tokenizer}")

    def tokenize(self, tweet):
        return self._tknzr.tokenize(tweet)


class SocialMediaTokenizer:
    """
    Tokenizer for social media.
    """

    def __init__(self):
        self.token_pipeline = [
            URL,
            EMAIL,
            MENTION,
            HASHTAG,
            EMOTICONS,
            HTML_TAG,
            ASCII_ARROW,
            DIGIT,
            ELLIPSIS_DOTS,
            EMOJI_STRING,
            WORD,
            r"\S",
        ]
        self.tokenizer = re.compile(rf'{"|".join(self.token_pipeline)}', re.UNICODE)

    def tokenize(self, text: str) -> List[str]:
        text = text.encode("utf-16", "surrogatepass").decode("utf-16", "replace")
        escaped = html.unescape(text)  # &pound;100 -> £100
        return self.tokenizer.findall(escaped)


class WeiboTokenizer(SocialMediaTokenizer):
    def __init__(self):
        super().__init__()
        hashtag_regex_index = self.token_pipeline.index(HASHTAG)
        self.token_pipeline[hashtag_regex_index] = WEIBO_HASHTAG
        self.tokenizer = re.compile(rf'{"|".join(self.token_pipeline)}', re.UNICODE)


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


class WhiteSpaceTokenizer:
    @staticmethod
    def tokenize(text):
        return white_space_tokenize(text)


def social_media_tokenize(text: str) -> List[Token]:
    return [Token(tok) for tok in SocialMediaTokenizer().tokenize(text)]


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
    return social_media_tokenize("".join(output))


def chinese_tokenize(text: str) -> List[Token]:
    return _asian_language_tokenize(text=text, language="zh", char_check_func=_is_chinese)


def japanese_tokenize(text: str) -> List[Token]:
    return _asian_language_tokenize(text=text, language="ja", char_check_func=_is_japanese)


def thai_tokenize(text: str) -> List[Token]:
    return _asian_language_tokenize(text=text, language="th", char_check_func=_is_thai)


def weibo_tokenize(text: str, segment_hashtag=False) -> List[WeiboToken]:
    """Weibo tokenizer utils function."""
    output = []
    tokens = map(WeiboToken, WeiboTokenizer().tokenize(text))

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
