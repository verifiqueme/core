import urllib.parse
from typing import List

import requests

from jano.config import Config
from jano.models.SearchObject import SearchObject
from jano.search.SearchInterface import SearchInterface


class GoogleCrawler(SearchInterface):
    def __init__(self, ignore):
        self.ignore = ignore

    def search_relatives(self, query: str) -> List[SearchObject]:
        """
        Busca as ocorrências de uma string (Query) no Google News
        :rtype: List[SearchObject]
        :param query: string a ser buscada
        :return: lista com os resultados
        """
        resultados = list()
        search_url = "http://news.verifique.me/search/" + urllib.parse.quote_plus(query)
        headers = {}
        params = {"lang": Config.values()['language']}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        values = response.json()
        for entrada in values["articles"]:
            if not self.ignore or self.ignore not in entrada.get('link'):
                modelo = SearchObject(entrada.get('title'), entrada.get('link'), entrada.get('description'),
                                      entrada.get('pubDate'))
                resultados.append(modelo)
        return resultados
