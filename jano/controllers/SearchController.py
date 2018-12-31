import os
from multiprocessing import Process, Queue
from typing import List, Optional

from jano.exceptions import NoAzureKey, JunoException
from jano.search.bing import BingCrawler
from jano.search.google import GoogleCrawler
from jano.util import available_cpu_count


class SearchController(object):
    def __init__(self, ignore):
        self.__results = []
        self.ignore = ignore

    def bing_wrapper(self, query: str, q: Optional[Queue]):
        bing = BingCrawler(os.environ.get('MS_BING_KEY'), self.ignore)
        values = bing.search_relatives(query)
        if q is not None:
            q.put(values)
        return values

    def google_wrapper(self, query: str, q: Optional[Queue]):
        google = GoogleCrawler(self.ignore)
        values = google.search_relatives(query)
        if q is not None:
            q.put(values)
        return values

    def search(self, query: str) -> List:
        try:
            if not os.environ.get('MS_BING_KEY'):
                raise NoAzureKey("Uma chave do Bing deve estar em MS_BING_KEY")
            cpus = available_cpu_count()
            q = Queue()
            if cpus > 1:
                proc = Process(target=self.bing_wrapper, args=(query, q,)), Process(target=self.google_wrapper,
                                                                                    args=(query, q,))
                for p in proc:
                    p.start()
                result = q.get() + q.get()
            else:
                result = self.bing_wrapper(query, None) + self.google_wrapper(query, None)
                q.empty()
            return result
        except Exception as e:
            raise JunoException(e.__str__())
