![ci](https://github.com/hitchhicker/tweet_nlp_toolkit/actions/workflows/makefile.yml/badge.svg)

# tweet_nlp_toolkit
Tweet NLP toolkit
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
>>> from tweet_nlp_toolkit.prep.text_parser import parse_text
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
### More
```python
:param text: string, the text to preprocess
:param tokenizer: Callable[[str], List[Token]], optional
:param encoding: the encoding of the text, default to "utf-8"
:param remove_unencodable_char: in case of encoding error of a character it is replaced with '�'.
This option allows removing the '�'. Otherwise a sequence of '�' is replaced by a single one
:param to_lower: whether to convert the text to lowercase
:param strip_accents: whether to remove accents from latin characters
:param reduce_len: whether to remove repeated character sequences
:param filters: the set of token to filter (case sensitive)
:param emojis: how to handle emojis. Default: no special treatment.
Options: - 'remove': delete all emojis
         - 'tag': replaces the emoji by a tag <EMOJI>
         - 'demojize': replaces the emoji by its textual representation, e.g. :musical_keyboard:
            list of emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
         - 'emojize: replaces the emoji by its unicode representation, e.g. 😰
:param hashtags: how to treat hashtags. Options: remove/tag (similar behavior as for emojis).
:param urls: how to treat hashtags. Options: remove/tag
:param mentions: how to treat mentions. Options: remove/tag
:param digits: how to treat digits. Options: remove/tag
:param emoticons: how to treat emoticons. Options: remove/tag
:param puncts: how to treat puncts. Options: remove/tag
:param emails: how to treat emails. Options: remove/tag
:param html_tags: how to treat html tags. Options: remove
:param stop_words: how to treat stop words. Options: remove
:return: a ParsedText instance
"""
```