import sys
from requests_html import HTMLSession
from bs4 import BeautifulSoup, PageElement, ResultSet
import re
import psycopg2
import os
from urllib.parse import urlparse, urlunparse


class Data:
    def __init__(self, type, url, title, price, priceAfterDiscount=0) -> None:
        self.type = type
        self.url = url
        self.title = title
        self.price = price
        self.priceAfterDiscount = priceAfterDiscount


class Database:
    def __init__(self) -> None:
        pass

    def save(self, data: Data) -> None:
        pass

    def remove(self, data: Data) -> None:
        pass


class PostgresAdapter(Database):
    def __init__(self) -> None:
        Database.__init__(self)
        self.con = psycopg2.connect(
            database=os.getenv('POSTGRES_DB'), user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASSWORD'), host=os.getenv('POSTGRES_HOST'), port=os.getenv('POSTGRES_PORT'))
        self.cur = self.con.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS public.data(id SERIAL, type VARCHAR(255), url VARCHAR(255) NOT NULL, title VARCHAR(255) NOT NULL, price FLOAT NOT NULL, priceAfterDiscount FLOAT, created_at TIMESTAMP DEFAULT NOW(), modified_at TIMESTAMP DEFAULT NOW())")
        self.con.commit()

    def save(self, data: Data) -> None:
        self.cur.execute(
            "SELECT url FROM public.data WHERE url='{0}'".format(data.url))
        if (self.cur.fetchone() is None):
            self.cur.execute("INSERT INTO public.data (type, url, title, price, priceAfterDiscount) VALUES(%s, %s, %s, %s, %s)",
                             (data.type, data.url, data.title, data.price, data.priceAfterDiscount))
        else:
            self.cur.execute("UPDATE public.data SET type='{0}', title='{1}', price={2}, priceAfterDiscount={3}, modified_at='NOW()' WHERE url='{4}'".format(
                data.type, data.title.replace("'", "''"), data.price, data.priceAfterDiscount if data.priceAfterDiscount else 'NULL', data.url))

        self.con.commit()

    def remove(self, data: Data) -> None:
        self.cur.execute(
            "DELETE FROM public.data WHERE url='{0}'".format(data.url))
        self.con.commit()


class SqliteAdapter(Database):
    def __init__(self) -> None:
        Database.__init__(self)

        # self.con = sqlite3.connect("main.db")
        # self.cur = self.con.cursor()
        # self.cur.execute(
        #     "CREATE TABLE IF NOT EXISTS data(url, title, price, priceAfterDiscount)")

    def save(self, data: Data) -> None:
        # res = self.cur.execute(
        #     "SELECT url FROM data WHERE url='{0}'".format(data.url))
        # if (res.fetchone() is None):
        #     self.cur.execute("INSERT INTO data VALUES(?, ?, ?, ?)",
        #                      (data.url, data.title, data.price, data.priceAfterDiscount))
        # else:
        #     print(1)
        #     self.cur.execute("UPDATE data SET title='{0}', price={1}, priceAfterDiscount={2} WHERE url='{3}'".format(
        #         data.title, data.price, data.priceAfterDiscount, data.url))
        pass

    def remove(self, data: Data) -> None:
        # self.cur.execute("DELETE FROM data WHERE url='{0}'".format(data.url))
        pass


class Scraper:
    def __init__(self, db) -> None:
        self.db = db
        self.data = []
        self.domain = ""
        self.listUrl = ""

    def getData(self) -> list:
        return self.data

    def run(self) -> None:
        pass


class SteamScraper(Scraper):
    def __init__(self, db: Database) -> None:
        Scraper.__init__(self, db)
        self.domain = "store.steampowered.com"
        self.listUrl = self.prepareListUrl()

    def run(self) -> None:
        print("Running Steam scraper...", file=sys.stderr)
        session = HTMLSession()

        start = 0
        listUrl = self.prepareListUrl(start)
        while (listUrl):
            r = session.get(listUrl)
            json = r.json()

            soup = BeautifulSoup(json['results_html'], "html.parser")
            for element in soup.find_all('a'):
                try:
                    url = element.attrs['href']
                    url = self.prepareElementUrl(url)
                    title = element.find(class_="title").text

                    priceAfterDiscount = None
                    price = element.find(class_='search_price')
                    if "discounted" in price.attrs['class'] and price.find('strike'):
                        br = price.find('br')
                        priceAfterDiscount = br.next_sibling.strip()

                        price = price.find('strike').text
                    else:
                        price = price.text.strip()

                    if (price.lower() in ['free to play', 'free', 'play for free!', 'play the demo']):
                        price = 0

                    # remove "zł" and change to float
                    trim = re.compile(r'[^\d.,]+')
                    price = float(trim.sub('', price).replace(
                        ',', '.')) if price and price != 0 else 0
                    priceAfterDiscount = float(trim.sub('', priceAfterDiscount).replace(
                        ',', '.')) if priceAfterDiscount else None

                    data = Data(
                        type='steam',
                        url=url,
                        title=title,
                        price=price,
                        priceAfterDiscount=priceAfterDiscount
                    )

                    self.data.append(data)
                    self.db.save(data)
                except:
                    pass

            start = start + 100
            listUrl = self.prepareListUrl(start)
        print("Steam scraper run finished.", file=sys.stderr)

    def prepareListUrl(self, start=0, count=100) -> str:
        return "https://store.steampowered.com/search/results/?query&start={}&count={}&infinite=1".format(start, count)

    def prepareElementUrl(self, url: str) -> str:
        parsed_url = urlparse(url)
        query_params = parsed_url.query.split("&")
        query_params = [param for param in query_params if not param.startswith("snr=")]
        new_query = "&".join(query_params)
        return urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query, parsed_url.fragment))




