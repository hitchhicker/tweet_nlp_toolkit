"""
Text parser.
"""
import html
import re
from typing import List, Optional, Callable, Set

from tweet_nlp_toolkit.constants import UNENCODABLE_CHAR
from tweet_nlp_toolkit.prep.regexes import LENGTHENING_PATTERN
from tweet_nlp_toolkit.prep.tokenizer import tweet_tokenize
from tweet_nlp_toolkit.prep.token import Token, Action
from tweet_nlp_toolkit.utils import strip_accents_unicode, remove_variation_selectors


class ParsedText:
    """Parsed Text"""

    __name__ = "ParsedText"

    def __init__(self, tokens: List[Token], split: str = " "):
        self._split = split
        self._tokens = tokens
        self._value: Optional[str] = None  # text in str

    def __repr__(self):
        return str([str(token) for token in self._tokens])

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        for token in self._tokens:
            yield token

    def __len__(self):
        return len(self._tokens)

    def __getitem__(self, item):
        return self._tokens[item]

    def __setitem__(self, key, value):
        self._tokens[key].value = value

    def process(
        self,
        mentions_action=None,
        hashtags_action=None,
        urls_action=None,
        digits_action=None,
        emojis_action=None,
        emoticons_action=None,
        puncts_action=None,
        emails_action=None,
        html_tags_action=None,
        stop_words_action=None,
    ):
        """Process tokens."""
        for token in self.tokens:
            for action in [
                Action(action_name=mentions_action, action_condition="is_mention"),
                Action(action_name=hashtags_action, action_condition="is_hashtag"),
                Action(action_name=urls_action, action_condition="is_url"),
                Action(action_name=digits_action, action_condition="is_digit"),
                Action(action_name=emojis_action, action_condition="is_emoji"),
                Action(action_name=emoticons_action, action_condition="is_emoticon"),
                Action(action_name=puncts_action, action_condition="is_punct"),
                Action(action_name=emails_action, action_condition="is_email"),
                Action(action_name=stop_words_action, action_condition="is_stop_word"),
                Action(action_name=html_tags_action, action_condition="is_html_tag"),
            ]:
                if token.do_action(action):
                    break
        self._tokens = [token for token in self.tokens if len(token)]  # filter removed tokens

    def post_process(self):
        text = self.value
        text = re.sub(r"\s+", " ", text)  # get rid of redundant spaces
        text = text.strip()
        self._value = text

    @property
    def value(self) -> str:
        if self._value is None:
            self._value = self._split.join(tok.value for tok in self._tokens)
        return self._value

    @property
    def tokens(self) -> List[Token]:
        return self._tokens

    @property
    def hashtags(self) -> List[str]:
        return list({token.value for token in self._tokens if token.is_hashtag})

    @property
    def mentions(self) -> List[str]:
        return [token.value for token in self._tokens if token.is_mention]

    @property
    def emoticons(self) -> List[str]:
        return [token.value for token in self._tokens if token.is_emoticon]

    @property
    def emojis(self) -> List[str]:
        return [token.value for token in self._tokens if token.is_emoji]

    @property
    def digits(self) -> List[str]:
        return [token.value for token in self._tokens if token.is_digit]

    @property
    def emails(self) -> List[str]:
        return [token.value for token in self._tokens if token.is_email]

    @property
    def urls(self) -> List[str]:
        return [token.value for token in self._tokens if token.is_url]


