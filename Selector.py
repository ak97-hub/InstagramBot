'''
The purpose of this code is to use the urls collected from the
hashtags, and cleany lays out the information about each url(e.g
Amount of likes, comments, the dog breed, and even collects data
like the account names of commenters).
This program also includes a quick downloader that immediatly
downloads either all photos or videos or both from a hashtag
or list of hashtags.

'''

import pandas as pd
import os
import random
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import csv
from Converter_for_Downloadable_urls import Run_Converter
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

def remove_duplicates(filename):

    # making data frame from csv file
    data = pd.read_csv("/Users/AngeloKhan/{}".format(filename))


    # dropping ALL duplicte values
    data = data.drop_duplicates(subset="Href", keep="first")

    # saving data
    data.to_csv("/Users/AngeloKhan/{}".format(filename), sep=',', index=False)
    print("Duplicates removed for {}".format(filename))


def selector():
    path = "/Users/AngeloKhan/Documents/Dogs/"
    files = []
    column = ["Href"]

    for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                files.append(os.path.basename(file))


    rand_sel = random.sample(files, 25)
    final_sample = dict()
    print(rand_sel)

    for f in rand_sel:
        f = 'Documents/Dogs/' + f
        remove_duplicates(filename=f)
        print(f)
        df = pd.read_csv("/Users/AngeloKhan/Documents/Dogs/{}".format(f), delimiter=',')
        data = df.loc[:, column]
        content_list = [x[0] for x in data.values]
        random_sample = random.sample(content_list, 4)
        for href in random_sample:
            final_sample.update({href: f})


        for x in random_sample:
            drop = df.loc[df["Href"] == x, 'Href']
            drop = drop.index.item()
            df = df.drop(drop)

            print("Index is collected & Removed at:", drop)

        df.to_csv("/Users/AngeloKhan/Documents/Dogs/{}".format(f), sep=',', index=False)


    with open("/Users/AngeloKhan/Desktop/Monthly_Content.csv", "w") as File:
        header = ["Href", "Breed"]
        writer = csv.writer(File)
        writer.writerow(header)
        for href, breed in final_sample.items():
            breed = breed.strip(".csv")
            writer.writerow([href, breed])

def quickVids_n_images(profiles, breed):
    print(profiles)
    url = 'https://www.instagram.com/{}'.format(profiles)
    driver.get(url=url)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(5)
    driver.refresh()
    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(5)
    i = 0
    vid_hrefs = []
    pic_hrefs = []
    b_check = None
    new_b_check = True


    while b_check != new_b_check and i < 20: #THIS COLLECTS VIDEOS
    ###Change to counter if you want to collect a limited amount of videos(while i < 10)

        i += 1
        b_check = driver.execute_script("return document.documentElement.scrollTop;")
        driver.execute_script("window.scrollBy(0, 300)")
        time.sleep(0.2)
        driver.execute_script("return document.documentElement.scrollTop;")
        xpath = "//span[@class='mediatypesSpriteVideo__filled__32 u-__7']/ancestor::a[contains(@href,'')]"
        href_elem = driver.find_elements_by_xpath(xpath)
        vid_href = [x.get_attribute('href') for x in href_elem]
        vid_hrefs.extend(vid_href)
        new_b_check = driver.execute_script("return document.documentElement.scrollTop;")
        print("Page Length Check:", b_check, new_b_check)


    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(1)
    h = 0

    while h < 4:  # For 3 scrolls, short rows are best, THIS COLLECTS PICTURES
        h += 1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        hrefs = driver.find_elements_by_xpath("//div[@class='v1Nh3 kIKUG  _bz0w']//a[contains(@href,'')]")
        pic_href = [elem.get_attribute('href') for elem in hrefs]
        pic_hrefs.extend(pic_href)

    vid_hrefs = list(vid_hrefs)
    pic_hrefs = list(pic_hrefs)

    print(vid_hrefs)
    print(pic_hrefs)

    with open('/Users/AngeloKhan/Desktop/Monthly_Content.csv', 'a') as file:
        header = ["Href", "Breed"]
        writer = csv.writer(file)
        writer.writerow(header)

        for vid_href in vid_hrefs[:10]: #Only first 6 videos are collected
            writer.writerow([vid_href, breed])

        for pic_href in pic_hrefs[:10]:
            writer.writerow([pic_href, breed])



