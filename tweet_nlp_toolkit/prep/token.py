"""
Token.
"""
import re
import unicodedata

import emoji
from emoji import EMOJI_ALIAS_UNICODE_ENGLISH, UNICODE_EMOJI_ENGLISH

from tweet_nlp_toolkit.constants import (
    MENTION_TAG,
    HASHTAG_TAG,
    URL_TAG,
    DIGIT_TAG,
    EMOJI_TAG,
    EMOTICON_TAG,
    PUNCTUATION_TAG,
    EMAIL_TAG,
    UNKNOWN_LANGUAGE,
)
from tweet_nlp_toolkit.prep.regexes import (
    WEIBO_HASHTAG,
    NOT_A_HASHTAG_PATTERN,
    HASHTAG_PATTERN,
    URL_PATTERN,
    MENTION_PATTERN,
    EMOTICONS_PATTERN,
    DIGIT_PATTERN,
    EMAIL_PATTERN,
    HTML_TAG_PATTERN,
)
from tweet_nlp_toolkit.utils import get_stop_words


class Token:
    """
    A string like Token class
    """

    __name__ = "Token"

    def __init__(self, value, lang=None):
        super().__init__()
        self._value = value
        self._lang = lang

    def __repr__(self):
        return f"'{self.__str__()}'"

    def __str__(self):
        return self._value

    def __len__(self):
        return len(self._value)

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self._value) == other

        return str(self._value) == str(other.value)

    def __hash__(self):
        return hash(self._value)

    def __getitem__(self, item):
        return self._value[item]

    def __setitem__(self, key, value):
        self._value[key] = value

    def _check_flag(self, pattern):
        return re.match(pattern, self._value) is not None

    def do_action(self, action):
        return action.apply(self)

    def get_attr(self, attr_name):
        return self.__getattribute__(attr_name)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, new_lang):
        self._lang = new_lang

    @property
    def is_hashtag(self):
        return not self._check_flag(pattern=NOT_A_HASHTAG_PATTERN) and self._check_flag(pattern=HASHTAG_PATTERN)

    @property
    def is_url(self):
        return self._check_flag(pattern=URL_PATTERN)

    @property
    def is_mention(self):
        return self._check_flag(pattern=MENTION_PATTERN)

    @property
    def is_emoticon(self):
        return self._check_flag(pattern=EMOTICONS_PATTERN)

    @property
    def is_emoji(self):
        # emoji in unicode representation or textual representation
        return self.value in UNICODE_EMOJI_ENGLISH or self.value in EMOJI_ALIAS_UNICODE_ENGLISH

    @property
    def is_digit(self):
        return self._check_flag(pattern=DIGIT_PATTERN)

    @property
    def is_punct(self):
        return len(self.value) == 1 and self._is_punctuation(self._value)

    @property
    def is_email(self):
        return self._check_flag(pattern=EMAIL_PATTERN)

    @property
    def is_stop_word(self):
        if self._lang is None or self.lang == UNKNOWN_LANGUAGE:
            return False
        return self.value.lower() in get_stop_words(self._lang)

    @property
    def is_html_tag(self):
        return self._check_flag(pattern=HTML_TAG_PATTERN)

    @staticmethod
    # The following function is copied from https://github.com/google-research/bert/blob/master/tokenization.py#L386
    def _is_punctuation(char):
        """Checks whether `chars` is a punctuation character."""
        cp = ord(char)
        # We treat all non-letter/number ASCII as punctuation.
        # Characters such as "^", "$", and "`" are not in the Unicode
        # Punctuation class but we treat them as punctuation anyways, for
        # consistency.
        if (33 <= cp <= 47) or (58 <= cp <= 64) or (91 <= cp <= 96) or (123 <= cp <= 126):
            return True
        cat = unicodedata.category(char)
        if cat.startswith("P"):
            return True
        return False


class Action:
    """
    Action to apply on the token.
    """

    REPLACE_MAPPINGS = {
        "is_mention": MENTION_TAG,
        "is_hashtag": HASHTAG_TAG,
        "is_url": URL_TAG,
        "is_digit": DIGIT_TAG,
        "is_emoji": EMOJI_TAG,
        "is_emoticon": EMOTICON_TAG,
        "is_punct": PUNCTUATION_TAG,
        "is_email": EMAIL_TAG,
    }
    ACTION_MAPPING = {
        "is_mention": ["remove", "tag"],
        "is_hashtag": ["remove", "tag"],
        "is_url": ["remove", "tag"],
        "is_digit": ["remove", "tag"],
        "is_emoji": ["remove", "tag", "demojize", "emojize"],
        "is_emoticon": ["remove", "tag"],
        "is_punct": ["remove", "tag"],
        "is_email": ["remove", "tag"],
        "is_html_tag": ["remove"],
        "is_stop_word": ["remove"],
    }

    def __init__(self, action_name, action_condition):
        self._action_name = action_name
        self._action_condition = action_condition

    @staticmethod
    def _remove(token: Token):
        token.value = ""

    def _tag(self, token: Token):
        token.value = self.REPLACE_MAPPINGS[self._action_condition]

    @staticmethod
    def _demojize(token: Token):
        token.value = emoji.demojize(token.value)

    @staticmethod
    def _emojize(token: Token):
        token.value = emoji.emojize(token.value, use_aliases=True)

    def _is_valid_action(self, token_obj):
        """Check if action is valid."""
        if (
            self._action_name is None
            or len(self._action_name) == 0
            or self._action_condition is None
            or len(self._action_condition) == 0
        ):
            return False
        if not hasattr(token_obj, self._action_condition):
            raise ValueError(f"{token_obj.__class__.__name__} doesn't has attribute {self._action_condition}")
        if self._action_name not in self.ACTION_MAPPING[self._action_condition]:
            raise ValueError(
                f"unknown action '{self._action_name}', expected {self.ACTION_MAPPING[self._action_condition]}"
            )
        return True

    def apply(self, token: Token):
        """
        Apply action on token.

        :return: bool, Is the action applied on token
        """
        if self._is_valid_action(token) and token.get_attr(self._action_condition):
            {"remove": self._remove, "tag": self._tag, "demojize": self._demojize, "emojize": self._emojize,}[
                self._action_name
            ](token)
            return True
        return False


class WeiboToken(Token):
    @property
    def is_hashtag(self):
        return self._check_flag(WEIBO_HASHTAG)
