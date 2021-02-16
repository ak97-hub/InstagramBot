'''
This program was used to mass collect all videos and photos,
this program was the first program developed to collect content.
This program is simplified as project progressed.
'''
import pandas as pd
from Tag_Comment_Liker import *
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True


class ContentFinder:

    def __init__(self):
        self.driver = webdriver.Firefox(options=options)

    def checker(self):
        driver = self.driver
        global manipulator

        try:
            x_path = "/html/body/span/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]"
            href_elem = driver.find_elements_by_xpath("{}//a[contains(@href,'')]".format(x_path))
            href = [x.get_attribute('href') for x in href_elem]

        except:
            pass
        if href == []:
            print('This is a key 2')
            manipulator = 2
        else:
            manipulator = 3

        return manipulator

    def breeder(self):
        global breed
        df = pd.read_csv("/Users/AngeloKhan/Desktop/Profile_breed_info.csv", delimiter=',')
        columns = ['Profile', 'Breed']
        breed = df.loc[:, columns]
        breed = breed.values
        breed = {k: v for k, v in breed}

    def scroller_and_collect(self):
        driver = self.driver
        self.bottom_checker = driver.execute_script("return document.documentElement.scrollTop;")
        driver.execute_script("window.scrollBy(0, 321)")
        time.sleep(2)
        self.new_bottom_checker = driver.execute_script("return document.documentElement.scrollTop;")


    def content_grabber(self, photo_row, column, photos_2_collect, profile, mani):
        driver = self.driver

        try:
            if (photo_row <= 10) and (photo_row <= photos_2_collect):
                x_path = "/html/body/span/section/main/div/div[{}]/article/div[1]/div/div[{}]/div[{}]".format(mani ,photo_row, column)
                href_elem = driver.find_elements_by_xpath("{}//a[contains(@href,'')]".format(x_path))
                key = 1

            elif (photo_row > 10) and (photo_row <= photos_2_collect):
                css_select = 'div.Nnq7C:nth-child(10) > div:nth-child({}) > a:nth-child(1)'.format(column)
                href_elem = driver.find_elements_by_css_selector(css_select)
                x_path = "/html/body/span/section/main/div/div[{}]/article/div[1]/div/div[10]/div[{}]".format(mani, column)
                key = 1

            elif (photo_row > 10) and (photo_row > photos_2_collect):
                vid_x_path = "/html/body/span/section/main/div/div[{}]/article/div[1]/div/div[10]/div[{}]/a/div[2]/span[@aria-label='Video']".format(mani, column)
                driver.find_element_by_xpath(vid_x_path)
                x_path = "/html/body/span/section/main/div/div[{}]/article/div[1]/div/div[10]/div[{}]".format(mani, column)
                css_select = 'div.Nnq7C:nth-child(10) > div:nth-child({}) > a:nth-child(1)'.format(column)
                href_elem = driver.find_elements_by_css_selector(css_select)
                key = 2

            elif (photo_row <= 10) and (photo_row > photos_2_collect):
                vid_x_path = "/html/body/span/section/main/div/div[{}]/article/div[1]/div/div[{}]/div[{}]/a/div[2]/span[@aria-label='Video']".format(mani, photo_row, column)
                driver.find_element_by_xpath(vid_x_path)
                x_path = "/html/body/span/section/main/div/div[{}]/article/div[1]/div/div[{}]/div[{}]".format(mani, photo_row, column)
                href_elem = driver.find_elements_by_xpath("{}//a[contains(@href,'')]".format(x_path))
                key = 2

            href = [x.get_attribute('href') for x in href_elem]
            hover_xpath = driver.find_element_by_xpath(x_path)
            hover = ActionChains(driver).move_to_element(hover_xpath)
            hover.perform()
            time.sleep(1)
            post_info = driver.find_elements_by_xpath("//div[@class='Nnq7C weEfm']//li[@class='-V_eO']//span")
            post_information = [elem.text for elem in post_info]

            if key == 1:
                with open("/Users/AngeloKhan/Documents/Dogs/{}.csv".format(breed[profile]), 'a', newline='') as outputFile:
                    writer = csv.writer(outputFile)
                    writer.writerow([href, post_information[0], post_information[2]])

            elif key == 2:
                with open("/Users/AngeloKhan/Documents/Dogs/{}Vids.csv".format(breed[profile]), 'a', newline='') as outputFile:
                    writer = csv.writer(outputFile)
                    writer.writerow([href, post_information[0], post_information[2]])

        except:
            pass

    def collecting(self, profiles, limit):
        driver = self.driver

        for profile in profiles.keys():
            print(profile, "Will begin to have its data collected")
            print(breed[profile])
            driver.get("https://www.instagram.com/{}".format(profile))
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 0)")
            time.sleep(2)
            driver.execute_script("window.scrollBy(0, 230)")
            photos_2_collect = profiles[profile] + 1
            mani = self.checker()
            print(mani)

            for photo_row in range(1, photos_2_collect):
                self.scroller_and_collect()
                print(photo_row, self.bottom_checker, self.new_bottom_checker)

                if self.bottom_checker != self.new_bottom_checker:
                    for column in range(1, 4):
                        self.content_grabber(photo_row=photo_row, column=column, photos_2_collect=photos_2_collect,profile=profile,mani=mani)

            while self.bottom_checker != self.new_bottom_checker and photo_row < limit: ##Collects vids till done scrolling/120 rows
                photo_row += 1
                print(photo_row, self.bottom_checker, self.new_bottom_checker)
                self.scroller_and_collect()
                for column in range(1, 4):
                    self.content_grabber(photo_row=photo_row, column=column, photos_2_collect=(photo_row-1),profile=profile,mani=mani)

            print(profile, "Has been Completed")



df = pd.read_csv("/Users/AngeloKhan/Desktop/Great_800.csv", delimiter=',')
data = df.loc[:, :]
profile_dictionary = {k: v for k,v in data.values}
a = ContentFinder()
a.breeder()
a.collecting(profiles=profile_dictionary, limit=45)