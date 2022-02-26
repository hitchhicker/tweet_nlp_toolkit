import pytest

from tweet_nlp_toolkit.constants import UNKNOWN_LANGUAGE
from tweet_nlp_toolkit.utils import get_stop_words, get_language, remove_variation_selectors, strip_accents_unicode


def test_get_stop_words():
    assert type(get_stop_words('en')) == frozenset


def test_get_stop_words_unknown_language():
    with pytest.raises(ValueError):
        assert get_stop_words('test')

#
# def test_get_language():
#     assert get_language('this is en') == 'en'
#     assert get_language('this is en', languages_set='fr') == UNKNOWN_LANGUAGE
#     assert get_language('c\'est francais') == 'fr'
#     assert get_language('') == UNKNOWN_LANGUAGE


def test_remove_variation_selectors():
    assert remove_variation_selectors(u'\ufe00') == ""


@pytest.mark.parametrize(('text', 'expected'),
                         [('', ''),  # empty input
                         ('english', 'english'),  # no accent input
                         ('ếtre', 'etre'),  # French
                          ('ความรักมากสำหรับผู้หญิงคนนี้', 'ความรกมากสำหรบผหญงคนน')])  # Thai
def test_strip_accents_unicode(text, expected):
    assert strip_accents_unicode(text) == expected
