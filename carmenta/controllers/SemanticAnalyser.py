from polyglot.downloader import downloader
from polyglot.text import Text

from carmenta.util import filter_stopwords
from jano import Config


class SemanticAnalyser(object):
    @staticmethod
    def check_packages():
        packages = ["embeddings2.pt", "pos2.pt", "ner2.pt", "sentiment2.pt"]
        for package in packages:
            if not downloader.is_installed(package):
                print("Baixando {0}".format(package))
                downloader.download(package)
        return True

    def gramatica(self, texto: str) -> dict:
        """
        Analisa e conta cada token de um texto no formato explicado aqui: http://polyglot.readthedocs.io/en/latest/POS.html
        :param texto: Texto a ser analisado
        :return: Dicionário com as tags presentes e a quantia delas
        """
        resposta = dict()
        if len(texto) == 0:
            return dict()
        polyglot_text = Text(texto, hint_language_code=Config().values()['language'][:2])
        for word, tag in polyglot_text.pos_tags:
            if tag in resposta.keys():
                resposta[tag] += 1
            else:
                resposta[tag] = 1
        # Porcentagem
        total = sum(resposta.values())
        for tag in resposta.keys():
            resposta[tag] = round(resposta[tag] / total, 3)
        return resposta

    def polaridade(self, texto: str) -> dict:
        """
        Verifica a polaridade de um texto (sentimentos bons/ruins)
        :param texto: Texto a ser analisado
        :return: Polaridade em número
        """
        resultado = dict(good=0, bad=0)
        if len(texto) == 0:
            return dict()
        polyglot_text = Text(filter_stopwords(texto), hint_language_code=Config().values()['language'][:2])
        for w in polyglot_text.words:
            pol = w.polarity
            if pol < 0:
                resultado['bad'] += 1
            elif pol > 0:
                resultado['good'] += 1
        resultado['bad'] = round(resultado['bad'] / len(polyglot_text.words), 3)
        resultado['good'] = round(resultado['good'] / len(polyglot_text.words), 3)
        return resultado
