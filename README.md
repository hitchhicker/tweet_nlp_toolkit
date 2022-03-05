![ci](https://github.com/hitchhicker/tweet_nlp_toolkit/actions/workflows/makefile.yml/badge.svg)

# tweet_nlp_toolkit
Tweet NLP toolkit

It can handle:
 - mentions
 - hashtags
 - emojis
 - emoticons
 - emails
 - HTML entities
 - digits
 - urls
 - punctuations
 - customized words to filter
## Installation
```
python3 -m venv .env
source .env/bin/activate
python -m pip install -U pip
pip install tweet_nlp_toolkit
```
## Usage
### Text Parsing
```python
>>> from tweet_nlp_toolkit import parse_text
>>> text = parse_text("123 @hello #world www.url.com 😰 :) abc@gmail.com")
>>> text.tokens
['123', '@hello', '#world', 'www.url.com', '😰', ':)', 'abc@gmail.com']
>>> text.hashtags
['world']
>>> text.mentions
['@hello']
>>> text.urls
['www.url.com']
>>> text.emojis
['😰']
>>> text.emoticons
[':)']
>>> text.digits
['123']
>>> text.emails
['abc@gmail.com']
```
### Tagging entities
```python
>>> from tweet_nlp_toolkit import parse_text
>>> parse_text(
...     "123 @hello #world www.url.com 😰 :) abc@gmail.com",
...     emojis="tag",
...     hashtags="tag",
...     mentions="tag"
... ).tokens
>>> ['123', '<MENTION>', '<HASHTAG>', 'www.url.com', '<EMOJI>', ':)', 'abc@gmail.com']
```

### Preprocessing
```python
>>> from tweet_nlp_toolkit import prep
>>> prep(
        "123 @hello #world www.url.com 😰 :) abc@gmail.com",
        emojis="demojize",
        mentions="remove",
        hashtags="remove",
        urls="remove",
        digits="tag",
        emails="remove"
... )
>>> '<DIGIT> :anxious_face_with_sweat: :)'
```

```
>>> from tweet_nlp_toolkit import prep_file
>>> prep_file("input.txt", "output.txt")
```
### More
`parse_text`, `prep` and `prep_file` share the same parameters, `parse_text` returns an instance of `ParsedText`,
`prep` returns the preprocessed string and `prep_file` preprocesses the file.
```
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
    Default False
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
```