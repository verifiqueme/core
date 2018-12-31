import nltk
from nltk.corpus import stopwords
from polyglot.text import Text

from jano import Config


def filter_stopwords(texto: str) -> str:
    """
    Filtra stopwords, removendo-as
    :param texto: Texto a ser filtrado
    :return: Texto filtrado
    """
    try:
        nltk.data.find('corpora\stopwords')
    except LookupError:
        nltk.download('stopwords')
    if len(texto) == 0:
        return ""
    p_stopwords = set(stopwords.words('portuguese'))
    filtered = (w for w in texto.split() if w.lower() not in p_stopwords)
    return " ".join(filtered)


def count_words(texto: str) -> int:
    polyglot_text = Text(filter_stopwords(texto), hint_language_code=Config.values()['language'][:2])
    return len(polyglot_text.words)
