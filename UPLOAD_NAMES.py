'''
This was to help automate the process of mass scheduling and
helped with uploading photos and videos with appropriate
credit to creator of content to later.com
'''

from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
chromedriver = "/Users/AngeloKhan/Downloads/chromedriver"
driver = webdriver.Chrome(chromedriver)
from selenium.webdriver.common.keys import Keys
import pyperclip
from selenium.webdriver.common.action_chains import ActionChains

def upload_names():
    profile_name = ''
    i = 0

    try:
        driver.get("https://app.later.com/user/login")
        options = Options()
        options.headless = False
        time.sleep(3)
        user_name_elem = driver.find_element_by_xpath("//input[@autocomplete='username']")
        user_name_elem.clear()
        user_name_elem.send_keys("khanangelo97@gmail.com")
        password_elem = driver.find_element_by_xpath("//input[@autocomplete='current-password']")
        password_elem.clear()
        password_elem.send_keys("fuhgen-4saqcY-fyxqid")
        password_elem.send_keys(Keys.RETURN)
        time.sleep(5)

    except:
        pass

    ##CLICK ON MEDIA LIBRARY
    try:
        xpath = "//a[@id='ember99']"
        driver.find_element_by_xpath(xpath).click()
        time.sleep(2)

    except:
        print('couldnt click media library')
        pass

    ##CLICK LIST MODE
    try:
        xpath = "//div[@class='o--btn o--btn--outline ']"
        driver.find_element_by_xpath(xpath).click()
        time.sleep(10)

    except:
        print("couldnt change to list mode")
        pass

    #CLICK LOAD BUTTON
    while i < 20:
        try:
            time.sleep(2)
            xpath = "//div[@class='cMT--tbody__footer']/a[1]"
            driver.find_element_by_xpath(xpath).click()

        except:
            print("couldnt find load button")

        i += 1

    i = 0
    while i < 50:
        i += 1
        #FIND THE ACCOUNT NAME

        try:
            xpath = "//table[@class='o--table o--table--sort o--table--hover u--m__b__0']/tbody[1]/tr[{}]/td[4]/p[1]".format(
                i)
            profile_name = driver.find_element_by_xpath(xpath).text
            print(profile_name)
            time.sleep(1)

        except:
            print('could not find profile name')
            pass

        ##CLICK PROFILE
        try:
            xpath = "//table[@class='o--table o--table--sort o--table--hover u--m__b__0']/tbody[1]/tr[{}]".format(i)
            driver.find_element_by_xpath(xpath).click()
            time.sleep(1)

        except:
            print("couldnt click profile")
            pass

        #CLICK THE EDIT BUTTON
        try:
            xpath = "//a[@class='u--m__l__sm u--text--sm u--text--uppercase']"
            driver.find_element_by_xpath(xpath).click()
            time.sleep(1)

        except:
            print("couldnt click edit button")

        ##NOTES WINDOW
        try:
            xpath = "//textarea[@id='textareaMediaNote']"
            notes_elem = driver.find_element_by_xpath(xpath)
            notes_elem.clear()
            head, sep, tail = profile_name.partition('-')
            final_text = "@@" + head
            final_note = """
Follow: @huskies.culture
Follow: @huskies.culture
.
.
.
.
.
#bigdog #bigdoggos
#giantbreed #gentlegiants #gentlegiantsofinstagram #gentlegiantoftheday 
#doglove #husky #huskylove #huskies #huskyofinstagram
#dogloversofinstagram

Tiktok Credit : 

"""
            final_note = final_note + final_text
            notes_elem.click()
            notes_elem.send_keys(final_note)
            update_xpath = "//button[@class='o--btn o--btn--primary']" #UPDATE WINDOW
            driver.find_element_by_xpath(update_xpath).click()
            time.sleep(1.5)
            driver.execute_script("window.scrollTo(0, 0);")

            #Click X to leave the notes area
            try:
                close_xpath = "//div[@id='ember1860']/div/i"
                driver.find_element_by_xpath(close_xpath).click()

            except:
                try:
                    close_xpath = "/html/body/div[9]/div/div[5]/main/div[4]/div[2]/div[1]/div/div/div[1]/i"
                    driver.find_element_by_xpath(close_xpath).click()

                except:
                    try:
                        close_xpath = "/html/body/div[7]/div/div[5]/main/div[4]/div[2]/div/div/div/div[1]/i"
                        driver.find_element_by_xpath(close_xpath).click()
                    except:
                        pass


            time.sleep(2)

        except:
            pass

upload_names()
#you could create a checker with free time
#change the upload amount before starting program