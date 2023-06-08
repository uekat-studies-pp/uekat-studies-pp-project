from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re

class Data:
    def __init__(self, url, title, price, priceAfterDiscount = 0) -> None:
        self.url = url
        self.title = title
        self.price = price
        self.priceAfterDiscount = priceAfterDiscount

class Scrapper:
    def __init__(self) -> None:
        self.data = []
        self.domain = ""
        self.listUrl = ""
    
    def getData(self) -> list:
        return self.data

    def run(self) -> None:
        pass

class SteamScrapper(Scrapper):
    def __init__(self) -> None:
        Scrapper.__init__(self)
        self.domain = "store.steampowered.com"
        self.listUrl = self.prepareListUrl()

    def run(self) -> None:
        session = HTMLSession()
        
        start = 0
        listUrl = self.prepareListUrl(start)
        while(listUrl):
            r = session.get(listUrl)
            json = r.json()

            soup = BeautifulSoup(json['results_html'], "html.parser")
            for element in soup.find('a'):
                url = element.attrs['href'] 
                title = element.find('.title')[0].text

                priceAfterDiscount = None
                price = element.find('.search_price')[0]
                if "discounted" in price.attrs['class']:
                    priceAfterDiscount = price.find('strike')[0].text

                    soup = BeautifulSoup(price.html, "html.parser")
                    br = soup.find('br')
                    price = br.next_sibling.strip()
                else:
                    price = price.text

                if (price.lower() == 'free to play'):
                    price = 0

                # remove "zł" and change to float
                trim = re.compile(r'[^\d.,]+')
                price = float(trim.sub('', price).replace(',', '.')) if price and price != 0 else 0
                priceAfterDiscount = float(trim.sub('', priceAfterDiscount).replace(',', '.')) if priceAfterDiscount else None

                # print(url, title, price, priceAfterDiscount)

                self.data.append(
                    Data(
                        url=url,
                        title=title,
                        price=price,
                        priceAfterDiscount=priceAfterDiscount
                    )
                )

            start = start + 100
            listUrl = self.prepareListUrl(start)

    def prepareListUrl(self, start = 0, count = 100) -> str:
        return "https://store.steampowered.com/search/results/?query&start={}&count={}&infinite=1".format(start, count)

class GogScrapper(Scrapper):
    def __init__(self) -> None:
        Scrapper.__init__(self)
        self.domain = "gog.com"
        self.listUrl = "https://www.gog.com/games"

    def run(self) -> None:
        pass

class App:
    def __init__(self) -> None:
        self.scrappers = {
            'steam': SteamScrapper(),
            'gog': GogScrapper(),
        }

    def run(self) -> None:
        try:
            data = {}

            for key, scrapper in self.scrappers.items():
                scrapper.run()
                data[key] = scrapper.getData()

            print(data)

        except Exception as error:
            print("An exception occurred:", error)

    def runSteam(self) -> None:
        pass

    def runGog(self) -> None:
        pass

if __name__ == "__main__":
    app = App()
    app.run()
