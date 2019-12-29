# import libraries
import csv
from datetime import datetime
import xlwt as worksheetMaker

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
    innerCarList = []
    columnHeaders = []
    overallList = []
    for item in inputWebsite:
        # querying of the target website and return the html to the variable 'page'
        page = urllib2.urlopen(item)

        # parses the html using beautiful soup and stores it
        soup = BeautifulSoup(page, 'html.parser')

        # dive into the tags to find the name
        nameCar = soup.find('div', attrs={'class': 'vehicle-title-container'}).find('h1').text.strip()

        innerCarList.append(nameCar)

        price = soup.find('div', attrs={'class': 'vehicle-info-details-price'}).text.strip()

        innerCarList.append(price)

        # get the details numbers
        detailsMeat = soup.select('div[class=vehicle-info-details]')

        # get the header titles
        detailsTitle = soup.find_all('div', class_= 'vehicle-info-details-title')

        # add the details to the list
        for item in detailsMeat:
            innerCarList.append(item.text)


        stockNumber = soup.find('div', attrs={'class': 'test-auto-stock'}).text.strip()
        innerCarList.append(stockNumber)


        innerCarList.append(str(datetime.now()))

        # adding the headers for each column
        if (len(columnHeaders) == 0):
            columnHeaders.append("Car Name")
            for item2 in detailsTitle:
                columnHeaders.append(item2.text)
            columnHeaders.append("Update Date")



        scrapedData.append((innerCarList))
        innerCarList = []

    overallList.append(columnHeaders)
    overallList.append(scrapedData)
    print(overallList)
    return (overallList)

def add_To_CSVFile(scrapedData):
    # toDo: change which row add to
    with open('./carEvalsAutomated.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)

        for nameCar in scrapedData:
            writer.writerow([nameCar, datetime.now()])


def add_to_WorkSheet(returnedData):
    mainStyle = worksheetMaker.easyxf('font: name Times New Roman, color-index black, bold off', num_format_str='#,##0.00')
    styleDate = worksheetMaker.easyxf(num_format_str='dd/mm/yyyy')
    headerBold = worksheetMaker.easyxf('font: name Times New Roman, color-index black, bold on')

    wb = worksheetMaker.Workbook()
    ws = wb.add_sheet('Car Evaluations')


    actualData = returnedData[1]
    headers = returnedData[0]

    for column in range(len(headers)):
        ws.write(0, column, headers[column], headerBold)

    for row in range(len(actualData)):
        for column in range(len(actualData[row])):
            ws.write(row + 1, column, actualData[row][column], mainStyle)



    wb.save('carEvalsAutomated.xls')



# this is the url to target
target_page_carFax = ['https://www.carfax.com/vehicle/4S3GTAK65H3723107', 'https://www.carfax.com/vehicle/4S3GKAM62K3616300']


returnedData = scrape_The_Data(target_page_carFax)
add_to_WorkSheet(returnedData)


# uncomment if csv file is desired
#add_To_CSVFile(returnedData)

#uncomment when want to upload to google
#upload_To_Google()
