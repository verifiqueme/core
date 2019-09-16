# -*- coding: utf-8 -*-
import base64
import json
import os
import re
from abc import ABC
from concurrent.futures import ThreadPoolExecutor

import pendulum
import tornado.ioloop
import tornado.web
import tornado.wsgi
from tinydb import TinyDB, Query
from tornado import httpserver
from tornado.concurrent import run_on_executor

from jano import available_cpu_count, extract_data
from jano.controllers.CacheController import CacheController
from jano.models.ArticleObject import ArticleObject
from pales.controllers.BuilderController import predict

MAX_WORKERS = available_cpu_count()
db = TinyDB('db.json')


def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    data = bytes(data, 'utf-8')  # normalize
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'=' * (4 - missing_padding)
    return base64.b64decode(data, altchars).decode("utf-8")


class BaseHandler(tornado.web.RequestHandler, ABC):
    def set_default_headers(self, *args, **kwargs):
        if os.environ.get('CORE_DEV'):
            self.set_header("Access-Control-Allow-Origin", "*")
            self.set_header("Access-Control-Allow-Headers", "x-requested-with, Origin, Content-Type, X-Auth-Token")


class IndexHandler(BaseHandler, ABC):
    async def hello(self):
        return "hello"

    async def get(self):
        self.write(await self.hello())


class RatingHandler(BaseHandler, ABC):
    async def hello(self):
        return "hello"

    async def get(self):
        self.write(await self.hello())

    async def options(self):
        self.write(await self.hello())

    def post(self):
        try:
            Rating = Query()
            url = str(self.get_argument('url'))
            rating = int(self.get_argument('rating'))
            table = db.table('rating')
            search = table.search(Rating.url == url)
            if search:
                if rating == 1:
                    table.update({'good': int(search[0]['good']) + rating}, Rating.url == url)
                else:
                    table.update({'bad': int(search[0]['bad']) + rating}, Rating.url == url)
            else:
                table.insert({'url': url, 'good': 1 if int(rating) == 1 else 0, 'bad': 1 if int(rating) != 1 else 0})
            data = "ok"
            self.set_status(201)
        except Exception as e:
            self.set_status(401)
            data = dict({"error": e.__str__()})
            print(data)
        self.write(json.dumps(data))


class APIHandler(BaseHandler, ABC):
    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    @run_on_executor
    def background_analyse(self, i):
        """ Isto sera executado em uma Pool. """
        result = predict(i)
        return str(result[0])

    @tornado.web.gen.coroutine
    def get(self, query):
        """ Chama a tarefa de fundo de forma assíncrona """
        try:
            url = decode_base64(query)
            res = yield self.background_analyse(url)
            metadados = extract_data(url)
            original: ArticleObject = metadados['original']
            words = 0
            for artigo in metadados["meta"]:
                assert isinstance(artigo, ArticleObject)
                words += len(artigo.texto)
            cache_age = CacheController.cacheAge(url).to_atom_string()
            age = cache_age if cache_age else "now"
            data = {
                "request": str(url),
                "info": {
                    "title": str(original.titulo),
                    "descricao": str(original.descricao),
                    "domain": str(original.domain),
                    "words": int(words),
                    "total": int(len(metadados['meta'])),
                    "age": age
                },
                "response": res
            }
            table = db.table('history')
            table.insert({'url': url, 'date': str(pendulum.now('America/Sao_Paulo'))})
            self.set_status(200)
        except Exception as e:
            self.set_status(401)
            data = dict({"error": e.__str__()})
        self.write(json.dumps(data))


def make_app(*args, **kwargs):
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/api/([\s\S]*)", APIHandler),
        (r"/rating", RatingHandler)
    ])
    return app


if __name__ == "__main__":
    print("Tornado it! Workers: {}".format(MAX_WORKERS))
    app = make_app()
    port = os.environ.get('PORT') if os.environ.get('PORT') else 8888

    if os.environ.get('CORE_MULTIPROCESSING'):
        server = httpserver.HTTPServer(app)
        server.bind(port)
        server.start(0)  # forks one process per cpu
    else:
        app.listen(port)
    tornado.ioloop.IOLoop.current().start()
