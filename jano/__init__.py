from jano.controllers.ArticleExtractor import ArticleExtractor
from jano.controllers.SearchController import SearchController
from jano.models import SearchObject


def extract_data(url: str) -> dict:
    dados = {
        "original": None,
        "metarelativos": []
    }
    artigo = ArticleExtractor().extract(url)
    find = SearchController(artigo.domain)
    data = find.search(artigo.titulo)
    for dado in data:
        dados['metarelativos'].append(ArticleExtractor().extract(dado.url))
    return dados
