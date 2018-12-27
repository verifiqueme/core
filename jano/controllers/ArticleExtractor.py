from newsplease import NewsPlease

from jano.config import Config
from jano.exceptions import TextUnavailable
from jano.models.ArticleObject import ArticleObject
from jano.util import fixcharset


class ArticleExtractor(object):
    @staticmethod
    def extract(url: str) -> ArticleObject:
        try:
            artigo = NewsPlease.from_url(url, timeout=5)
            # Definir Texto
            if artigo.text is not None:
                text = fixcharset(artigo.text)
            elif artigo.description is not None:
                text = fixcharset(artigo.description)
            else:
                raise TextUnavailable("Não existem textos disponíveis no NewsPlease para análise. Tente com Goose3")
            # Definir data
            if artigo.date_publish is not None:
                data = str(artigo.date_publish)
            elif artigo.date_modify is not None and artigo.date_modify is not "None":
                data = str(artigo.date_modify)
            else:
                data = str(artigo.date_download)

            objeto = ArticleObject(fixcharset(artigo.title), url, None, data, artigo.authors,
                                   artigo.source_domain, text)
            return objeto
        except Exception:
            from goose3 import Goose
            g = Goose(
                {'strict': False, 'use_meta_language': True,
                 'target_language': Config().values()['language'].replace("-", "_"),
                 'parser_class': 'lxml', 'enable_image_fetching': False})
            artigo = g.extract(url=url)
            if artigo.cleaned_text:
                text = fixcharset(artigo.cleaned_text)
            elif artigo.meta_description:
                text = fixcharset(artigo.meta_description)
            else:
                raise TextUnavailable("Não existem textos suficientes para análise.")

            objeto = ArticleObject(fixcharset(artigo.title), url, None,
                                   artigo.publish_date, artigo.authors, artigo.domain, text)
            return objeto