def parse_text(
    text: str,
    tokenizer: Callable[[str], List[Token]] = tweet_tokenize,
    encoding: str = "utf-8",
    remove_unencodable_char: bool = False,
    to_lower: bool = True,
    strip_accents: bool = False,
    reduce_len: bool = False,
    filters: Optional[Set[str]] = None,
    emojis: Optional[str] = None,
    mentions: Optional[str] = None,
    hashtags: Optional[str] = None,
    urls: Optional[str] = None,
    digits: Optional[str] = None,
    emoticons: Optional[str] = None,
    puncts: Optional[str] = None,
    emails: Optional[str] = None,
    html_tags: Optional[str] = None,
    stop_words: Optional[str] = None,
):
    """
    Preprocess the text

    Example:
        In [1]: from tweet_nlp_toolkit.prep.text_parser import parse_text

        In [2]: text = parse_text("123 @hello #world www.url.com 😰 :) abc@gmail.com", emails="remove", emojis="remove", emoticons="remove", urls="remove", digits="remove")  # noqa

        In [3]: text.tokens
        Out[3]: ['@hello', '#world']

        In [4]: text.hashtags
        Out[4]: ['#world']

        In [5]: text.mentions
        Out[5]: ['@hello']

        In [6]: text.value
        Out[6]: '@hello #world'

    Parameters
    ----------
    text: str
        The text to preprocess.
    tokenizer: Callable[[str], List[Token]]
        Tokenizer
    encoding: str
        The encoding of the text.
        Default "utf-8".
    remove_unencodable_char: bool
        In case of encoding error of a character it is replaced with '�'. This option allows removing the '�'.
        Otherwise a sequence of '�' is replaced by a single one
        Default False
    to_lower: bool
        Whether to convert the text to lowercase.
        Default True
    strip_accents: bool
        Whether to remove accents from latin characters.
        Default True
    reduce_len: bool
        Whether to remove repeated character sequences.
        Default False
    filters: set
        Tokens to filter (case sensitive).
        Default None
    emojis: Optional[str]
        How to handle emojis.
        Options:
            - "remove": remove all emojis
            - "tag": replaces the emoji by a tag <EMOJI>
            - "demojize": replaces the emoji by its textual representation, e.g. :musical_keyboard:
                list of emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
            - "emojize": replaces the emoji by its unicode representation, e.g. 😰
        Default None
    hashtags: Optional[str]
        How to handle hashtags.
        Options:
            - "remove": delete all hashtags
            - "tag"replaces the hashtag by a tag <HASHTAG>
        Default None
    urls: Optional[str]
        How to handle urls.
        Options:
            - "remove": delete all urls
            - "tag"replaces the url by a tag <URL>
        Default None
    mentions: Optional[str]
        How to handle mentions.
        Options:
            - "remove": delete all mentions
            - "tag"replaces the mention by a tag <MENTION>
        Default None
    digits: Optional[str]
        How to handle digits.
        Options:
            - "remove": delete all digits
            - "tag"replaces the digit by a tag <DIGIT>
        Default None
    emoticons: Optional[str]
        How to handle emoticons.
        Options:
            - "remove": delete all emoticons
            - "tag"replaces the emoticon by a tag <EMOTICON>
        Default None
    puncts: Optional[str]
        How to handle puncts.
        Options:
            - "remove": delete all puncts
            - "tag"replaces the puncts by a tag <PUNCT>
        Default None
    emails: Optional[str]
        How to handle puncts.
        Options:
            - "remove": delete all emails
            - "tag"replaces the emails by a tag <EMAIL>
        Default None
    html_tags: Optional[str]
        How to handle HTML tags like <div>.
        Options:
            - "remove": delete all HTML tags
        Default None
    html_tags: Optional[str]
        How to handle HTML tags like <div>.
        Options:
            - "remove": delete all HTML tags
        Default None
    stop_words: Optional[str]
        How to handle stop words.
        Options:
            - "remove": delete all HTML tags
        Default None
    stop_words
        How to handle stop words. Only English stop words are supported
        Options:
            - "remove"
        Default None

    Returns
    -------
        A ParsedText instance.
    """
    # TODO: check all parameters
    if filters is None:
        filters = set()
    if encoding is not None:
        text = text.encode(encoding, "surrogatepass").decode(encoding, "replace")
        if remove_unencodable_char:
            text = text.replace(UNENCODABLE_CHAR, " ")
        else:  # change any sequence of unknown characters to a single one
            text = re.sub(UNENCODABLE_CHAR + "{2,}", UNENCODABLE_CHAR, text)
    if to_lower:
        text = text.lower()
    if strip_accents:
        text = strip_accents_unicode(text)
    if reduce_len:
        text = reduce_lengthening(text)

    text = remove_variation_selectors(text)

    # separate URL from attached previous word e.g. asylum seeker:http://t.co/skU8zM7Slh
    text = re.sub(r"([^ ])(https?://)", r"\1 \2", text)

    text = re.sub(r"(\w+)\?(\w+)", r"\g<1>'\g<2>", text)  # c?est -> c'est

    text = html.unescape(text)  # &pound;100 -> £100
    tokens = [tk for tk in tokenizer(text) if tk not in filters]
    parsed_text = ParsedText(tokens=tokens)
    parsed_text.process(
        mentions_action=mentions,
        hashtags_action=hashtags,
        urls_action=urls,
        digits_action=digits,
        emojis_action=emojis,
        emoticons_action=emoticons,
        puncts_action=puncts,
        emails_action=emails,
        stop_words_action=stop_words,
        html_tags_action=html_tags,
    )
    parsed_text.post_process()
    return parsed_text


def reduce_lengthening(text):
    """
    Replace repeated character sequences of length 3 or greater with sequences
    of length 3.
    # This function is copy from nltk: https://www.nltk.org/_modules/nltk/tokenize/casual.html#TweetTokenizer
    """
    return LENGTHENING_PATTERN.sub(r"\1\1\1", text)