###USE IF YOU HAVE A REALLY GOOD PROFILE AND WANT TO GRAB VIDEOS FROM IT

#USE THIS IF YOU WANT TO USE TAGS TO GRAB VIDS & PHOTOS
dog_tags = {'oldenglishsheepdog': 'oldenglishsheepdog','greatdane': 'greatdane',
       'alaskanmalamute': 'alaskanmalamute','canecorso': 'canecorso','dobermanpinscher': 'doberman_pinscher',
        'komondordog': 'komondor', 'newfoundlanddog': 'newfoundlanddog',
        'irishwolfhoundsofinstagram': 'irishwolfhound','frenchmastiff': 'frenchmastiff',
        'neomastiff': 'neomastiff', 'bullmastiffofinstagram': 'bullmastiff', 'leonberger': 'leonberger',
        'greatdanesofinstagram': 'greatdane', 'rottiesofinstagram': 'rottie',
        'bernesemountaindoglovers': 'bernesemountain', 'siberianhusky': 'siberianhusky',
        'englishmastiff': 'englishmastiff','caucasianmountaindog': 'caucasianmountaindog',
        'tibetanmastiff': 'tibetanmastiff','sheepadoodlesofinstagram': 'sheepadoodlesofinstagram'}

finance_profiles = {'getjoemoneyright': 'tips','financefather':'Tips','makingcentsoffinance':'Tips',
                    'savetoinvest':'tips', 'internetbusinesslife': 'Tips', 'investingmentors':'Mindset',
                    'investorsgrow':'Mindset','businesstutorship':'Learning', 'economicfacts':'facts',
                    'entrepreneurialfact':'Facts','billionairity':'Motivation','financekit':'Motivation',
                    'smartinvest101':'Tips','moneysaveop':'Tips','topearnerprocess':'Tips',
                    'nowfuture':'Tips','Financialplanet':'Tips','themodestwallet':'tips',
                    'veemakescents':'Motivation','wordsofsuccess':'motivation', 'businessmoral': 'Tips',
                    'age_of_attitude':'Motivation','grindingondreams':'Motivation','inspiredpal':'Motivation',
                    'mindset.therapy':'Mindset','life.stories.goalcast':'Mindset'}


dog_profile_tags = {'vital_screen_': 'Doberman', 'dobie_odin' : 'Doberman', 'nala_the_needy_rottie': 'Rottweiler',
            'rottweilermom' : 'Rottweiler', 'lovewolfstore': 'Wolf', 'germanshepherrds':'germansheperd',
            'inland_empire_mastinos': 'Neo_Mastiffs','chowpuppies':'Chow_Chow'}


tags = {'newfoundlanddog': 'newfoundlanddog','chowpuppies':'Chow_Chow','alaskanmalamute': 'alaskanmalamute'}
#initiate collecting vids for specific profiles
"""
for profile, breed in profiles.items():
    quickVids(profiles=profile, breed=breed)
"""

#initiate collecting photos & Vids for specific tags
def Run_Selector():
    for tag, breed in tags.items():
        tag = "explore/tags/" + tag
        quickVids_n_images(profiles=tag, breed=breed)

    #remove duplicates in Monthly_Content File
    remove_duplicates(filename='Desktop/Monthly_Content.csv')

    driver.close()

    #Run Converter
    time.sleep(60)
    Run_Converter()
#USE THIS BELOW IF YOU WANT TO  GRAB FILE FROM ALREADY STORED DATA
#selector()

Run_Selector()