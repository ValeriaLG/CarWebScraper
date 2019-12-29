# import libraries
import csv
from datetime import datetime

from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
from apiclient.http import MediaFileUpload

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from bs4 import BeautifulSoup



def upload_To_Google():
    creds = ServiceAccountCredentials.from_json_keyfile_name('GOOGLE_APPLICATION_CREDENTIALS', ['https://www.googleapis.com/auth/drive.file'])
    drive_api = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': 'carEvalsAutomated.csv', 'mimeType': 'application/vdn.google-apps.spreadsheet'}
    media = MediaFileUpload('carEvalsAutomated.csv', mimetype= 'text/csv', resumable=True)
    something = drive_api.files().create(body=file_metadata, media_body=media).execute()

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
    return scrapedData

def add_To_CSVFile(scrapedData):
    # toDo: change which row add to
    with open('./carEvalsAutomated.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)

        for nameCar in scrapedData:
            writer.writerow([nameCar, datetime.now()])



# this is the url to target
target_page_carFax = ['https://www.carfax.com/vehicle/4S3GTAK65H3723107', 'https://www.carfax.com/vehicle/4S3GKAM62K3616300']



add_To_CSVFile(scrape_The_Data(target_page_carFax))

#uncomment when want to upload to google
#upload_To_Google()
