from jano.models.SearchObject import SearchObject


class ArticleObject(SearchObject):
    def __init__(self, titulo, url, descricao, data, autor, domain, texto):
        super().__init__(titulo, url, descricao, data)
        self.author = autor
        self.domain = domain
        self.texto = texto
