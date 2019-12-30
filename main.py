# import libraries
from datetime import datetime
import sys
import os.path
import pandas
import openpyxl
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from bs4 import BeautifulSoup



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




def append_Worksheet(returnedData):
    if (os.path.isfile('carEvalsAutomated.xlsx') == False):
        wb = openpyxl.Workbook()
        ws = wb.create_sheet('Car Evaluations', 0)
    else:
        wb = openpyxl.load_workbook('carEvalsAutomated.xlsx')
        ws = wb.get_sheet_by_name('Car Evaluations')

    actualData = returnedData[1]
    headers = returnedData[0]
    iteratorC = 0

    for column in range(1, len(headers) + 1):
         referencedcell = ws.cell(row=1, column=column)
         if (referencedcell.value == None):
             referencedcell.value = headers[iteratorC]
         iteratorC += 1

    startingRow = 1
    foundBlank = False
    i = 1
    while foundBlank == False:
         if ws.cell(row=i, column=1).value == None:
              print(i)
              startingRow = i
              foundBlank = True
         i += 1

    for row, array in enumerate(actualData, start=startingRow-1):
         for col, value in enumerate(array):
             print(str(value))
             referencedcell = ws.cell(row=row+1, column=col+1)
             referencedcell.value = value

    wb.save('carEvalsAutomated.xlsx')



returnedData = ask_Input()
append_Worksheet(returnedData)
