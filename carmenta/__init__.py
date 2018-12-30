import jano
from carmenta.controllers.EvaluateObjects import EvaluateObjects
from carmenta.controllers.SemanticAnalyser import SemanticAnalyser


def score(url: str) -> dict:
    data = {
        'comparators': [],
        'semantic': []
    }
    SemanticAnalyser.check_packages()
    jano_data = jano.extract_data(url)
    evaluation = EvaluateObjects.evaluate(jano_data)
    data['comparators'] = evaluation
    data['semantic'] = {**SemanticAnalyser.gramatica(jano_data['original'].texto),**SemanticAnalyser.polaridade(jano_data['original'].texto)}
    return data
