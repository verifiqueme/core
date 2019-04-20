import click
import newspaper

from pales.controllers.BuilderController import translate_to_keras

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
            results = translate_to_keras(article.url)[0]
            results.append(1)
            with open("test.txt", "a") as myfile:
                myfile.write(str(results) + "\n")
                myfile.close()
            with open("originals.txt", "a") as myfile:
                myfile.write(str(article.url) + "\n")
                myfile.close()
            print("thank you next")
        except Exception:
            pass


if __name__ == '__main__':
    hello()