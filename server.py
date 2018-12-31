import base64
import json
from abc import ABC
from concurrent.futures import ThreadPoolExecutor

import tornado.ioloop
import tornado.web
from tornado import httpserver
from tornado.concurrent import run_on_executor

from jano import available_cpu_count
from pales.controllers.BuilderController import predict

MAX_WORKERS = available_cpu_count() * 5


class APIHandler(tornado.web.RequestHandler, ABC):
    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

    @run_on_executor
    def background_task(self, i):
        """ Isto será executado em uma Pool. """
        result = predict(i)
        return result[0]

    @tornado.web.gen.coroutine
    def get(self, query):
        """ Chama a tarefa de fundo de forma assíncrona """
        data = base64.urlsafe_b64decode(query)
        res = yield self.background_task(data)
        data = {
            "response": res
        }
        self.write(json.dumps(data))


class Teste(tornado.web.RequestHandler, ABC):
    async def teste(self):
        return "hello"

    async def get(self):
        self.write(await self.teste())


def make_app():
    return tornado.web.Application([
        (r"/", Teste),
        (r"/api/([\s\S]*)", APIHandler),
    ])


if __name__ == "__main__":
    print("Tornado it!")
    app = make_app()
    server = httpserver.HTTPServer(app)
    server.bind(8888)
    server.start(0)  # forks one process per cpu
    tornado.ioloop.IOLoop.current().start()
