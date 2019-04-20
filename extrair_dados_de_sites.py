import click
import newspaper

from carmenta import score
from jano import Config


@click.command()
@click.option("--url", prompt="Site a ser analisado",
              help="O site a ser analisado")
def hello(url):
    search = newspaper.build(url, language="pt", memoize_articles=False, timeout=15)
    articles = list(reversed(search.articles))
    print(len(articles))
    for article in search.articles:
        try:
            print(article.url)
            results = translate_to_keras(article.url) + [1]
            with open("test.txt", "a") as myfile:
                myfile.write(str(results) + "\n")
                myfile.close()
            with open("originals.txt", "a") as myfile:
                myfile.write(str(article.url) + "\n")
                myfile.close()
            print("thank you next")
        except Exception as e:
            print(e.__str__())
            pass


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
    return [v for k, v in info.items()]


if __name__ == '__main__':
    hello()
