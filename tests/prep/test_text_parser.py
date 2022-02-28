import pytest
from pytest import fixture

from tweet_nlp_toolkit.prep.text_parser import ParsedText, parse_text
from tweet_nlp_toolkit.prep.token import Token, WeiboToken
from tweet_nlp_toolkit.prep.tokenizer import weibo_tokenize


@fixture
def mocked_text_parser():
    tokens = [
        Token('<p>'),
        Token('c\'est'),
        Token('</p>'),
        Token('@nlp'),
        Token('https://www.google.fr'),
        Token('cant'),
        Token('wait'),
        Token('😰'),
        Token('for'),
        Token('the'),
        Token('new'),
        Token('season'),
        Token('of'),
        Token('tutu@gmail.com'),
        Token(r'\(^o^)/'),
        Token('123'),
        Token('!'),
        Token('!'),
        Token('#davidlynch'),
        Token('#tvseries'),
        Token('#tvseries'),
        Token(':))))')
    ]
    return ParsedText(tokens=tokens)


def test_text_parser_value(mocked_text_parser):
    assert mocked_text_parser.value == r"<p> c'est </p> @nlp https://www.google.fr cant wait 😰 for the new season of tutu@gmail.com \(^o^)/ 123 ! ! #davidlynch #tvseries #tvseries :))))"


def test_text_parser__str__(mocked_text_parser):
    assert str(
        mocked_text_parser) == r"""['<p>', "c'est", '</p>', '@nlp', 'https://www.google.fr', 'cant', 'wait', '😰', 'for', 'the', 'new', 'season', 'of', 'tutu@gmail.com', '\\(^o^)/', '123', '!', '!', '#davidlynch', '#tvseries', '#tvseries', ':))))']"""


def test_text_parser__repr__(mocked_text_parser):
    assert repr(
        mocked_text_parser) == r"""['<p>', "c'est", '</p>', '@nlp', 'https://www.google.fr', 'cant', 'wait', '😰', 'for', 'the', 'new', 'season', 'of', 'tutu@gmail.com', '\\(^o^)/', '123', '!', '!', '#davidlynch', '#tvseries', '#tvseries', ':))))']"""


def test_text_parser__len__(mocked_text_parser):
    assert len(mocked_text_parser) == 22
    assert len(mocked_text_parser) == 22


def test_text_parser__getitem__(mocked_text_parser):
    assert mocked_text_parser[1].value == 'c\'est'


def test_text_parser__setitem__(mocked_text_parser):
    mocked_text_parser[1] = 'cest'
    assert mocked_text_parser[1].value == 'cest'


def test_text_parser_post_process(mocked_text_parser):
    mocked_text_parser.tokens[0].value = ' <p>'
    assert mocked_text_parser.value == r" <p> c'est </p> @nlp https://www.google.fr cant wait 😰 for the new season of tutu@gmail.com \(^o^)/ 123 ! ! #davidlynch #tvseries #tvseries :))))"
    mocked_text_parser.post_process()
    assert mocked_text_parser.value == r"<p> c'est </p> @nlp https://www.google.fr cant wait 😰 for the new season of tutu@gmail.com \(^o^)/ 123 ! ! #davidlynch #tvseries #tvseries :))))"


