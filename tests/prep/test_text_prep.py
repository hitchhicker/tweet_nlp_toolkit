import os
import tempfile

import pytest

from tweet_nlp_toolkit.constants import UNENCODABLE_CHAR, MENTION_TAG, HASHTAG_TAG
from tweet_nlp_toolkit.prep.text_prep import prep, replace_contractions, prep_file, normalize_apos, normalize_quotes


@pytest.mark.parametrize(("text", "expected"),
                         [("C?est parce qu?elle a bénéficié", "c'est parce qu'elle a beneficie")
                          ])
def test_prep(text, expected):
    assert prep(text) == expected


@pytest.mark.parametrize(("text", "expected"),
                         [("I got 12 apples", "i got apples")
                          ])
def test_prep_remove_digits(text, expected):
    assert prep(text, digits='remove') == expected


@pytest.mark.parametrize(("text", "expected"),
                         [("Types of #Bias in Machine Learning https://buff.ly/2Uclr2A",
                           "Types of #Bias in Machine Learning")
                          ])
def test_prep_remove_url(text, expected):
    assert prep(text, to_lower=False, urls='remove') == expected


@pytest.mark.parametrize(("text", "expected"),
                         [("I'm gonna do it", "I am going to do it")
                          ])
def test_fix_contractions(text, expected):
    assert replace_contractions(text) == expected


@pytest.mark.parametrize(("text", "expected"),
                         [("I'm gonna do it", "I am going to do it")
                          ])
def test_replace_contractions_not_en(text, expected):
    assert replace_contractions(text, lang='fr') == text


# Emoji tests

@pytest.mark.parametrize(("text", "expected"),
                         [("cool 😰", "cool")
                          ])
def test_emoji_remove(text, expected):
    assert prep(text, emojis='remove') == expected


@pytest.mark.parametrize(("text", "expected"),
                         [("cool 😰", "cool <EMOJI>")
                          ])
def test_emoji_tag(text, expected):
    assert prep(text, emojis='tag') == expected


@pytest.mark.parametrize(("text", "expected"),
                         [("cool 😰", "cool :anxious_face_with_sweat:")
                          ])
def test_emoji_demojize(text, expected):
    assert prep(text, emojis='demojize') == expected


@pytest.mark.parametrize(("text", "expected"),
                         [
                             ("cool 😂", "cool 😂"),
                             ("cool :joy::joy:", "cool 😂 😂")
                         ])
def test_emoji_emojize(text, expected):
    assert prep(text, emojis='emojize') == expected


@pytest.mark.parametrize(("text", "expected"),
                         [("cool 😰", "cool 😰")
                          ])
def test_emoji_none(text, expected):
    assert prep(text) == expected


# Test encoding treatment

@pytest.mark.parametrize(("text", "expected"),
                         [("doesn\u2019t", "doesn ’ t")  # modified by Bokai
                          ])
def test_encoding(text, expected):
    assert prep(text, remove_unencodable_char=False) == expected


@pytest.mark.parametrize(("text", "expected"),
                         [("doesn\ud83c\udf08t", "doesn " + UNENCODABLE_CHAR + " t")  # modified by Bokai
                          ])
def test_encoding_unencodable(text, expected):
    assert prep(text, remove_unencodable_char=False) == expected


@pytest.mark.parametrize(("text", "expected"),
                         [("doesn\ud83c\udf08t", "doesn t")
                          ])
def test_encoding_unencodable_remove(text, expected):
    assert prep(text, remove_unencodable_char=True) == expected


@pytest.mark.parametrize(("text", "expected"),
                         [("@emnlp2019 should", "should"),  # beginning
                          ("I think @emnlp2019 should", "i think should"),  # middle
                          ("I think @emnlp2019", "i think"),  # end
                          ("I think a@b.com", "i think a@b.com"),  # don't remove email

                          ])
def test_mentions_remove(text, expected):
    assert prep(text, mentions='remove') == expected


