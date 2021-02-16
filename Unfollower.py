'''
This program determined which users were not following me back,
and unfollowed those users.
'''

import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
import datetime
import csv
chromedriver = "/Users/AngeloKhan/Downloads/chromedriver"
options = Options()
options.headless = False
driver = webdriver.Firefox(options=options)


def login(usr_name, psswrd):
    try:
        driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(3)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(usr_name)
        password_elem = driver.find_element_by_xpath("//input[@name='password']")
        password_elem.clear()
        password_elem.send_keys(psswrd)
        password_elem.send_keys(Keys.RETURN)
        time.sleep(2)

    except:
        print('couldnt login')
        pass

def turn_off_noti():
    try:
        time.sleep(3)
        turn_off_notification = driver.find_element_by_css_selector("button.aOOlW:nth-child(2)")
        turn_off_notification.click()

    except:
        print('No Notification Window')
        pass


def search_n_click(acct_name):
    first_item_in_pop_window = "//div[@class='fuqBx']/a[1]"
    search_xpath = "//input[@placeholder='Search']"
    try:
        search_usr = driver.find_element_by_xpath(search_xpath)
        search_usr.clear()
        search_usr.send_keys(acct_name)
        time.sleep(2.5)
        driver.find_element_by_xpath(first_item_in_pop_window).click()
        time.sleep(2)

    except:
        pass


def remove_nonreciprocators():
    df = pd.read_csv("/Users/AngeloKhan/Desktop/Non_Reciprocators.csv", delimiter=',', names=['acct'])
    Non_Reciprocators_data = df.loc[:, :]
    non_reciprocators = [x[0] for x in Non_Reciprocators_data.values]
    login(usr_name="snugglegiants", psswrd="BiggoDoggo")
    turn_off_noti()
    unfollow_counter = 0
    unfollowed_accts = []

    for acct in non_reciprocators[560:1000]:
        if unfollow_counter <15:
            #SEARCH
            time.sleep(2)
            search_n_click(acct_name=acct)
            ##UNFOLLOW
            try:
                time.sleep(2)
                unfollow_xpath = "//button[@class='_5f5mN    -fzfL     _6VtSN     yZn4P   ']"
                driver.find_element_by_xpath(unfollow_xpath).click()
                time.sleep(2)
                sure_unfollow = "//button[@class='aOOlW -Cab_   ']"
                driver.find_element_by_xpath(sure_unfollow).click()
                print(acct + ": unfollowed")
                unfollow_counter += 1
                unfollowed_accts.append(acct)
                time.sleep(6)
                with open("/Users/AngeloKhan/Desktop/UNFOLLOWED.csv", 'a', newline='') as outputFile:
                    writer = csv.writer(outputFile)
                    writer.writerow([acct])

            except:
                print("Couldn't unfollow: ", acct)
                pass

        else:
            dt = datetime.datetime.now()
            add_hr = datetime.timedelta(hours=0.25)
            dt = dt + add_hr
            print("THE PROGRAM WILL BEGIN AT: ", dt)
            while datetime.datetime.now() < dt:
                time.sleep(60)

            unfollow_counter = 0

remove_nonreciprocators()