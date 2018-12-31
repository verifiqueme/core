import pandas
from pathlib import Path

from keras.backend import clear_session

from jano import Config
from pales.util import pales_index


class KerasController(object):

    def keras_model(self, force=False):
        """
        Método para retornar um modelo iterativo do Keras. Se um modelo já existir, carregará os pesos e retornará um objeto
        de modelo iterativo. Caso não exista um modelo, um será gerado.
        :param force: se deve ou não forçar a geração de um modelo fresco
        :return: modelo iterativo do keras
        """
        from keras import Sequential
        from keras.layers import Dense
        MODULE_PATH = pales_index()
        HEADERS = Config.values()['headers']
        model_path = MODULE_PATH + "/data/model.data"
        weights_path = MODULE_PATH + "/data/weights.h5"
        if Path(model_path).is_file() and force is False:
            from keras.models import model_from_json
            clear_session()
            loaded_model = model_from_json(open(model_path, 'r').read())
            loaded_model.load_weights(weights_path)
            loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
            return loaded_model
        else:
            clear_session()
            dataset = pandas.read_csv(MODULE_PATH + "/data/dataset.csv", names=HEADERS)
            # Separar dados de validação, e dados de treino
            array = dataset.values
            # Dados
            X = array[:, 0:(len(HEADERS) - 1)]  # Dados
            Y = array[:, (len(HEADERS) - 1)]  # Resultados
            model = Sequential()
            model.add(Dense(52, input_dim=(len(HEADERS) - 1), activation='relu'))
            model.add(Dense(29, activation='relu'))
            model.add(Dense(17, activation='relu'))
            model.add(Dense(5, activation='relu'))
            model.add(Dense(2, activation='relu'))
            model.add(Dense(1, activation='sigmoid'))
            # Compile model
            model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
            return model
