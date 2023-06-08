from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import psycopg2
import os


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
                    title = element.find(class_="title").text

                    priceAfterDiscount = None
                    price = element.find(class_='search_price')
                    if "discounted" in price.attrs['class'] and price.find('strike'):
                        priceAfterDiscount = price.find('strike').text

                        br = price.find('br')
                        price = br.next_sibling.strip()
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

                    # print(url, title, price, priceAfterDiscount)

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

    def prepareListUrl(self, start=0, count=100) -> str:
        return "https://store.steampowered.com/search/results/?query&start={}&count={}&infinite=1".format(start, count)


class GogScraper(Scraper):
    def __init__(self, db: Database) -> None:
        Scraper.__init__(self, db)
        self.domain = "gog.com"
        self.listUrl = "https://www.gog.com/games"

    def run(self) -> None:
        pass


class App:
    def __init__(self) -> None:
        self.db = PostgresAdapter()
        self.scrapers = {
            'steam': SteamScraper(self.db),
            'gog': GogScraper(self.db),
        }

    def run(self) -> None:
        try:
            for key, scraper in self.scrapers.items():
                scraper.run()
        except Exception as error:
            print("An exception occurred:", error)

    def runSteam(self) -> None:
        pass

    def runGog(self) -> None:
        pass


if __name__ == "__main__":
    app = App()
    app.run()