class GogScraper(Scraper):
    def __init__(self, db: Database) -> None:
        Scraper.__init__(self, db)
        self.domain = "gog.com"
        self.listUrl = "https://www.gog.com/pl/games"

    def prepareListUrl(self, page: int) -> str:
        if page == 1:
            return self.listUrl
        else:
            return "{}?page={}".format(self.listUrl, page)
        
    def extractData(self, soup: BeautifulSoup) -> list[Data]:
        output = []
        gameTiles: ResultSet[PageElement] = soup.find_all("a", {
        "selenium-id": "productTile"
        })
        
        for tile in gameTiles:
            try:
                url = tile.attrs["href"]
                title = tile.find("div", {
                    "class": "product-tile__title"
                }, recursive = True).attrs["title"]
                trim = re.compile(r'[^\d.,]+')
                baseValue = None
                finalValue = None
                isFree = False
                baseValueElement = tile.find("span", {
                    "class": "base-value"
                }, recursive = True)
                if baseValueElement is not None:
                    text = str(baseValueElement.string)
                    baseValue = float(trim.sub('', text).replace(',', '.'))
                finalValueElement = tile.find("span", {
                    "class": "final-value"
                }, recursive = True)
                if baseValueElement is not None:
                    finalValueText = str(finalValueElement.string)
                    finalValue = float(trim.sub('', finalValueText).replace(',', '.'))
                isFree = tile.find("span", {
                    "selenium-id": "productPriceFreeLabel"
                }, recursive = True) is not None
                price: float = 0
                priceAfterDiscount: float | None = None
                if isFree:
                    price = 0
                elif baseValue is not None:
                    priceAfterDiscount = finalValue
                    price = baseValue
                elif finalValue is not None:
                    price = finalValue
                else:
                    price = 0
                data = Data(
                    type="gog",
                    url=url,
                    title=title,
                    price=price,
                    priceAfterDiscount=priceAfterDiscount
                )
                output.append(data)
            except:
                pass
        return output

    def run(self) -> None:
        print("Running GOG scraper...", file=sys.stderr)
        page = 1
        pageNumber = 0
        session = HTMLSession()
        print("Downloading first page...", file=sys.stderr)
        r = session.get(self.prepareListUrl(page))
        print("Downloaded page 1.", file=sys.stderr)
        responseText = r.text
        try:
            soup = BeautifulSoup(responseText, "html.parser")
            # Extract the amount of pages to go
            pageNumbers: ResultSet[PageElement] = soup.find_all("button", {
                "selenium-id": "paginationPage"
            })
            lastPageNumber = pageNumbers[-1]
            innerText = lastPageNumber.contents[0]
            pageNumber = int(str(innerText.string))
            print(f"There are {pageNumber} pages of games to scrape", file=sys.stderr)
            games = self.extractData(soup)
            print(f"Found {len(games)} games", file=sys.stderr)
            for game in games:
                self.db.save(game)
            page += 1
        except:
            print("Could not parse HTML.", file=sys.stderr)
        
        while (page <= pageNumber):
            try:
                print(f"Getting page {page}...", file=sys.stderr)
                r = session.get(self.prepareListUrl(page))
            except:
                print(f"Could not get page {page}", file=sys.stderr)
                break
            try:
                print(f"Parsing page {page}...", file=sys.stderr)
                soup = BeautifulSoup(r.text, "html.parser")
                print(f"Parsed page {page}.", file=sys.stderr)
                games = self.extractData(soup)
                print(f"Found {len(games)} games", file=sys.stderr)
            except:
                print(f"Could not parse page {page}", file=sys.stderr)
                break
            try:
                for game in games:
                    self.db.save(game)
                page += 1
            except Exception as error:
                print(f"Could not save games from page {page} to DB", file=sys.stderr)
                print(f"Underlying error: {error}", file=sys.stderr)
                break
                
            
        print("GOG scraper run finished.", file=sys.stderr)


class App:
    def __init__(self) -> None:
        self.db = PostgresAdapter()
        self.scrapers = [
            SteamScraper(self.db),
            GogScraper(self.db),
        ]

    def run(self) -> None:
        print("Running scrapers...", file=sys.stderr)
        try:
            for scraper in self.scrapers:
                scraper.run()
        except Exception as error:
            print("An exception occurred:", error, file=sys.stderr)
        print("Scraper run finished.", file=sys.stderr)


if __name__ == "__main__":
    app = App()
    app.run()
