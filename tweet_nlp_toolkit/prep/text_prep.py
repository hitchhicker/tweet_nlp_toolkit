import codecs
import logging
import re

import contractions


from tweet_nlp_toolkit.prep.regexes import URL_PAT, QUOTES_PAT, RT_MENTION_PAT, APOSTROPHES_PAT
from tweet_nlp_toolkit.prep.text_parser import parse_text

"""
Text preprocessing utils
The goal is to allow using individual functions as required

# TODO handle html entities &amp;
# TODO improve pattern
"""

logger = logging.getLogger(__name__)


def replace_contractions(text, lang='en'):
    """
    e.g.
    ima    -> I am going to
    yall  -> you all

    See https://github.com/kootenpv/contractions
    :param text: the text to process
    :param lang: the language to handle. Only English is supported.
    :return:
    """
    if lang != 'en':
        logger.warning("Contractions fix is currently only supporting English. Not changing the text")
        return text

    return contractions.fix(text)


def prep(text, **kwargs):
    """
    Preprocess the text
    :param text: the text to preprocess
    :return: the processed text
    """
    return parse_text(text=text, **kwargs).value


def prep_file(filename, outfile, **kwargs):
    """
    Preprocess a file, assuming it's supposed to be utf-8
    :param filename:
    :param outfile:
    :param kwargs: arguments for the prep function
    :return:
    """
    with codecs.open(filename, encoding='unicode_escape') as f:
        outf = open(outfile, 'w')
        for line in f.readlines():
            outf.write(prep(line, encoding='utf-8', **kwargs) + '\n')
        outf.close()


def normalize_apos(text, ):
    """ Normalize single quotes / apostrophes to a unique type """
    return re.sub(APOSTROPHES_PAT, "'", text)


def normalize_quotes(text):
    """ Normalize double quotes to a unique type """
    return re.sub(QUOTES_PAT, '"', text)


def remove_redundant_spaces(text):
    return re.sub(r'[ \t]{2,}', ' ', text).strip()


def remove_rt_mention(text):
    """Remove RT followed by a mention (e.g. RT @BentheFidler:).
    This format is used to mark retweets with no comments """
    return re.sub(RT_MENTION_PAT, '', text)


def remove_url(text):
    return re.sub(URL_PAT, '', text)


