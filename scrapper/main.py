from requests_html import HTMLSession
from bs4 import BeautifulSoup

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
        self.listUrl = "https://store.steampowered.com/search"

    def run(self) -> None:
        session = HTMLSession()
        r = session.get(self.listUrl)

        for element in r.html.find('#search_resultsRows a'):
            url = element.attrs['href'] 
            title = element.find('.title').text

            priceAfterDiscount = None
            price = element.find('.search_price')[0]
            if "discounted" in price.attrs['class']:
                priceAfterDiscount = price.find('strike')[0].text

                soup = BeautifulSoup(price.html, "html.parser")
                br = soup.find('br')
                price = br.next_sibling.strip()
            else:
                price = price.text

            self.data.append(
                Data(
                    url=url,
                    title=title,
                    price=price,
                    priceAfterDiscount=priceAfterDiscount
                )
            )
        
        print(self.data)

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
