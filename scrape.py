import re
from bs4 import BeautifulSoup
from requests import get

class Scraper:
    def __init__(self, url):
        '''
        Webscrapper to scraping phone number to company which link to webpage user gives
        :param url: are a link to company website
        '''

        self.url = url
        if not self.url.startswith(("http")):
            try:
                self.url = f'https://{url}'
            except:
                self.url = f'http://{url}'
    
    def scrape_main_page(self):

        '''
        The function looks for phone numbers on the home page provided by the user.
        :return numbers: list with numbers found in website
        '''

        page = get(self.url)
        bs = BeautifulSoup(page.content, "html.parser")
        numbers = (re.findall(r"[+][\d )(-]{3,20}|[\d )(-]{3,20}",bs.text))
        numbers = [num.strip() for num in numbers if len(num.strip()) > 9 and not num.startswith((')', '(', ' ', '-'))]

        return numbers


    def scrape_subpages(self):

        '''
        Function looks for phone numbers on subpages, which name is mentioned in the list ['kontakt', 'o firmie', 'o nas', 'wizytówka'].\
        :return numbers: list with numbers found in website
        '''

        page = get(self.url)
        bs = BeautifulSoup(page.content, "html.parser")
        kontakt = bs.find_all('a')
        subsection_list = ['kontakt', 'o firmie', 'o nas', 'wizytówka']
        lista_podstron = list(set([element['href'] for element in kontakt if str(element.get_text()).lower() in subsection_list]))
        for element in lista_podstron:
            if element.startswith(('http', 'https')):
                url2 = element
            else:
                url2 = f"{self.url}{element}"
            page = get(url2)
            bs = BeautifulSoup(page.content, "html.parser")
            numbers = (re.findall(r"[+][\d )(-]{3,20}|[\d )(-]{3,20}",bs.text))
            numbers = [num.strip() for num in numbers if len(num.strip()) > 9 and not num.startswith((')', '(', ' ', '-'))]
        return numbers

def main():
    url = input("")
    scraper = Scraper(url)
    try:
        numbers = scraper.scrape_main_page()
        if len(scraper.scrape_main_page()) == 0:
            try:
                numbers = scraper.scrape_subpages()
            except:
                print("Cannot be connected")

            if len(numbers) == 0:
                print("The number was not found on the website.")
            else:
                print (', '.join(map(str, set(numbers))))
        else:
            print (', '.join(map(str, set(numbers))))
    except:
        print("Unable to connect to page.")

if __name__ == "__main__":
    main()




