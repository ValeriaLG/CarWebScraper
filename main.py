# import libraries
import csv
from datetime import datetime
import xlwt as worksheetMaker
import sys

from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
from apiclient.http import MediaFileUpload

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from bs4 import BeautifulSoup


# Not Tested
def upload_To_Google():
    creds = ServiceAccountCredentials.from_json_keyfile_name('GOOGLE_APPLICATION_CREDENTIALS', ['https://www.googleapis.com/auth/drive.file'])
    drive_api = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': 'carEvalsAutomated.csv', 'mimeType': 'application/vdn.google-apps.spreadsheet'}
    media = MediaFileUpload('carEvalsAutomated.csv', mimetype= 'text/csv', resumable=True)
    something = drive_api.files().create(body=file_metadata, media_body=media).execute()

# some example urls... ['https://www.carfax.com/vehicle/4S3GTAK65H3723107', 'https://www.carfax.com/vehicle/4S3GKAM62K3616300']
def ask_Input():
    targetPages = []
    inputUser = ""
    print("Enter a url from a vehicle on the CarFax website only. \nEnter s to stop.\n")
    while inputUser != "s":
        inputUser = input()
        if (inputUser != "s"):
            targetPages.append(inputUser)

    if (len(targetPages) != 0):
        results = scrape_The_Data_carFax(targetPages)
    else:
        sys.exit()

    return results


def scrape_The_Data_carFax(inputWebsite):
    scrapedData = []
    innerCarList = []
    columnHeaders = []
    overallList = []
    for pageURL in inputWebsite:
        if "carfax" not in pageURL:
            continue
        # querying of the target website and return the html to the variable 'page'
        page = urllib2.urlopen(pageURL)

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
        innerCarList.append(str(pageURL))

        # adding the headers for each column
        if (len(columnHeaders) == 0):
            columnHeaders.append("Car Name")
            for item2 in detailsTitle:
                columnHeaders.append(item2.text)
            columnHeaders.append("Update Date")
            columnHeaders.append("URL")

        scrapedData.append((innerCarList))
        innerCarList = []

    overallList.append(columnHeaders)
    overallList.append(scrapedData)
    print(overallList)
    return (overallList)



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



returnedData = ask_Input()
add_to_WorkSheet(returnedData)

#uncomment when want to upload to google
#upload_To_Google()
