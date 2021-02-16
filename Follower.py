'''
This program logins into insta account and follows accounts
collected from when program was collecting urls of popular posts.
The followers are commenters of popular posts. An API was also
used. Clarifai provides a free machine learning API that I used
to check if there were any dogs in the profile pics, before I
followed the user. This was because those who had photos in their
profile pic were most likely to follow back.

'''

import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from clarifai.rest import ClarifaiApp, Concept
chromedriver = "/Users/AngeloKhan/Downloads/chromedriver"
options = Options()
options.headless = False
driver = webdriver.Firefox(options=options)
from selenium.webdriver.common.keys import Keys
import pandas as pd
import csv
import datetime
import requests
                                    ###FOLLOWS PROVIDED ACCOUNTS###

def remove_annotations(number):
    if 'k' and '.' in number:
        number = number.replace('.', '')
        number = number.replace('k', '00')

    elif 'k' in number and '.' not in number:
        number = number.replace('k', '000')

    elif ',' in number:
        number = number.replace(',', '')

    elif ' ' in number:
        head, sep, tail = number.partition(" ")
        number = head

    return number

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

def click_n_scroll_followers_tab(scroll_amt):
    i = 1
    #CLICK FOLLOWERS TAB
    try:
        time.sleep(2)
        followers_xpath = "//ul[@class='k9GMp ']/li[2]/a"
        driver.find_element_by_xpath(followers_xpath).click()

    except:
        pass

    while i < scroll_amt:
        #SCROLL THROUGH WINDOW
        try:
            time.sleep(1.25)
            follow_window_xpath = "//div[@class='isgrP']"
            scr1 = driver.find_element_by_xpath(follow_window_xpath)
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)

        except:
            pass

        i += 1

    print("Finished Scrolling through Follower Tab")

def click_scroll_following_tab(scroll_amt):
    i = 1
    # CLICK FOLLOWING TAB
    try:
        time.sleep(2)
        following_xpath = "//ul[@class='k9GMp ']/li[3]/a"
        driver.find_element_by_xpath(following_xpath).click()

    except:
        pass

    while i < scroll_amt:
        # SCROLL THROUGH WINDOW
        try:
            time.sleep(1.25)
            follow_window_xpath = "//div[@class='isgrP']"
            scr1 = driver.find_element_by_xpath(follow_window_xpath)
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)

        except:
            pass

        i += 1

    print("Finished Scrolling through Following Tab")

def image_checker(url):
    time.sleep(2)
    app = ClarifaiApp(api_key='381b51dda43e4c60a957368a68046b49')
    model = app.models.get("general-v1.3")
    select_concept_list = [Concept(concept_name='Dog'), Concept(concept_id='ai_8S2Vq3cR')]
    confirmation = ''
    try:
        tags = model.predict_by_url(url, select_concepts=select_concept_list)

        for tag in tags['outputs'][0]['data']['concepts']:
            print(tag['name'], tag['value'])
            if tag['value'] > 0.85:
                confirmation = 'yes'
            else:
                confirmation = 'no'

    except:
        print('couldnt retrieve photo identification')
        pass

    return confirmation

def profile_pic(row_num):
    profile_pic_xpath = "//div[@class='PZuss']/li[{}]/div[1]/div[1]/div[1]/a/img".format(row_num)
    img_src = ''
    try:
        img_src = driver.find_element_by_xpath(profile_pic_xpath)
        img_src = img_src.get_attribute('src')
        print(img_src)

    except:
        try:
            profile_pic_xpath = "//div[@class='PZuss']/li[{}]/div[1]/div[1]/div[1]/span/img".format(row_num)
            img_src = driver.find_element_by_xpath(profile_pic_xpath)
            img_src = img_src.get_attribute('src')
            print(img_src)

        except:
            print('couldnt find image source url')
            pass

    return img_src

def click_follow(row_num):
    follow_status = ''
    try:
        follow_button_xpath = "//div[@class='PZuss']/li[{}]/div[1]/div[2]/button".format(row_num)
        follow_button = driver.find_element_by_xpath(follow_button_xpath)
        status = follow_button.text
        if status == "Follow":
            try:
                follow_button.click()
                print('Followed')
                follow_status = "Followed"

            except:
                pass
        else:
            print("Following already")

    except:
        print('couldnt follow account')
        pass

    return follow_status


def close_window():
    try:
        time.sleep(2)
        close_xpath = "//div[@class='WaOAr']/button"
        close = driver.find_element_by_xpath(close_xpath)
        close.click()

    except:
        print('couldnt close window')
        pass

