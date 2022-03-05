import pytest

from tweet_nlp_toolkit.prep.token import Token, WeiboToken
from tweet_nlp_toolkit.prep.tokenizer import TwitterTokenizer, white_space_tokenize, \
    SocialMediaTokenizer, WhiteSpaceTokenizer, social_media_tokenize, Detokenizer, chinese_tokenize, japanese_tokenize, \
    _is_chinese, _is_japanese, thai_tokenize, _is_thai, weibo_tokenize


def test_default_init_tokenizer():
    assert type(TwitterTokenizer()._tknzr) == SocialMediaTokenizer


def test_nltk_init_tokenizer():
    assert type(TwitterTokenizer(tokenizer='naive')._tknzr) == WhiteSpaceTokenizer
    assert type(TwitterTokenizer(tokenizer='social_media')._tknzr) == SocialMediaTokenizer


def test_error_init_tokenizer():
    with pytest.raises(NotImplementedError):
        _ = TwitterTokenizer(tokenizer='xxx')


@pytest.mark.parametrize(("text", "expected_tokens"),
                         [(" @remy: This is waaaaayyyy too much for you",
                           ['@remy:', 'This', 'is', 'waaaaayyyy', 'too', 'much', 'for', 'you']),
                          ("", [])])
def test_white_space_tokenize(text, expected_tokens):
    assert white_space_tokenize(text) == expected_tokens


@pytest.mark.parametrize(("text", "expected_tokens"),
                         [("", []),
                          (" คลับพาราไดซ์, จะถูกต้อง. วันสุดท้ายทุกสิ่งที่ดูเหมือนว่าตกลง",
                           ["คลับพาราไดซ์", ",", "จะถูกต้อง", ".", "วันสุดท้ายทุกสิ่งที่ดูเหมือนว่าตกลง"])])
def test_social_media_tokenize(text, expected_tokens):
    tokens = social_media_tokenize(text)
    assert tokens == expected_tokens


def test_detokenizer():
    en_detok = Detokenizer()
    assert en_detok.detokenize(['Hello', 'World', '!']) == 'Hello World!'
    assert en_detok.detokenize(
        'Paris , Lyon , and Grenoble .'.split(' ')) == 'Paris, Lyon, and Grenoble.'

    text = 'Réformes des retraites : Macron "n\'est pas...\", dit Mazerolle'
    fr_detok = Detokenizer(lang='fr')
    assert fr_detok.detokenize(
        ['Réformes', 'des', 'retraites', ':', 'Macron', '"', "n'est", 'pas', '...', '"', ',', 'dit',
         'Mazerolle']) == text

    # check that the tokenization is reversible by the detokenization
    assert fr_detok.detokenize(list(map(str, social_media_tokenize(text)))) == text


@pytest.mark.parametrize(("text", "expected_tokens"),
                         [
                             ("", []),  # empty input
                             (
                                     "我这个星期六工作",  # plain Chinese
                                     ["我", "这个", "星期六", "工作"]
                             ),
                             (
                                     "#996 oh my god ! 我这个星期六工作 post english",  # mix English and Chinese
                                     ["#996", "oh", "my", "god", "!", "我", "这个", "星期六", "工作", "post", "english"]
                             )])
def test_chinese_tokenize(text, expected_tokens):
    assert chinese_tokenize(text) == expected_tokens


@pytest.mark.parametrize(("text", "expected_tokens"),
                         [
                             ("", []),  # empty input
                             (
                                     "私は土曜日に出勤します。",  # plain Japanese
                                     ['私', 'は', '土曜日', 'に', '出勤', 'し', 'ます', '。']
                             ),
                             (
                                     "#996 oh my god ! 私は土曜日に出勤します。 post english",  # mix English and Japanese
                                     ["#996", "oh", "my", "god", "!", '私', 'は', '土曜日', 'に', '出勤', 'し', 'ます', '。',
                                      "post",
                                      "english"]
                             )])
def test_japanese_tokenize(text, expected_tokens):
    assert japanese_tokenize(text) == expected_tokens


@pytest.mark.parametrize(("text", "expected_tokens"),
                         [
                             ("", []),  # empty input
                             (
                                     "ฉันทำงานวันเสาร์นี้",  # plain Thai
                                     ['ฉัน', 'ทำงาน', 'วัน', 'เสาร์', 'นี้']
                             ),
                             (
                                     "#996 oh my god ! ฉันทำงานวันเสาร์นี้ post english",  # mix English and Thai
                                     ["#996", "oh", "my", "god", "!", 'ฉัน', 'ทำงาน', 'วัน', 'เสาร์', 'นี้', "post",
                                      "english"]
                             )])
def test_thai_tokenizer(text, expected_tokens):
    assert thai_tokenize(text) == expected_tokens


@pytest.mark.parametrize(("cp", "expected"),
                         [(ord("は"), True),
                          (ord("工"), True)])
def test_is_japanese(cp, expected):
    assert _is_japanese(cp) == expected


@pytest.mark.parametrize(("cp", "expected"),
                         [(ord("は"), False),
                          (ord("工"), True)])
def test_is_chinese(cp, expected):
    assert _is_chinese(cp) == expected


def test_is_thai():
    assert _is_thai(ord("ส")) is True


@pytest.mark.parametrize(
    ("text", "expected"),
    [("#全国已确诊新型肺炎病例319例#中国加油!", ["#全国已确诊新型肺炎病例319例#", "中国", "加油", "!"])]
)
def test_weibo_tokenize_with_segment_hashtag_as_false(text, expected):
    assert weibo_tokenize(text, segment_hashtag=False) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [("#全国已确诊新型肺炎病例319例#中国加油!", ["#", "全国", "已", "确诊", "新型", "肺炎", "病例", "319", "例", "#", "中国", "加油", "!"])]
)
def test_weibo_tokenize_with_segment_hashtag_as_true(text, expected):
    assert weibo_tokenize(text, segment_hashtag=True) == expected


def test_social_media_tokenize_return_type():
    assert type(social_media_tokenize("unit test")[0]) == Token


def test_white_space_tokenize_return_type():
    assert type(white_space_tokenize("unit test")[0]) == Token


def test_weibo_tokenize_return_type():
    assert type(weibo_tokenize("unit test")[0]) == WeiboToken
