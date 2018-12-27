import _thread
from queue import Queue
from typing import List

from jano.config import Config
from jano.controllers.ArticleExtractor import ArticleExtractor
from jano.controllers.SearchController import SearchController
from jano.models import SearchObject
from jano.util import split_list, available_cpu_count


def extractor_wrapper(data: List, q: Queue):
    result = []
    mx = Config().values()['max_list']-1
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
    cpus = available_cpu_count()
    if len(data) > cpus > 1:
        list_parts = split_list(data, wanted_parts=cpus)
        queues = []
        results = []
        for l in list_parts:
            q = Queue()
            _thread.start_new_thread(extractor_wrapper, (l, q,))
            queues.append(q)
        for q in queues:
            q.join()
        for q in queues:
            results = results + q.get()
    dados['original'] = artigo
    return dados
