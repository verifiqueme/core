<img src="https://cdn.jsdelivr.net/gh/verifiqueme/web@master/src/assets/icon.png" width="123px" alt="verifica.me" align="right">

# Núcleo

![License](https://img.shields.io/github/license/verifiqueme/core.svg)

Verifique.me é um protótipo de automatização de checagem de notícias pela internet.

Componentes
=====

O núcleo consiste de múltiplos componentes (módulos), cada componente é responsável por um tipo de processamento no núcleo:

* Jano: Módulo responsável por extrair e converter artigos/sites em um modelo compatível e simplificado.
* Carmenta: Módulo responsável exclusivamente para análise de texto, comparação/avaliação de relativos, e processamento de linguagem natural.
* Pales: Módulo responsável por organizar e controlar a rede neural usando o Talos/Keras

***

Instalando
=====

Depende de:
* [Python 3](https://www.python.org/downloads/) (3+)
* [Pipenv](https://github.com/pypa/pipenv) (11.8+)
* [ICU4C](http://site.icu-project.org/download) (61.1+)

### Windows
* [PyICU](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu) (Pré-Compilado para o Python utilizado)
* [pycld2](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycld2) (Pré-Compilado para o Python utilizado)

É possível que a instalação acima falhe e você deve instalar os Wheels do `PyICU` e `pycld2` e deve-se instala-los manualmente usando como exemplo:
```sh
pipenv install ./PyICU.whl
```

### Instalando dependências
Instale as dependências do pipenv e inicie o ambiente virtual:
```sh
pipenv install
pipenv shell
```

> É necessário definir a variável de ambiente `MS_BING_KEY` com uma chave de busca gerada nos [Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/) e `ICU_VERSION` com base na versão do ICU que você utiliza