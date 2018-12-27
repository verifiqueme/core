import requests

from jano.config import Config
from jano.models.SearchObject import SearchObject
from jano.search.SearchInterface import SearchInterface


class BingCrawler(SearchInterface):
    def __init__(self, key, ignore):
        self.AzureKey = key
        self.ignore = ignore

    def search_relatives(self, query: str) -> list:
        resultados = list()
        search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"
        headers = {"Ocp-Apim-Subscription-Key": str(self.AzureKey)}
        params = {"q": query, "textDecorations": True, "textFormat": "HTML", "count": 50, "offset": 0,
                  "setLang": Config.values().country, "mkt": Config.values().language}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        values = response.json()
        for entrada in values["value"]:
            modelo = SearchObject(entrada.get('name'), entrada.get('url'), entrada.get('description'),
                                  entrada.get('datePublished'))
            resultados.append(modelo)
        return resultados
