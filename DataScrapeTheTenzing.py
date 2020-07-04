from urllib.request import urlopen, Request
import requests
from bs4 import BeautifulSoup as soup
import re
import time
import datetime

# Test Commit
def ScrapeWebpage():
    url = Request('https://www.thetenzingapts.com/floorplans.aspx', headers={'User-Agent': 'Mozilla/5.0'})

    #opening up connection, getting page
    uClient = urlopen(url)
    page_html = uClient.read()
    uClient.close()

    #parsing page
    page_soup = soup(page_html, "html.parser")
    pre_sub_soup = page_soup.findAll('tbody', {"class":"floorplan-details"})

    sub_soup = soup(pre_sub_soup[2].prettify(), "html.parser") # 0 = 1Br, 1 = 2Br, 2 = 3Rr
    # print(sub_soup)

    #---------rent---------------------#
    floorplans_all = sub_soup.findAll('td', {"data-label":"Rent"})
    floorplan_soup = soup(floorplans_all[0].prettify(), "html.parser")
    rent_span = floorplan_soup.findAll('span', {"class":"sr-only"})

    fp_all_details = [span.next_sibling.string.strip() for span in sub_soup.findAll(class_='sr-only')]

    # print(row_details)


    #---------available----------------#y
    results = page_soup.findAll('td', {"data-label":"Availability"})

    string = "id=\"3"

    i = 0
    # for pos in results:
    #     if string in str([pos]):
    #         print(i)
    #     i = + 1
    availbility_int_list = []
    while i < len(results):
        if string in str(results[i]):
            availbility_int_list.append(i)
            i = i + 1
        else:
            i = i + 1

    # print(availbility_int_list)

    scraped_availability_list = []
    for row in availbility_int_list:
        a = soup(results[row].prettify(), "html.parser")

        available_found = a.findAll("span", {"class":"available-fp"})

        available = str(available_found[0])
        available_list = re.findall(r'\d+', available)

        scraped_availability_list.append(str(available_list[0]) + " Available")

    #----------------------------------#

    # print(len(row_details))
    floorplan_count = int(len(fp_all_details) / 6) # each row has 6 items in row_details
    # print(floorplan_count)

    if floorplan_count == 1:
        fp_all_details[5] = scraped_availability_list[0]

    if floorplan_count == 2:
        fp_all_details[5] = scraped_availability_list[0]
        fp_all_details[11] = scraped_availability_list[1]

    if floorplan_count == 3:
        fp_all_details[5] = scraped_availability_list[0]
        fp_all_details[11] = scraped_availability_list[1]
        fp_all_details[17] = scraped_availability_list[2]

    # time.wait(1)
    
    return fp_all_details

# print(ScrapeWebpage)

# print(15 - datetime.datetime.now().minute % 15)
