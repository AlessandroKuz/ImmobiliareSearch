from bs4 import BeautifulSoup
import requests
import re
import timeit as t

from house_scraper import RentingHouseParser

# TODO: introdurre una parte che tiene conto dei filtri iniziali
# SE SOLO SU 1 PAG NON FUNZIONA
# if  re.compile("?\$=*")

def house_parsing(house_url: str, soup):
    houses = soup.find_all("a", class_="in-card__title")
    for house in houses:
        house_url = house["href"]
        house_to_parse = RentingHouseParser(house_url)
        house_to_parse.start_html()
        print(house_to_parse.get_title())


def main(url: str):
    IMMOBILIARE_URL: str = "https://www.immobiliare.it/"
    # ???????????
    # TODO: se contiene ?QUALCOSA=QUALCOSA allora aggiungi &pag anzicchè ?pag
    # TODO: add functionality to use filters: {
    # rilevanza: "?criterio=rilevanza",
    # prezzo: "?criterio=prezzo" + "&ordine=desc" oppure "&ordine=desc"
    # superficie: "?criterio=superficie" + "&ordine=desc" oppure "&ordine=desc"
    # locali: "?criterio=locali" + "&ordine=desc" oppure "&ordine=desc"
    # dataModifica: "?criterio=dataModifica" + "&ordine=desc" oppure "&ordine=desc"
    # }
    # pattern = re.compile("\$=*")
    # print(pattern.match(url))

    if not url.startswith(IMMOBILIARE_URL):
        print("Invalid Link or not of the immobiliare.it domain.")
    else:
        response: str = requests.get(url).text
        soup = BeautifulSoup(response, "lxml")
        pages_number = soup.find_all("div", class_="in-pagination__item hideOnMobile in-pagination__item--disabled")[-1].text
        # for i in range(1, int(pages_number) + 1):  # check su pagina inesistente?? || secondo me ridondante
        for i in range(1, int(pages_number) + 1):  # check su pagina inesistente?? || secondo me ridondante
            #if ESPRESSIONE REGEX:
            #new_url = f"{url}&pag={i}"
            #else:
            new_url = f"{url}?pag={i}"
            house_parsing(new_url, soup)


if __name__ == "__main__":
    print(t.timeit(main("https://www.immobiliare.it/affitto-case/torino/")))
    # main("https://www.immobiliare.it/affitto-case/sesto-san-giovanni/")
    # main("https://www.immobiliare.it/affitto-case/torino/")
# main("https://www.immobiliare.it/affitto-case/torino/?criterio=prezzo&ordine=asc&pag=2")
