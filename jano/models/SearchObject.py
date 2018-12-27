import pendulum

from jano.config import Config


class SearchObject(object):
    def __init__(self, titulo, url, descricao, data):
        self.titulo = titulo
        self.url = url
        self.descricao = descricao
        self.data = pendulum.parse(data, tz=Config().values()['timezone'], strict=False)
