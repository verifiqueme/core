import numpy

from carmenta import score
from jano import Config
from pales.controllers.KerasController import KerasController


def translate_to_keras(url: str) -> list:
    info = dict()
    for head in Config.values()['headers']:
        info[head] = 0
    info.pop('result', None)
    data = score(url)
    for key in data['comparators'].keys():
        info[key] = data['comparators'][key]
    for key in data['semantic'].keys():
        info[key] = data['semantic'][key]
    return [[v for k, v in info.items()]]


def predict(url: str) -> list:
    """
    Prevê se uma notícia é verdadeira ou falsa (1 para verdadeiro, ou 0 para falsa)
    :param url: a URL a ser analisada
    :return: Retorna uma lista de probabilidade (1° coluna: chance de ser verdadeira, 2° coluna: chance de ser falsa)
    """
    keras = KerasController()
    return keras.keras_model().predict_proba(numpy.array(translate_to_keras(url)))[0]
