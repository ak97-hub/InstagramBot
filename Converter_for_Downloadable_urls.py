'''This program locates the source url within the main set of
 collected urls, and adds it to a csv file'''

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
import time
options = Options()
options.headless = True
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import csv
driver = webdriver.Firefox(options=options)

def get_download_url(breed):
    photo_href = []
    vid_href = []

    #GET PROFILE NAME
    try:
        href_elem = driver.find_elements_by_xpath("//a[@class='sqdOP yWX7d     _8A5w5   ZIAjV ']")
        href = [x.get_attribute('href') for x in href_elem]
        href = href[0]
        head, sep, href_tail = href.partition('.com/')
        profile_name = href_tail.strip("/")
        print("Account name: " + profile_name)
        print("Breed: "+breed)

    except:
        print('couldnt get account name')
        profile_name = "PAGE_NOT_FOUND"

    #GET IMAGE DOWNLOAD URL
    try:
        href_elem = driver.find_elements_by_xpath("//img[@class='FFVAD']")
        photo_href = [x.get_attribute('src') for x in href_elem]
        print("This is your photo " + photo_href[0])

    except:
        pass
    #GET VIDEO DOWNLOAD URL

    try:
        href_elem = driver.find_elements_by_xpath("//video[@class='tWeCl']")
        vid_href = [x.get_attribute('src') for x in href_elem]
        print("This is your video " + vid_href[0])

    except:
        pass

    if photo_href != []:
        with open("/Users/AngeloKhan/Desktop/Downloadable_Monthly_Content.csv", 'a', newline='') as outputFile:
            writer = csv.writer(outputFile)
            writer.writerow([photo_href, breed, profile_name, "Photo"])


    elif vid_href != []:
        with open("/Users/AngeloKhan/Desktop/Downloadable_Monthly_Content.csv", 'a', newline='') as outputFile:
            writer = csv.writer(outputFile)
            writer.writerow([vid_href, breed, profile_name, "Videos"])
    else:
        pass



#Open Files Holding Untranslated URL
#MAKE SURE YOU ADJUST FILE NAME TO FILE YOU CARE TO CONVERT TO DOWNLOADABLE URLS
#    ***MAKE SURE YOU HAVE HREF AND BREED IN HEADER***
def Run_Converter():
    file_names_raw_content = ["Monthly_Content.csv"]

    #Iterate through files
    for file_name in file_names_raw_content:
        df = pd.read_csv("/Users/AngeloKhan/Desktop/{}".format(file_name), delimiter=',')
        columns = ['Href', 'Breed']
        data = df.loc[:, columns]
        temp_dictionary = {k: v for k, v in data.values}
        primary_href_dict = dict()

        #Remove all special characters from link
        for k, v in temp_dictionary.items():
            k = k.replace("]", "")
            k = k.replace("[", "")
            k = k.replace("'", "")
            primary_href_dict.update({k: v})

        print(primary_href_dict)

        #RUN THE PROGRAM
        for href, breed in primary_href_dict.items():
            try:
                driver.get(href)
                time.sleep(0)
                driver.refresh()
                time.sleep(0)
                get_download_url(breed=breed)
                print("\n")

            except:
                print(href + ' is not a real href')
                pass
    #ADD HEADER TO DOWNLOADABLE MONTHLY FILES
    data = pd.read_csv("/Users/AngeloKhan/Desktop/Downloadable_Monthly_Content.csv", names= ['Href',
                                                                                             'Breed',
                                                                                             'Profile_name',
                                                                                             'Media_type'])

    data.to_csv("/Users/AngeloKhan/Desktop/Downloadable_Monthly_Content.csv", sep=',', index=False)
    driver.close()

"""
THIS IS USED FOR TESTING BOTH PHOTO AND VIDEO IF YOU RUN INTO PROBLEMS
primary_href=["https://www.instagram.com/p/B-zkWaXhdRt/","https://www.instagram.com/p/B-2kcSOBjfF/"]
for href in primary_href:
    driver.get(href)
    get_download_url(breed="doggo")
    print("\n")

driver.close()
"""
