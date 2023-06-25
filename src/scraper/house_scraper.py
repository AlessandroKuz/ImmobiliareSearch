import pandas as pd
import requests
import bs4


class HouseFeaturesScraper:
    """Class that allow you to scrape the features of a given house
    from the Immobiliare.it website - renting section;
    gets title, price, square meters, rooms, bathrooms, energy class,
    address and link to the house, and returns the data as a pandas.Series"""
    def __init__(self, url) -> None:
        self.url = url
        self.soup = self.get_soup()

        self.house_traits = {}
        self.price = {}
        
    def get_soup(self) -> bs4.BeautifulSoup:
        """Returns the soup of the given url"""
        response = requests.get(self.url)
        self.soup = bs4.BeautifulSoup(response.text, 'lxml')

        return self.soup
    
    def get_title(self) -> dict:
        """Returns the title of the house"""
        self.title = self.soup.find("h1", class_="in-titleBlock__title").text

        return {"title": self.title}
    
    def get_location(self) -> dict:
        """Returns the location of the house"""
        location_list = self.soup.find_all("span", class_="in-location")
        location = [location.text for location in location_list]
        self.location = {"city": location[0], "area": location[1], "street": location[2]} \
                        if len(location) == 3 else {"city": location[0], "area": pd.NA, "street": location[1]}

        return self.location

    def get_description(self) -> dict:
        self.description = self.soup.find("div", class_="in-readAll").text

        return {"descrizione": self.description}

    def get_house_traits(self) -> dict:
        """Returns the traits of the house"""
        dl_lists = self.soup.find_all("dl", class_="in-realEstateFeatures__list")  # return three objects "Caratteristiche", "Costi", "Efficienza Energetica"
        
        interested_descriptions = ["contratto", "tipologia", "superficie",
                                "locali", "bagni", "piano", "disponibilità",
                                "prezzo", "spese condominio", "cauzione",
                                "anno costruzione", "stato", "riscaldamento",
                                "climatizzatore", "efficienza energetica"]
        
        price_descriptions = ["prezzo", "spese condominio", "cauzione"]
        
        for dl_list in dl_lists:
            terms = dl_list.find_all("dt")
            descriptions = dl_list.find_all("dd")
        
            for term, description in zip(terms, descriptions):
                if term.text.lower() in interested_descriptions:
                    self.house_traits[term.text.lower()] = description.text
                elif term.text.lower() in price_descriptions:
                    self.price[term.text.lower()] = description.text

        return self.house_traits
    
    def get_price(self) -> dict:
        """Returns the price of the house"""
        #TODO: REVISE the func to get all the prices (affitto, )
        if not self.price:
            self.get_house_traits()

        return self.price    

    def to_Series(self) -> pd.Series:
        """Returns the house features as a pandas.Series"""
        title = self.get_title()
        location = self.get_location()
        description = self.get_description()
        characteristics = self.get_house_traits()
        price = self.get_price()

        features = [
            title,
            price,
            location,
            description,
            characteristics
            ]
        series = pd.Series()
        for feature in features:
            for key, val in feature.items():
                series[key] = val
        
        return series
