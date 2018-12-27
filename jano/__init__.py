import _thread
from queue import Queue
from typing import List

from jano.config import Config
from jano.controllers.ArticleExtractor import ArticleExtractor
from jano.controllers.SearchController import SearchController
from jano.models import SearchObject
from jano.util import split_list


def extractor_wrapper(data: List, q: Queue):
    result = []
    mx = Config().values()['max_list']
    del result[mx:]
    for dado in data:
        try:
            result.append(ArticleExtractor().extract(dado.url))
        except Exception:
            pass
    q.put(result)
    q.task_done()


def extract_data(url: str) -> dict:
    dados = {
        "original": None,
        "metarelativos": []
    }
    artigo = ArticleExtractor().extract(url)
    find = SearchController(artigo.domain)
    data = find.search(artigo.titulo)
    if len(data) > 5:
        l1, l2 = split_list(data, wanted_parts=2)
        q1, q2 = Queue(), Queue()
        _thread.start_new_thread(extractor_wrapper, (l1, q1,))
        _thread.start_new_thread(extractor_wrapper, (l2, q2,))
        q1.join()
        q2.join()
        dados['metarelativos'] = q1.get() + q2.get()
    dados['original'] = data
    return dados
