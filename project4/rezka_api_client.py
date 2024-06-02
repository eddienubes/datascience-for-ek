from HdRezkaApi import *


class RezkaApiClient:
    def __init__(self):
        self.rezka = HdRezkaApi('https://rezka.ag/series/thriller/646-vo-vse-tyazhkie-2008.html')

    def get_stream(self):
        def progress(current, all):
            percent = round(current * 100 / all)
            print(f"{percent}%: {current}/{all}", end="\r")

        return self.rezka.getStream('1', '1', translation='Оригинал (+субтитры)')('360p')
