from bs4 import BeautifulSoup
import requests
import json

# TODO: da aggiungere un parametro che si salva i metri quadri delle case

class RentingHouseParser:
    """Given a url of a specific rented house on Immobiliare.it,
    parses the site to get the title, description and features;
    also returns an optional .txt file for the description and
    a .json file for the features"""
    def __init__(self, url: str) -> None:
        self.__url: str = url
        self.__soup = None
        self.__title: str = None
        self.__soup_error: str = "You need to define the soup first!\n\
        Please run the start_html first."


    def start_html(self) -> None:
        response: str = requests.get(self.__url).text
        self.__soup = BeautifulSoup(response, "lxml")


    def get_title(self) -> str:
        if self.__soup:
            self.__title = self.__soup.find("h1",
                                             class_='in-titleBlock__title'
                                             ).text
            return self.__title
        else:
            print(self.__soup_error)


    def get_description(self, report_file: bool = False) -> str:
        if self.__soup:
            description = self.__soup.find("div", class_='in-readAll')
            descrizione: str = str(description)
            inizio: int = descrizione.find("<div>") + len("<div>")
            fine: int = descrizione.find("</div>")
            self.__description: str = descrizione[inizio:fine]
            self.__description = self.__description.replace("<hr/>","")
            self.__description = self.__description.replace("<hr>","")
            self.__description = self.__description.replace("<br/>", "\n")
            self.__description = self.__description.replace("<br>", "\n")

            if report_file:
                if not self.__title:
                    self.get_title()
                with open(f"{self.__title}.txt", "w") as f:
                    f.write(self.__description)

            return self.__description
        else:
            print(self.__soup_error)


    def get_features(self, json_file: bool = False) -> dict:
        if self.__soup:
            features = self.__soup.find_all("dl", 
                                        class_='in-realEstateFeatures__list')
            self.__features_dict: dict[str] = {}

            for index, elemento in enumerate(features):
                lista_temp1: list = []
                lista_temp2: list = []

                for key in elemento.find_all("dt"):                
                    lista_temp1.append(key.text)

                if index == 0:  # if span allora fai così, non come ho fatto ora
                    for value in elemento.find_all("dd")[:-1]:
                        lista_temp2.append(value.text)
                    x = elemento.find_all("dd")[-1]
                    other_features_list: list = []
                    for i in x.find_all("span"):
                        other_features_list.append(i.text)
                    lista_temp2.append((other_features_list))
                else:
                    for value in elemento.find_all("dd"):
                        lista_temp2.append(value.text)

                for key, value in zip(lista_temp1, lista_temp2):
                    self.__features_dict[key] = value

            if json_file:
                if not self.__title:
                    self.get_title()
                with open(f"{self.__title}.json", "w") as f:
                    json.dump(self.__features_dict, f, indent=2)

            return self.__features_dict
        else:
            print(self.__soup_error)


if __name__ == "__main__":
    def print_details(aparment):
        aparment.start_html()

        title = aparment.get_title()
        description = aparment.get_description()
        features = aparment.get_features()
        
        divider = "-"*100

        print(divider)   
        print(title)
        print(divider)
        print(description)
        print(divider)
        print(features)
    

    def print_houses(houses_list):
        for url in houses_list:
            house = RentingHouseParser(url)
            print_details(house)

            print("\n\n", "|"*100)


    lista_case = ["https://www.immobiliare.it/annunci/101281527/",
                  "https://www.immobiliare.it/annunci/101754409/",
                  "https://www.immobiliare.it/annunci/101631381/",
                  "https://www.immobiliare.it/annunci/100761695/",
                  "https://www.immobiliare.it/annunci/101321083/"
                  ]

    casa = RentingHouseParser(lista_case[0])
    casa.start_html()
    casa.get_features(True)