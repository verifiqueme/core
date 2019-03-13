from carmenta.controllers.ArticleComparator import ArticleComparator
from carmenta.exceptions import InvalidJunoObject
from jano.models import ArticleObject


class EvaluateObjects(object):
    @staticmethod
    def evaluate(dados: dict) -> dict:
        resultados = {
            'title': 0,
            'corpus': 0
        }
        if 'original' not in dados and 'meta' not in dados:
            raise InvalidJunoObject("Dicionário deve ser um dicionário extraído de juno.extract_data")
        original: ArticleObject = dados['original']
        for relativo in dados['meta']:
            if relativo.data is not None and relativo.data.diff(original.data).in_days() <= 14:
                comparador = ArticleComparator.compare(original, relativo)
                resultados['title'] += comparador[0]
                resultados['corpus'] += comparador[1]
        resultados['title'] = round(resultados['title']/len(dados['meta']), 2) if resultados['title'] > 0 else 0
        resultados['corpus'] = round(resultados['corpus']/len(dados['meta']), 2) if resultados['corpus'] > 0 else 0
        return resultados
