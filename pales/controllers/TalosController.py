import os
from pathlib import Path

import pandas
import talos as ta
from keras import Sequential
from keras.backend import binary_crossentropy, elu, relu, sigmoid, clear_session
from keras.layers import Dropout, Dense
from keras.optimizers import Adam, Nadam
from talos.model import hidden_layers, lr_normalizer

from jano import Config
from pales.util import pales_index


class TalosController(object):
    def __init__(self):
        self.MODULE_PATH = pales_index()
        self.HEADERS = Config.values()['headers']
        dataset_path = os.path.normpath(pales_index() + os.path.normcase("/data/dataset.csv"))
        dataset = pandas.read_csv(dataset_path, names=self.HEADERS)
        array = dataset.values
        self.X = array[:, 0:(len(self.HEADERS) - 1)]
        self.Y = array[:, (len(self.HEADERS) - 1)]
        self.p = {'lr': (0.5, 5, 8),
                  'first_neuron': [8, 16, 32, 64],
                  'hidden_layers': [2, 3, 4, 5],
                  'batch_size': (1, 5, 5),
                  'epochs': [50, 100, 150],
                  'dropout': (0, 0.2, 0.5),
                  'weight_regulizer': [None],
                  'emb_output_dims': [None],
                  'shape': ['brick', 'long_funnel'],
                  'kernel_initializer': ['uniform', 'normal'],
                  'optimizer': [Adam, Nadam],
                  'losses': [binary_crossentropy],
                  'activation': [relu, elu],
                  'last_activation': [sigmoid]}

    def fake_news_model(self, x_train, y_train, x_val, y_val, params):
        model = Sequential()
        model.add(Dense(10, input_dim=(len(self.HEADERS) - 1),
                        activation=params['activation'],
                        kernel_initializer='normal'))

        model.add(Dropout(params['dropout']))

        hidden_layers(model, params, 1)

        model.add(Dense(1, activation=params['last_activation'],
                        kernel_initializer='normal'))

        model.compile(loss=params['losses'],
                      optimizer=params['optimizer'](lr=lr_normalizer(params['lr'], params['optimizer'])),
                      metrics=['acc'])

        history = model.fit(x_train, y_train,
                            validation_data=[x_val, y_val],
                            batch_size=params['batch_size'],
                            epochs=params['epochs'],
                            verbose=0)

        return history, model

    def talos_model(self, force=False):
        """
        Método para retornar um modelo iterativo do Talos. Se um modelo já existir, carregará os pesos e retornará um objeto
        de modelo iterativo. Caso não exista um modelo, um será gerado.
        :param force: se deve ou não forçar a geração de um modelo fresco
        :return: modelo iterativo do talos
        """
        model_path = self.MODULE_PATH + "/data/talos/fakedata.zip"
        if Path(model_path).is_file() and force is False:
            clear_session()
            return ta.Restore(model_path)
        else:
            clear_session()
            t = ta.Scan(x=self.X,
                        y=self.Y,
                        model=self.fake_news_model,
                        grid_downsample=.01,
                        params=self.p,
                        dataset_name='fakenews',
                        experiment_no='1')
            ta.Deploy(t, str(model_path).replace(".zip", ""))
            return t
