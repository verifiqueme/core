import numpy
import pandas as pd

from carmenta import count_words
from carmenta.controllers.EvaluateObjects import EvaluateObjects
from carmenta.controllers.SemanticAnalyser import SemanticAnalyser
from jano import extractor, Config
from jano.controllers.ArticleExtractor import ArticleExtractor
from jano.controllers.SearchController import SearchController
from jano.models.ArticleObject import ArticleObject


def extract_data(row) -> dict:
    dados = {
        "original": None,
        "meta": []
    }
    artigo = ArticleExtractor().extract(row['link'])
    find = SearchController("none")
    artigo_titulo = str(artigo.titulo).replace("#boato", "")
    data = find.search(artigo_titulo)
    results = extractor(data)
    dados["meta"] = results
    dados['original'] = ArticleObject(artigo_titulo, row['link'], "none", row['timestamp'], "none", "none", row['hoax'])
    return dados


def score(row) -> dict:
    data = {
        'comparators': [],
        'semantic': []
    }
    SemanticAnalyser.check_packages()
    jano_data = extract_data(row)
    evaluation = EvaluateObjects.evaluate(jano_data)
    data['comparators'] = evaluation
    data['semantic'] = {**SemanticAnalyser.gramatica(jano_data['original'].texto),
                        **SemanticAnalyser.polaridade(jano_data['original'].texto)}
    data['semantic']['length'] = count_words(jano_data['original'].texto)
    return data


def translate_to_keras(row) -> list:
    info = dict()
    for head in Config.values()['headers']:
        info[head] = 0
    info.pop('result', None)
    data = score(row)
    for key in data['comparators'].keys():
        info[key] = data['comparators'][key]
    for key in data['semantic'].keys():
        info[key] = data['semantic'][key]
    return [v for k, v in info.items()]


df = pd.read_csv('boatos.csv', header=0)
for index, row in df.iterrows():
    try:
        print(index)
        result = translate_to_keras(row) + [0.0]
        with open("test.csv", "a") as myfile:
            myfile.write(str(result) + "\n")
    except Exception:
        pass