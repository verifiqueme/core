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
        dataset_path = os.path.normpath(pales_index() + os.path.normcase("/data/dataset.csv"))
        dataset = pandas.read_csv(dataset_path, names=self.HEADERS)
        array = dataset.values
        self.X = array[:, 0:(len(self.HEADERS) - 1)]
        self.Y = array[:, (len(self.HEADERS) - 1)]
        self.validation_size = 0.20

    def evaluate(self, keras_model, evaluate_x=None, evaluate_y=None):
        if evaluate_x is None:
            evaluate_x = self.X
        if evaluate_y is None:
            evaluate_y = self.Y
        scores = keras_model.evaluate(evaluate_x, evaluate_y)
        return "%s: %.2f%%" % (keras_model.metrics_names[1], scores[1] * 100)

    def keras_model(self, force=False, verbose=False, final=False):
        """
        Método para retornar um modelo iterativo do Keras. Se um modelo já existir, carregará os pesos e retornará um objeto
        de modelo iterativo. Caso não exista um modelo, um será gerado.
        :param final: Se deve utilizar todos os dados (True) do dataset ou dividi-lo (False)
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
            model.add(Dense(30, input_dim=(len(self.HEADERS) - 1), activation='relu'))
            model.add(Dense(51, activation='relu'))
            model.add(Dense(36, activation='relu'))
            model.add(Dense(10, activation='relu'))
            model.add(Dense(1, activation='sigmoid'))
            # Compile model
            model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
            model_json = model.to_json()
            from sklearn import model_selection
            X_train, X_validation, Y_train, Y_validation = \
                model_selection.train_test_split(self.X, self.Y, test_size=self.validation_size)
            if not final:
                model.fit(X_train, Y_train, epochs=150, batch_size=20, verbose=0, shuffle=True)
            else:
                model.fit(self.X, self.Y, epochs=150, batch_size=20, verbose=0, shuffle=True)
            if verbose:
                if not final:
                    print(self.evaluate(model, evaluate_x=X_validation, evaluate_y=Y_validation))
                else:
                    print(self.evaluate(model, evaluate_x=self.X, evaluate_y=self.Y))
            with open(model_path, "w") as json_file:
                json_file.write(model_json)
            model.save_weights(weights_path)
            return model
