'''
This was used to collect the data on any account, such as followers
and following. This was to help determine the ratio of followers
to following, and therefore be used as a tool of whether account
should be followed. For example people who had a lot of followers,
but very little following were most likely no going to follow back.
'''

import datetime
from selenium.webdriver.firefox.options import Options
from Tag_Comment_Liker import *
import pandas as pd

options = Options()
options.headless = True

##COLLECTS DATA ON ANY ACCT- PROFILE NAME, BIO, FOLLOWER, PHOTO NUM
class Scroll:

    def __init__(self):
        self.driver = webdriver.Firefox(options=options)

    def scroller(self, profiles):  # GETS PROFILE DATA- PHOTO_NUM, BIO, FOllOWERS_NUM
        driver = self.driver
        for num, profile in enumerate(profiles, start=1):
            try:
                driver.get("https://www.instagram.com/{}/".format(profile))
                driver.execute_script("window.scrollTo(0, 0)")
                photo_count_raw = driver.find_elements_by_xpath(
                    "/html/body/span/section/main/div/header/section/ul/li[1]/a/span")
                photo_count = [x.text for x in photo_count_raw]
                follower_count_raw = driver.find_elements_by_xpath(
                    "/html/body/span/section/main/div/header/section/ul/li[2]/a/span")
                follower_count = [x.text for x in follower_count_raw]
                bio_raw = driver.find_elements_by_xpath("/html/body/span/section/main/div/header/section/div[2]/span")
                bio = [x.text for x in bio_raw]
                if bio == []:
                    bio = ['None']
                time.sleep(0.5)
                print(profile, photo_count[0], follower_count[0], "\n" + bio[0] + "\n")
                with open("/Users/AngeloKhan/Desktop/Content_profile_list2.csv", "a", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([profile, photo_count[0], follower_count[0], bio[0]])

            except:
                print(num, profile + " No Longer Exists")
                with open("/Users/AngeloKhan/Desktop/Outdated_profiles.txt", "a", newline='') as file:
                    file.write(profile + "\n")
                continue

        print("PROJECT HAS FINISHED")


with open("/Users/AngeloKhan/Desktop/Content_profile_list.txt", 'r', newline='') as outputFile:
    profile_list_raw = outputFile.readlines()
    profile_list = [x.strip('\n') for x in profile_list_raw]
    profile_list = set(profile_list)

print(profile_list)
print(len(profile_list))
profile_info = Scroll()
profile_info.scroller(profile_list)
