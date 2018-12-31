import os
from pathlib import Path

import pandas
from keras.backend import clear_session

from jano import Config
from pales.util import pales_index


class KerasController(object):
    def __init__(self):
        self.MODULE_PATH = pales_index()
        self.HEADERS = Config.values()['headers']
        dataset = pandas.read_csv(os.path.join(self.MODULE_PATH, "/data/dataset.csv"), names=self.HEADERS)
        array = dataset.values
        self.X = array[:, 0:(len(self.HEADERS) - 1)]
        self.Y = array[:, (len(self.HEADERS) - 1)]

    def evaluate(self, keras_model):
        scores = keras_model.evaluate(self.X, self.Y)
        return "%s: %.2f%%" % (keras_model.metrics_names[1], scores[1] * 100)

    def keras_model(self, force=False, verbose=False):
        """
        Método para retornar um modelo iterativo do Keras. Se um modelo já existir, carregará os pesos e retornará um objeto
        de modelo iterativo. Caso não exista um modelo, um será gerado.
        :param verbose: quando o verbose estiver ligado durante a criação de um modelo, mostrará a precisão do mesmo
        :param force: se deve ou não forçar a geração de um modelo fresco
        :return: modelo iterativo do keras
        """
        from keras import Sequential
        from keras.layers import Dense
        model_path = self.MODULE_PATH + "/data/model.data"
        weights_path = self.MODULE_PATH + "/data/weights.h5"
        if Path(model_path).is_file() and force is False:
            from keras.models import model_from_json
            clear_session()
            loaded_model = model_from_json(open(model_path, 'r').read())
            loaded_model.load_weights(weights_path)
            loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
            return loaded_model
        else:
            clear_session()
            model = Sequential()
            model.add(Dense(51, input_dim=(len(self.HEADERS) - 1), activation='relu'))
            model.add(Dense(30, activation='relu'))
            model.add(Dense(1, activation='sigmoid'))
            # Compile model
            model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
            model_json = model.to_json()
            model.fit(self.X, self.Y, epochs=150, batch_size=20, verbose=0, shuffle=True)
            if verbose:
                print(self.evaluate(model))
            with open(model_path, "w") as json_file:
                json_file.write(model_json)
            model.save_weights(weights_path)
            return model
