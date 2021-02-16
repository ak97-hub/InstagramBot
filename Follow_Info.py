'''
This was used to grab the accounts in which popular pages were
following. This was because most were following accounts that
were follow 4 follow accounts. Essentially other dog pages
that would reciprocate a follow, as to boost each others
following count. Bringing up our following amount allowed us
to bring in more followers easily.
'''

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chromedriver = "/Users/AngeloKhan/Downloads/chromedriver"
options = Options()
options.headless = False
driver = webdriver.Chrome(chromedriver, options=options)
chromedriver = "/Users/AngeloKhan/Downloads/chromedriver"
from selenium.webdriver.common.keys import Keys
import csv
import pandas as pd


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
            time.sleep(3)
            follow_window_xpath = "//div[@class='isgrP']"
            scr1 = driver.find_element_by_xpath(follow_window_xpath)
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)

        except:
            pass

        i += 1

    print("Finished Scrolling through Following Tab")

def grab_acct_names(num_of_accts, filename):
    i = 1
    follower_profiles = []
    while i < num_of_accts +1:
        #GET ACCT NAME
        try:
            time.sleep(0.15)
            acct_name_xpath = "//div[@class='PZuss']/li[{}]/div[1]/div[1]/div[2]/div[1]/a".format(i)
            acct_name = driver.find_element_by_xpath(acct_name_xpath)
            acct_name = acct_name.get_attribute("title")
            print(acct_name, len(follower_profiles))
            follower_profiles.append(acct_name)

        except:
            print('couldnt get acct name')
            pass
        i += 1

    for profile in follower_profiles:
        with open('/Users/AngeloKhan/Desktop/{}.csv'.format(filename), 'a') as file:
            writer = csv.writer(file)
            writer.writerow([profile])

    # Exit out of window
    try:
        exit_xpath = "/html/body/div[2]"
        driver.find_element_by_xpath(exit_xpath).click()

    except:
        pass

def close_window():
    try:
        time.sleep(2)
        close_xpath = "//div[@class='WaOAr']/button"
        close = driver.find_element_by_xpath(close_xpath)
        close.click()

    except:
        print('couldnt close window')
        pass

def reciprocator_checker():
    df = pd.read_csv("/Users/AngeloKhan/Desktop/Following.csv", delimiter=',', names=['acct'])
    Following_data = df.loc[:, :]
    Following = [x[0] for x in Following_data.values]

    df = pd.read_csv("/Users/AngeloKhan/Desktop/Followers.csv", delimiter=',', names=['acct'])
    Follower_data = df.loc[:, :]
    Followers = [x[0] for x in Follower_data.values]
    non_reciprocators = []
    reciprocators = []
    for acct in Following[:]:
        if acct not in Followers:
            non_reciprocators.append(acct)

        else:
            reciprocators.append(acct)

    print('amt following back = ', len(reciprocators))
    print('amt not following back = ', len(non_reciprocators))

    for acct in non_reciprocators:
        with open("/Users/AngeloKhan/Desktop/Non_Reciprocators.csv", 'a', newline='') as outputFile:
            writer = csv.writer(outputFile)
            writer.writerow([acct])


def Run_Follow_Collector(acct_names):

    login(usr_name='snugglegiants', psswrd='BiggoDoggo')
    turn_off_noti()
    for acct in acct_names:
        search_n_click(acct_name=acct)
        print(acct + " searched")
        click_n_scroll_followers_tab(scroll_amt=350)
        grab_acct_names(num_of_accts=2186, filename='Followers')
        close_window()
        click_scroll_following_tab(scroll_amt=350)
        time.sleep(100)
        grab_acct_names(num_of_accts=2000, filename="Following")
    driver.close()


acct_names = ['doberman_universe', '_merleman', '_tibetanmastiff', 'kennel_blissgrand',
              'thenewfcrew', 'hugo_the_newfie', 'thepawsomegsdtrio', 'dogoargentino_worldwide',
              'howtogetawaywithwolves', 'the_staffy_boys', 'malinois_universe',
              'doberman_loveteams', 'charlotte_briggs17']

acct_names = ['huskies.culture']

Run_Follow_Collector(acct_names=acct_names)
reciprocator_checker() #ONLY USE THIS IF CHECKING FOLLOWERS OF OWN ACCT