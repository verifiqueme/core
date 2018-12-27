import abc


class SearchInterface(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def search_relatives(self, query: str) -> dict:
        raise NotImplementedError('Deve implementar os metodos abstratos.')
