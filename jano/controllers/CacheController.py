import hashlib
import os
import pickle
from typing import Union

import pendulum

from carmenta.exceptions import InvalidJunoObject
from jano import Config
from jano.util import jano_index


class CacheController(object):
    @staticmethod
    def getCache(url: str) -> Union[dict, bool]:
        hashed = hashlib.sha224(str(url).encode('utf-8')).hexdigest()
        cache = os.path.normpath(jano_index() + os.path.normcase("/cache/{0}.jcache".format(hashed)))
        if os.path.isfile(cache):
            time = pendulum.from_timestamp(os.path.getmtime(cache))
            now = pendulum.now(Config.values()['timezone'])
            if now.diff(time).in_days() >= 2:
                os.remove(cache)
                return False
            return pickle.load(open(cache, "rb"))
        else:
            return False

    @staticmethod
    def cacheAge(url: str):
        hashed = hashlib.sha224(str(url).encode('utf-8')).hexdigest()
        cache = os.path.normpath(jano_index() + os.path.normcase("/cache/{0}.jcache".format(hashed)))
        if os.path.isfile(cache):
            time = pendulum.from_timestamp(os.path.getmtime(cache))
            return time
        else:
            return False

    @staticmethod
    def createCache(dados: dict) -> bool:
        if 'original' not in dados and 'meta' not in dados:
            raise InvalidJunoObject("Dicionário deve ser um dicionário extraído de juno.extract_data")
        hashed = hashlib.sha224(str(dados['original'].url).encode('utf-8')).hexdigest()
        cache = os.path.normpath(jano_index() + os.path.normcase("/cache/{0}.jcache".format(hashed)))
        pickle_out = open(cache, "wb")
        pickle.dump(dados, pickle_out)
        pickle_out.close()
        return True
