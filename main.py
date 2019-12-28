# import libraries
import csv
from datetime import datetime

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from bs4 import BeautifulSoup

# this is the url to target
target_page_carFax = ['https://www.carfax.com/vehicle/4S3GTAK65H3723107', 'https://www.carfax.com/vehicle/4S3GKAM62K3616300']




def scrape_The_Data(inputWebsite):
    scrapedData = []
    for item in inputWebsite:
        # querying of the target website and return the html to the variable 'page'
        page = urllib2.urlopen(item)

        # parses the html using beautiful soup and stores it
        soup = BeautifulSoup(page, 'html.parser')

        # dive into the tags to find the name
        nameCar = soup.find('div', attrs={'class': 'vehicle-title-container'}).find('h1').text.strip()
        print("name of car" + nameCar)

        scrapedData.append((nameCar))

def add_To_CSVFile():
    # toDo: change which row add to
    with open('./carEvalsAutomated.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)

        for nameCar in scrapedData:
            writer.writerow([nameCar, datetime.now()])



scrape_The_Data(target_page_carFax)
add_To_CSVFile()
