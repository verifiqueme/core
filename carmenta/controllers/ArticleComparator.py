from typing import Tuple

from fuzzywuzzy import fuzz

from carmenta.util import filter_stopwords
from jano.models import ArticleObject


class ArticleComparator(object):
    @staticmethod
    def compare(a1: ArticleObject, a2: ArticleObject) -> Tuple[int, int]:
        title = fuzz.token_sort_ratio(filter_stopwords(a1.titulo), filter_stopwords(a2.titulo))
        corpus = fuzz.token_set_ratio(filter_stopwords(a1.texto), filter_stopwords(a2.texto))
        return title, corpus