@pytest.mark.parametrize(("text", "expected"),
                         [("@emnlp2019 should", MENTION_TAG + " should"),  # beginning
                          ])
def test_mentions_tag(text, expected):
    assert prep(text, mentions='tag') == expected


@pytest.mark.parametrize(("text", "expected"),
                         [("#emnlp2019 should", "should"),  # beginning
                          ("I think #emnlp2019 should", "i think should"),  # middle
                          ("I think #emnlp2019", "i think"),  # end
                          ("#prédéfinie", ""),  # non ascii
                          ("#Филмскисусрети", ""),
                          # ("החיים עצמם #כן_אבל", ""), # RTL TODO
                          ("#HappyJungkookDay #정국생일ᄎᄏ", ""),
                          ("I think #123", "i think #123")  # a hashtag can't be just a seq of numbers
                          ])
def test_hashtags_remove(text, expected):
    assert prep(text, hashtags='remove') == expected


@pytest.mark.parametrize(("text", "expected"),
                         [("#emnlp2019 should", HASHTAG_TAG + " should"),  # beginning
                          ])
def test_hashtags_tag(text, expected):
    assert prep(text, hashtags='tag') == expected


@pytest.mark.parametrize(("text", "expected"),
                         [("Shit I\\u2019m gonna clip this bit on whiteness",
                           "shit i ’ m gonna clip this bit on whiteness")  # modified by Bokai
                          ])
def test_prep_file(text, expected):
    """
    Writes text to file, then processes the file (which writes to an output file),
    loads the output file and compares to the expected result
    :param text:
    :param expected:
    :return:
    """
    infile, infile_filename = tempfile.mkstemp()
    outfile, outfile_filename = tempfile.mkstemp()
    with open(infile_filename, 'w', encoding='ascii') as f:
        f.write(text)

    prep_file(infile_filename, outfile_filename)

    with open(outfile_filename, 'r') as f:
        line = f.readline().strip()

    assert line == expected

    # cleanup
    os.close(infile)
    os.close(outfile)


@pytest.mark.parametrize(("text", "expected"),
                         [("Maybe my new profession 😊 #golf #sport ", "maybe my new profession 😊 #golf"),
                          ("Maybe my new profession 😊 #golf #sports ", "maybe my new profession 😊 #golf #sports")
                          # not match
                          ])
def test_prep_with_filters_when_to_lower_is_true(text, expected):
    assert prep(text, to_lower=True, filters={'#sport'}) == expected


@pytest.mark.parametrize(("text", "expected"),
                         [("Maybe my new profession 😊 #golf #Sport ", "Maybe my new profession 😊 #golf #Sport")])
def test_prep_with_filters_when_to_lower_is_false(text, expected):
    assert prep(text, to_lower=False, filters={'#sport'}) == expected


@pytest.mark.parametrize(("text", "expected"),
                         [("@remy: This is waaaaayyyy too much for you!!!!!!",
                           "@remy : this is waaayyy too much for you ! ! !")])
def test_prep_when_reduce_len_is_true(text, expected):
    assert prep(text, reduce_len=True) == expected


@pytest.mark.parametrize(("text", "expected"),
                         [("ความรักมากสำหรับผู้หญิงคนนี้", "ความรักมากสำหรับผู้หญิงคนนี้")])
def test_prep_with_thai(text, expected):
    assert prep(text, strip_accents=False) == expected


@pytest.mark.parametrize(("text", "expected"),
                         [("I think therefore i‘m i’m", "I think therefore i'm i'm")])
def test_normalize_apos(text, expected):
    assert normalize_apos(text) == expected


@pytest.mark.parametrize(("text", "expected"),
                         [('“Because it\'s there” -- George Mallory', '"Because it\'s there" -- George Mallory'),
                          ('«Because it\'s there» -- George Mallory', '"Because it\'s there" -- George Mallory')]
                         )
def test_normalize_quotes(text, expected):
    assert normalize_quotes(text) == expected
