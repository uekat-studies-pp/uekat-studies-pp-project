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
        pass

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

        except:
            print("An exception occurred")

    def runSteam(self) -> None:
        pass

    def runGog(self) -> None:
        pass

if __name__ == "__main__":
    app = App()
    app.run()
