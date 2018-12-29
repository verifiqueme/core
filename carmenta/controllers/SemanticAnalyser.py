from polyglot.downloader import downloader


class SemanticAnalyser(object):
    @staticmethod
    def check_packages():
        packages = ["embeddings2.pt", "pos2.pt", "ner2.pt", "sentiment2.pt"]
        for package in packages:
            if not downloader.is_installed(package):
                print("Baixando {0}".format(package))
                downloader.download(package)
        return True