@pytest.mark.parametrize(("kwargs", "expected_value"),
                         [({'mentions_action': 'tag'},
                           r"<p> c'est </p> <MENTION> https://www.google.fr cant wait 😰 for the new season of tutu@gmail.com \(^o^)/ 123 ! ! #davidlynch #tvseries #tvseries :))))"),
                          ({'mentions_action': 'remove'},
                           r"<p> c'est </p> https://www.google.fr cant wait 😰 for the new season of tutu@gmail.com \(^o^)/ 123 ! ! #davidlynch #tvseries #tvseries :))))",),
                          ({'urls_action': 'tag'},
                           r"<p> c'est </p> @nlp <URL> cant wait 😰 for the new season of tutu@gmail.com \(^o^)/ 123 ! ! #davidlynch #tvseries #tvseries :))))"),
                          ({'urls_action': 'remove'},
                           r"<p> c'est </p> @nlp cant wait 😰 for the new season of tutu@gmail.com \(^o^)/ 123 ! ! #davidlynch #tvseries #tvseries :))))"),
                          ({'digits_action': 'tag'},
                           r"<p> c'est </p> @nlp https://www.google.fr cant wait 😰 for the new season of tutu@gmail.com \(^o^)/ <DIGIT> ! ! #davidlynch #tvseries #tvseries :))))"),
                          ({'emojis_action': 'tag'},
                           r"<p> c'est </p> @nlp https://www.google.fr cant wait <EMOJI> for the new season of tutu@gmail.com \(^o^)/ 123 ! ! #davidlynch #tvseries #tvseries :))))"),
                          ({'emojis_action': 'remove'},
                           r"<p> c'est </p> @nlp https://www.google.fr cant wait for the new season of tutu@gmail.com \(^o^)/ 123 ! ! #davidlynch #tvseries #tvseries :))))"),
                          ({'emojis_action': 'demojize'},
                           r"<p> c'est </p> @nlp https://www.google.fr cant wait :anxious_face_with_sweat: for the new season of tutu@gmail.com \(^o^)/ 123 ! ! #davidlynch #tvseries #tvseries :))))"),
                          ({'emoticons_action': 'tag'},
                           r"<p> c'est </p> @nlp https://www.google.fr cant wait 😰 for the new season of tutu@gmail.com <EMOTICON> 123 ! ! #davidlynch #tvseries #tvseries <EMOTICON>"),
                          ({'emoticons_action': 'remove'},
                           r"<p> c'est </p> @nlp https://www.google.fr cant wait 😰 for the new season of tutu@gmail.com 123 ! ! #davidlynch #tvseries #tvseries"),
                          ({'puncts_action': 'tag'},
                           r"<p> c'est </p> @nlp https://www.google.fr cant wait 😰 for the new season of tutu@gmail.com \(^o^)/ 123 <PUNCT> <PUNCT> #davidlynch #tvseries #tvseries :))))"),
                          ({'puncts_action': 'remove'},
                           r"<p> c'est </p> @nlp https://www.google.fr cant wait 😰 for the new season of tutu@gmail.com \(^o^)/ 123 #davidlynch #tvseries #tvseries :))))"),
                          ({'emails_action': 'tag'},
                           r"<p> c'est </p> @nlp https://www.google.fr cant wait 😰 for the new season of <EMAIL> \(^o^)/ 123 ! ! #davidlynch #tvseries #tvseries :))))"),
                          ({'emails_action': 'remove'},
                           r"<p> c'est </p> @nlp https://www.google.fr cant wait 😰 for the new season of \(^o^)/ 123 ! ! #davidlynch #tvseries #tvseries :))))"),
                          ({'html_tags_action': 'remove'},
                           r"c'est @nlp https://www.google.fr cant wait 😰 for the new season of tutu@gmail.com \(^o^)/ 123 ! ! #davidlynch #tvseries #tvseries :))))"),
                          ])
def test_text_parser_process(mocked_text_parser, kwargs, expected_value):
    mocked_text_parser.process(**kwargs)
    assert mocked_text_parser.value == expected_value


def test_text_parser_hashtags(mocked_text_parser):
    assert sorted(mocked_text_parser.hashtags) == sorted(['davidlynch', 'tvseries'])


def test_text_parser_mentions(mocked_text_parser):
    assert mocked_text_parser.mentions == ['@nlp']


def test_text_parser_emoticons(mocked_text_parser):
    assert mocked_text_parser.emoticons == [r'\(^o^)/', ':))))']


def test_text_parser_emojis(mocked_text_parser):
    assert mocked_text_parser.emojis == ['😰']


def test_text_parser_digits(mocked_text_parser):
    assert mocked_text_parser.digits == ['123']


def test_text_parser_emails(mocked_text_parser):
    assert mocked_text_parser.emails == ['tutu@gmail.com']


def test_text_parser_urls(mocked_text_parser):
    assert mocked_text_parser.urls == ['https://www.google.fr']


def test_text_parser_when_there_is_emoji():
    assert parse_text(
        text="July @AlraashidS @shalsaeedi_ @asaldhferi @Fa3ix_ @iiBeba_ @_hajaraljble ❤️",
        mentions='remove',
        emojis='remove'
    ).value == u'july'


def test_text_parser_with_attached_url():
    text = "asylum seeker:http://t.co/skU8zM7Slh"
    assert parse_text(
        text=text,
        urls='remove',
    ).value == 'asylum seeker :'

    assert parse_text(
        text=text,
        urls='tag'
    ).value == 'asylum seeker : <URL>'


@pytest.mark.parametrize(("text", "expected"), [
    ("@abc:joy:#hashtag",
     "@abc 😂 #hashtag")
])
def test_text_parser_with_emoji_string(text, expected):
    assert parse_text(
        text=text,
        emojis='emojize').value == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (
                "@招商银行 我只是想#改个电话号码#而已。",
                ParsedText(
                    tokens=[
                        WeiboToken('<MENTION>'),
                        WeiboToken('我'),
                        WeiboToken('只是'),
                        WeiboToken('想'),
                        WeiboToken('#改个电话号码#'),
                        WeiboToken('而已'),
                        WeiboToken('。')
                    ]
                )
        ),
    ]
)
def test_text_parser_with_weibo_token_cls(text, expected):
    parsed_text = parse_text(
        text,
        tokenizer=weibo_tokenize,
        mentions='tag'
    )
    assert parsed_text.tokens == expected.tokens
    assert parsed_text.hashtags == ['改个电话号码']
