import pycld2

# The path for the statistics data

# Tags for different elements in the text preprocessing
EMOJI_TAG = '<EMOJI>'
MENTION_TAG = '<MENTION>'
HASHTAG_TAG = '<HASHTAG>'
UNENCODABLE_CHAR = '�'
URL_TAG = '<URL>'
DIGIT_TAG = '<DIGIT>'
EMOTICON_TAG = '<EMOTICON>'
PUNCTUATION_TAG = '<PUNCT>'
EMAIL_TAG = '<EMAIL>'

# Note: the following code is copied from sklearn

# This list of English stop words is taken from the "Glasgow Information
# Retrieval Group". The original list can be found at
# http://ir.dcs.gla.ac.uk/resources/linguistic_utils/stop_words
ENGLISH_STOP_WORDS = frozenset([
    "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill",
    "find", "fire", "first", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "my", "myself", "name", "namely", "neither",
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
    "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "should", "show", "side",
    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
    "very", "via", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    "yourselves"])

# Unknown language symbol, used in the language detection function
UNKNOWN_LANGUAGE = 'un'

# from http://bit.ly/2rdjgjE (UTF-8 encodings and Unicode chars)
VARIATION_SELECTORS = [u'\ufe00',
                       u'\ufe01',
                       u'\ufe02',
                       u'\ufe03',
                       u'\ufe04',
                       u'\ufe05',
                       u'\ufe06',
                       u'\ufe07',
                       u'\ufe08',
                       u'\ufe09',
                       u'\ufe0a',
                       u'\ufe0b',
                       u'\ufe0c',
                       u'\ufe0d',
                       u'\ufe0e',
                       u'\ufe0f']

# ngram separator, used in the statistic representation for the word segmentation
NGRAM_SEP = '_'
# ngrams statistics folder structure template
NGRAMS_SOURCE = 'NGRAMS-WIKI'
NGRAMS_VERSION = 'v2'

# two letters language codes (ISO 639-1)
# more details: https://en.wikipedia.org/wiki/ISO_639-1
JAPANESE_LANGUAGE_CODE = "ja"
CHINESE_LANGUAGE_CODE = "zh"
ENGLISH_LANGUAGE_CODE = "en"
FRENCH_LANGUAGE_CODE = "fr"
THAI_LANGUAGE_CODE = "th"
ARABIC_LANGUAGE_CODE = "ar"
SUPPORTED_LANGUAGES = [
    JAPANESE_LANGUAGE_CODE,
    CHINESE_LANGUAGE_CODE,
    ENGLISH_LANGUAGE_CODE,
    FRENCH_LANGUAGE_CODE,
    THAI_LANGUAGE_CODE,
    ARABIC_LANGUAGE_CODE
]

# PYCLD2 language set
PYCLD2_LANGUAGE_CODES = frozenset(code for _, code in pycld2.LANGUAGES)