import re
import unicodedata

from ftfy import fix_encoding

from jano.config import Config


def normalizeword(palavra: str) -> str:
    """
    Normaliza uma palavra individualmente (remove acento e caracteres especiais)
    :param palavra: palavra a ser normalizada
    :return: palavra normalizada
    """
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavra_sem_acento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    if not palavra.islower() and not palavra.isupper():
        return palavra
    else:
        return re.sub('[^a-zA-Z0-9 \\\]', '', palavra_sem_acento)


def normalize(texto: str) -> str:
    """
    Remove caracteres especiais e acentos da língua portuguesa
    :param texto: texto a ser normalizado
    :return: texto sem caracteres especiais ou acentos
    """
    retorno = ""
    for palavra in str(texto).rsplit(" "):
        retorno += normalizeword(palavra) + " "
    return str(retorno)


def fixcharset(string):
    """
    Tenta consertar uma string em relação a codificação do texto de múltiplas maneiras
    :param string: texto a ser consertado
    :return: texto consertado
    """
    text = fix_encoding(string)
    if "�" in text:
        text = text.encode(Config().values()['replacement_charset'], "ignore")
    return text


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]
