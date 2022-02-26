import pytest

from tweet_nlp_toolkit.constants import HASHTAG_TAG, EMOJI_TAG, UNKNOWN_LANGUAGE
from tweet_nlp_toolkit.prep.token import Token, Action
from tweet_nlp_toolkit.prep.regexes import HASHTAG


@pytest.mark.parametrize(("value", "expected"),
                         [("#emnlp2019", True),
                          ("#prédéfinie", True),  # non ascii
                          ("#Филмскисусрети", True),
                          # ("#כן_אבל", True),  # RTL TODO
                          ("#정국생일ᄎᄏ", True),
                          ("#123", False)  # a hashtag can't be just a seq of numbers
                          ])
def test_token_is_hashtag(value, expected):
    assert Token(value).is_hashtag == expected


@pytest.mark.parametrize(("value", "expected"),
                         [("https://buff.ly/2Uclr2A", True),
                          ("www.google.fr", True)  # without leading http(s)
                          ])
def test_token_is_is_url(value, expected):
    assert Token(value).is_url == expected


@pytest.mark.parametrize(("value", "expected"),
                         [("@tutu", True),
                          ("@@", False),  # not valid mention
                          ("tutu@gmail.com", False)  # email
                          ])
def test_token_is_mention(value, expected):
    assert Token(value).is_mention == expected


@pytest.mark.parametrize(("value", "expected"),
                         [(":)", True),
                          ("(◕‿◕✿)", True)
                          ])
def test_token_is_emoticon(value, expected):
    assert Token(value).is_emoticon == expected


@pytest.mark.parametrize(("value", "expected"),
                         [("😰", True),
                          (":joy:", True),  # demojized emoji (':joy:' is in the emoji alias)
                          (":anxious_face_with_sweat:", True),  # demojized emoji
                          ("anxious_face_with_sweat", False)  # ':' matters
                          ])
def test_token_is_emoji(value, expected):
    assert Token(value).is_emoji == expected


@pytest.mark.parametrize(("value", "expected"),
                         [("1", True),  # single number
                          ("123", True),  # a sequence of numbers
                          ("12.34", True),  # decimal
                          ("12/34", True),  # fraction
                          ("12abc", False)  # combination of numbers and alphabets
                          ])
def test_token_is_digit(value, expected):
    assert Token(value).is_digit == expected


@pytest.mark.parametrize(("value", "expected"),
                         [(",", True),
                          ("\u2019", True),
                          ("12", False)])  # the length of token is not 1
def test_token_is_punct(value, expected):
    assert Token(value).is_punct == expected


@pytest.mark.parametrize(("value", "expected"),
                         [("tutu@gmail.com", True),
                          ("@tutu", False)  # mention
                          ])
def test_token_is_email(value, expected):
    assert Token(value).is_email == expected


def test_token_check_flag():
    hashtag_token = Token("#hashtag")
    assert hashtag_token._check_flag(HASHTAG) is True
    not_hashtag_token = Token("not_hashtag")
    assert not_hashtag_token._check_flag(HASHTAG) is False


def test_token_do_action_remove():
    token = Token("#hashtag")
    token.do_action(Action(action_name='remove', action_condition='is_hashtag'))
    assert token.value == ''


def test_token_do_action_tag():
    token = Token("#hashtag")
    token.do_action(Action(action_name='tag', action_condition='is_hashtag'))
    assert token.value == HASHTAG_TAG


def test_token_do_action_None():
    token = Token("#hashtag")
    token.do_action(Action(action_name=None, action_condition='is_hashtag'))
    assert token.value == "#hashtag"


def test_token_do_action_demojize():
    token = Token("😰")
    token.do_action(Action(action_name='demojize', action_condition='is_emoji'))
    assert token.value == ":anxious_face_with_sweat:"


def test_token_do_action_with_unknown_flag_str():
    token = Token("😰")
    with pytest.raises(ValueError):
        token.do_action(Action(action_name='demojize', action_condition='is_ijome', replace=EMOJI_TAG))


def test_token_do_action_with_unknown_action():
    token = Token("😰")
    with pytest.raises(ValueError):
        token.do_action(Action(action_name='ezijomed', action_condition='is_emoji', replace=EMOJI_TAG))

    token = Token("😰")
    with pytest.raises(ValueError):
        token.do_action(Action(action_name='demojize', action_condition='is_hashtag', replace=EMOJI_TAG))


def test_token___str__():
    token = Token('test')
    assert str(token) == 'test'


def test_token___repr__():
    token = Token('test')
    assert repr(token) == "'test'"


def test_token__is_stop_word():
    token = Token('the', lang='en')
    assert token.is_stop_word is True


def test_token__is_stop_word_when_token_is_in_upper_case():
    token = Token('The', lang='en')
    assert token.is_stop_word is True


def test_token_is_stop_word_when_language_is_not_given():
    token = Token('the')
    assert token.is_stop_word is False


def test_token_is_stop_word_when_language_is_detected_as_unknown():
    token = Token(value='the', lang=UNKNOWN_LANGUAGE)
    assert token.is_stop_word is False


def test_action_remove():
    action = Action(action_name='unittest', action_condition='unittest')  # arguments are not important here
    token = Token('test')
    action._remove(token)
    assert token == ''


def test_action_demojize():
    action = Action(action_name='unittest', action_condition='unittest')  # arguments are not important here
    token = Token('😰')
    action._demojize(token)
    assert token == ':anxious_face_with_sweat:'


def test_action_emojize():
    action = Action(action_name='unittest', action_condition='unittest')  # arguments are not important here
    token = Token(':joy:')
    action._emojize(token)
    assert token == "😂"


def test_action_tag():
    action = Action(action_name='tag', action_condition='is_emoji')  # arguments are not important here
    token = Token('😰')
    action._tag(token)
    assert token == '<EMOJI>'


@pytest.mark.parametrize(("action_obj", "expected"),
                         [(Action(action_name="", action_condition="is_hashtag"), False),  # action name is empty
                          (Action(action_name=None, action_condition="is_hashtag"), False),  # action name is None
                          (Action(action_name="tag", action_condition=""), False),  # action condition is empty
                          (Action(action_name="tag", action_condition=None), False),  # action condition is None
                          (Action(action_name="remove", action_condition="is_hashtag"), True),
                          (Action(action_name="tag", action_condition="is_hashtag"), True)])
def test_action_is_valid_action(action_obj, expected):
    token = Token("test")
    assert action_obj._is_valid_action(token) == expected


def test_action_apply_returning_true():
    action = Action(action_name="remove", action_condition="is_hashtag")
    assert action.apply(Token('#hashtag')) is True


def test_action_apply_returning_false():
    action = Action(action_name="remove", action_condition="is_hashtag")
    assert action.apply(Token('@hashtag')) is False