'''
def following():
    follow_button_xpath = "//button[@class='_5f5mN       jIbKX  _6VtSN     yZn4P   ']"
    search_xpath = "//input[@placeholder='Search']"
    first_item_in_pop_window = "//div[@class='fuqBx']/a[1]"
    followers = ''
    following = ''
    following_count_limit = 0

    df = pd.read_csv("/Users/AngeloKhan/Desktop/Follower_Tracker_2.csv", delimiter=',')
    column = ['Profile']
    data = df[column]
    accts = [x[0] for x in data.values]

    for acct in accts[500:700]:

        try:
            time.sleep(2)
            search_usr = driver.find_element_by_xpath(search_xpath)
            search_usr.clear()
            search_usr.send_keys(acct)
            time.sleep(4)
            driver.find_element_by_xpath(first_item_in_pop_window).click()
            time.sleep(5)

        except:
            pass

        try:
            followers_count_xpath = "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span"
            followers = driver.find_element_by_xpath(followers_count_xpath)
            followers = followers.get_attribute("title")
            following_count_xpath = "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span"
            following = driver.find_element_by_xpath(following_count_xpath).text
            time.sleep(1)

        except:
            print('***acct private***')

            try:
                followers_count_xpath = "/html/body/div[1]/section/main/div/header/section/ul/li[2]/span"
                following_count_xpath = "/html/body/div[1]/section/main/div/header/section/ul/li[3]/span"
                followers = driver.find_element_by_xpath(followers_count_xpath).text
                following = driver.find_element_by_xpath(following_count_xpath).text
            except:
                pass

        followers = remove_annotations(followers)
        following = remove_annotations(following)
        print(acct,
              "Followers: " + followers,
              "Following: " + following)

        try:
            ratio = int(following) / int(followers)
            print("Ratio: " + str(round(ratio, 2)))

            if float(ratio) > 0.80 and int(following) > 750:
                try:
                    driver.find_element_by_xpath(follow_button_xpath).click()
                    following_count_limit += 1
                    print(acct + " was followed")

                except:
                    try:
                        priv_follow_button_xpath = "/html/body/div[1]/section/main/div/header/section/div[1]/button"
                        driver.find_element_by_xpath(priv_follow_button_xpath).click()
                        following_count_limit += 1
                        print(acct + " was followed")

                    except:
                        pass
                    pass

                with open('/Users/AngeloKhan/Desktop/Followed.csv', 'a') as file:
                    writer = csv.writer(file)
                    ratio = round(ratio, 3)
                    writer.writerow([acct, followers, following, ratio])
        except:
            pass

        if following_count_limit >= 20:
            print('limit reached, resting 1hr')
            dt = datetime.datetime.now()
            add_hr = datetime.timedelta(hours=1)
            dt = dt + add_hr
            print("THE PROGRAM WILL BEGIN AT: ", dt)
            while datetime.datetime.now() < dt:
                time.sleep(60)

            following_count_limit = 0

    driver.close()

    df = pd.read_csv("/Users/AngeloKhan/Desktop/Follower_Tracker.csv",
                     delimiter=',', names=['Href', 'Followers', 'Following', 'Ratio'])

    df.to_csv("/Users/AngeloKhan/Desktop/Follower_Tracker.csv",
              sep=',', index=False)

'''

def parent_follower(usr_name, psswrd, accts, follow_count):
    login(usr_name=usr_name, psswrd=psswrd)
    turn_off_noti()
    for acct in accts:
        print(acct)
        search_n_click(acct_name=acct)
        click_n_scroll_followers_tab(scroll_amt=30)
        i = 1
        followed_count = 0
        while i < 100:
            img_src = profile_pic(row_num=i)
            confirmation = image_checker(url=img_src)
            if confirmation == 'yes':
                status = click_follow(i)
                if status == "Followed":
                    followed_count += 1
                    print('Followed Count: ', followed_count)

            if followed_count > follow_count:
                i = 101

            time.sleep(2.5)
            i += 1
        close_window()
        dt = datetime.datetime.now()
        print("program will begin 1hr from now: ", dt)
        mins = 45
        time.sleep(mins *60)


accts = ['entyssar_souissy','gatsbysiberian','horseshoundsandhens','_mollymoos','bear_the_good_dog',
         'cookie_cannelle','ariana_goldenretriever','ares.minibullterrier','huskyworkout','bad_dog_romeo']

parent_follower(usr_name="huskies.culture",
                psswrd="TacticalBabes1997",
                accts=accts,
                follow_count=40)