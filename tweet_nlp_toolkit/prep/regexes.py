"""
Important note:
The following expressions are modified from
    https://github.com/cbaziotis/ekphrasis/blob/master/ekphrasis/regexes/generate_expressions.py
and
    https://www.nltk.org/_modules/nltk/tokenize/casual.html#TweetTokenizer
"""
import re

HASHTAG = r"\#\b[\w\-\_]+\b"
WEIBO_HASHTAG = r"\#[^#]+#"
NOT_A_HASHTAG = r"\#\b[\d]+\b"
# Thai vowels range from \u0e00 to \u0e7f, reference: https://www.compart.com/en/unicode/scripts/Thai
WORD = r"(?:[^\W\d|(?:_](?:[^\W\d_]|['\-_]|[\u0e00-\u0e7f])+[^\W\d_]?)[^\W\d\w_]?"
MENTION = r"\@\w+"

_ltr_emoticon = [
    # optional hat
    r"(?:(?<![a-zA-Z])[DPO]|(?<!\d)[03]|[|}><=])?",
    # eyes
    r"(?:(?<![a-zA-Z\(])[xXB](?![a-ce-oq-zA-CE-OQ-Z,\.\/])|(?<![:])[:=|](?![\.])|(?<![%#\d])[%#](?![%#\d])|(?<![\d\$])[$](?![\d\.,\$])|[;](?!\()|(?<![\d\(\-\+])8(?![\da-ce-zA-CE-Z\\/])|\*(?![\*\d,.]))",
    # pylint: disable=line-too-long
    # optional tears
    r"(?:['\",])?",
    # optional nose
    r"(?:(?<![\w*])[oc](?![a-zA-Z])|(?:[-‑^]))?",
    # mouth
    r"(?:[(){}\[\]<>|/\\]+|[Þ×þ]|(?<!\d)[30](?!\d)|(?<![\d\*])[*,.@#&](?![\*\d,.])|(?<![\d\$])[$](?![\d\.,\$])|[DOosSJLxXpPbc](?![a-zA-Z]))",
]

_rtl_emoticon = [
    r"(?<![\w])",
    r"(?:[(){}\[\]<>|/\\]+|(?<![\d\.\,])[0](?![\d\.])|(?![\d\*,.@#&])[*,.@#&]|[$]|(?<![a-zA-Z])[DOosSxX])",
    # mouth
    r"(?:[-‑^])?",  # optional nose
    r"(?:['\",])?",  # optional tears
    r"(?:[xX]|[:=|]|[%#]|[$8](?![\d\.])|[;]|\*)",  # eyes
    r"(?:[O]|[0]|[|{><=])?",  # optional hat
    r"(?![a-zA-Z])",
]
_LTR_FACE = "".join(_ltr_emoticon)
_RTL_FACE = "".join(_rtl_emoticon)
_EASTERN_EMOTICONS = r"(?<![\w])(?:(?:[<>]?[\^;][\W_m][\;^][;<>]?)|(?:[^\s()]?m?[\(][\W_oTOJ]{1,3}[\s]?[\W_oTOJ]{1,3}[)]m?[^\s()]?)|(?:\*?[v>\-\/\\][o0O\_\.][v\-<\/\\]\*?)|(?:[oO0>][\-_\/oO\.\\]{1,2}[oO0>])|(?:\^\^))(?![\w])"  # pylint: disable=line-too-long
_REST_EMOTICONS = r"(?<![A-Za-z0-9/()])(?:(?:\^5)|(?:\<3))(?![[A-Za-z0-9/()])"
EMOTICONS = "|".join([_LTR_FACE, _RTL_FACE, _EASTERN_EMOTICONS, _REST_EMOTICONS])
EMAIL = r"(?:^|(?<=[^\w@.)]))(?:[\w+-](?:\.(?!\.))?)*?[\w+-]@(?:\w-?)*?\w+(?:\.(?:[a-z]{2,})){1,3}(?:$|(?=\b))"
URL = r"(?:https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})"
CAMEL_SPLIT = r"((?<=[a-z])[A-Z]|(?<!^)[A-Z](?=[a-z])|[0-9]+|(?<=[0-9\\-\\_])[A-Za-z]|[\\-\\_])"
HTML_TAG = r"""<[^>\s]+>"""
ASCII_ARROW = r"""[\-]+>|<[\-]+"""
DIGIT = r"(?:[+\-]?\d+[,/.:-]?\d*[+\-]?)"
ELLIPSIS_DOTS = r"(?:\.(?:\s*\.){1,})"
EMOJI_STRING = r"(?::\w+:)"

# === Patterns ===

QUOTES_PAT = re.compile("[“”«»]")
APOSTROPHES_PAT = re.compile("[‘’]")
URL_PAT = re.compile(URL)
RT_MENTION_PAT = re.compile(r"^RT " + MENTION + ": ")
