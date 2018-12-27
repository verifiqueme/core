class Config(object):

    @staticmethod
    def values():
        settings = {
            'max_list': 20,
            'country': "BR",
            'language': "pt-BR",
            'replacement_charset': "latin1",
            'max_words_precision': 20,
            'timezone': "America/Sao_Paulo"
        }
        return settings
