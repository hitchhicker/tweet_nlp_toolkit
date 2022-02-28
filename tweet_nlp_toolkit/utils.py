"""
Utils functions.
"""
import unicodedata

from tweet_nlp_toolkit.constants import ENGLISH_STOP_WORDS, UNKNOWN_LANGUAGE, VARIATION_SELECTORS, PYCLD2_LANGUAGE_CODES

import pycld2


# Note: The following code is copied from https://github.com/google-research/bert/blob/master/tokenization.py#L220
def strip_accents_unicode(text):
    text = unicodedata.normalize("NFD", text)
    output = []
    for char in text:
        cat = unicodedata.category(char)
        if cat == "Mn":
            continue
        output.append(char)
    return "".join(output)


def get_stop_words(lang):
    if lang == "en":
        return ENGLISH_STOP_WORDS

    raise ValueError(f"unknown stop list: {lang}")


def get_language(text, languages_set=PYCLD2_LANGUAGE_CODES):
    lang = pycld2.detect("".join([i for i in text if i.isprintable()]), bestEffort=True)[2][0][1]
    return UNKNOWN_LANGUAGE if lang not in languages_set else lang


# The following function is copied from https://github.com/bfelbo/DeepMoji/blob/master/deepmoji/filter_utils.py#L128
def remove_variation_selectors(text):
    """Remove styling glyph variants for Unicode characters.
    For instance, remove skin color from emojis.
    """
    for var in VARIATION_SELECTORS:
        text = text.replace(var, "")
    return text
