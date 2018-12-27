import urllib.parse

import requests

from jano.config import Config
from jano.models.SearchObject import SearchObject
from jano.search.SearchInterface import SearchInterface


class GoogleCrawler(SearchInterface):
    def __init__(self, ignore):
        self.ignore = ignore

    def search_relatives(self, query: str) -> list:
        resultados = list()
        search_url = "http://srv1.guiscaranse.ml:8087/search/" + urllib.parse.quote_plus(query)
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
