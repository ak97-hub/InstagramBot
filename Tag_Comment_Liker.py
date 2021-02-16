'''
This program was used to like the main post, and like the
comments under that post. And was also originally used to
find content using hashtags
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chromedriver = "/Users/AngeloKhan/Downloads/chromedriver"
options = Options()
options.headless = True

class InstagramBot:


    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome(chromedriver)

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver

        try:
            driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(2)
            user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
            user_name_elem.clear()
            user_name_elem.send_keys("snugglegiants")
            password_elem = driver.find_element_by_xpath("//input[@name='password']")
            password_elem.clear()
            password_elem.send_keys("BiggoDoggo")
            password_elem.send_keys(Keys.RETURN)
            time.sleep(3)

        except:
            pass

    def find_hashtag_and_collect_hrefs(self, tag):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/{}/".format(tag))
        time.sleep(2)
        pic_hrefs = []
        for i in range(1, 6):#For few rows are best
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            hrefs = driver.find_elements_by_xpath("//div[@class='v1Nh3 kIKUG  _bz0w']//a[contains(@href,'')]")
            pic_href = [elem.get_attribute('href') for elem in hrefs]
            pic_hrefs.extend(pic_href)

        pic_hrefs = list(set(pic_hrefs))
        print(tag+' photos: ' + str(len(pic_hrefs)))

        return pic_hrefs


    def like_photos_and_comments(self, tag):
        like_counter = 0
        like_comment_counter = 0
        driver = self.driver
        pic_hrefs = self.find_hashtag_and_collect_hrefs(tag)
        views = '0'
        likes = '0'


        for href in pic_hrefs[:70]:
            driver.get(href)
            time.sleep(0.5)
            comments_liked_per_photo = 0
            for i in range(1, 5):  # Scroll to load page
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1.5)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)

            try:
                # LIKE THE PHOTO
                xpath = "//section[@class='ltpMr Slqrh']/span[@class='fr66n']/button"
                driver.find_element_by_xpath(xpath).click()
                print("***successfully liked the pic***")
                time.sleep(0.5)
                like_counter += 1

            except:
                pass

            try:
                # RETRIEVE VIEWS
                views = driver.find_element_by_xpath("//span[@class='vcOH2']/span[1]")  ## VIEWS xpath
                print('found views element')
                views = views.text
                head, sep, tail = views.partition(",")
                views = head + tail
                print("VIEWS: " + views)

            except:
                pass

            try:
                # RETRIEVE LIKES
                xpath_likes = "//div[@class='Nm9Fw']/button[1]/span"
                likes = driver.find_element_by_xpath(xpath_likes) # LIKES x_path
                likes = likes.text
                likes = likes.replace(',', '')
                print("TOTAL LIKE: " + likes)

            except:
                pass


            if like_comment_counter < 80:
                # KEEP TRACK OF COMMENT LIKES ONLY CONTINUE IF BELOW 50
                i = 0
                while i < 10:
                    # LOAD ALL THE COMMENTS
                    try:
                        load_comment_x_path = "//span[@aria-label='Load more comments']" #LOAD COMMENT XPATH
                        driver.find_element_by_xpath(load_comment_x_path).click()  ##Load all comments
                        time.sleep(1)
                        i += 1

                    except:
                        i += 10

                print('All comments are loaded')

                i = 1
                while i < 11:
                    # LIKE THE FIRST 10 COMMENTS
                    try:
                        # COMMENT LIKING XPATH BELOW
                        xpath = "//ul[@class='XQXOT   pXf-y']/ul[{}]/div[1]/li[1]/div[1]/span[1]/div[1]/button".format(i)
                        driver.find_element_by_xpath(xpath).click()
                        time.sleep(2)

                    except:

                        try:
                            # COMMENT LIKING XPATH BELOW(SECOND VERSION OF IT)
                            xpath = "//ul[@class='XQXOT   ']/ul[{}]/div[1]/li[1]/div[1]/span[1]/div[1]/button".format(i)
                            driver.find_element_by_xpath(xpath).click()
                            time.sleep(2)

                        except:
                            comments_liked_per_photo = i - 1
                            print("this is how many comments were liked: "
                                  + str(comments_liked_per_photo) + "/10")
                            i += 10
                            pass

                    i += 1
            like_comment_counter += comments_liked_per_photo

            print("Total photos liked: " + str(like_counter))

            #DOWNLOAD HIGHLY ENGAGED CONTENT FOR LATER USE
            '''
            if int(views) > 5000:
                with open("/Users/AngeloKhan/Desktop/Potential_Content_Videos.csv", 'a', newline='') as outputFile:
                    writer = csv.writer(outputFile)
                    writer.writerow([href, tag, views])

            elif int(likes) > 500:
                with open("/Users/AngeloKhan/Desktop/Potential_Content_pictures.csv", 'a', newline='') as outputFile:
                    writer = csv.writer(outputFile)
                    writer.writerow([href,tag, likes])

            else:
                pass
                
            '''



    def turnOffNotification(self):
        driver = self.driver
        try:
            turn_off_notification = driver.find_element_by_css_selector("button.aOOlW:nth-child(2)")
            turn_off_notification.click()
        except:
            #print('No Notification Window')
            pass







#angeloIG.find_hashtag_and_collect_hrefs("funnyvideos")

#LOGIN
angeloIG = InstagramBot("snugglegiants", "BiggoDoggo")
angeloIG.login()
#TURN OFF NOTIFICATIONS
angeloIG.turnOffNotification()

#tags
data = ['greatdane', 'oldenglishsheepdog', 'russianterrier', 'puppiesofinstagram', 'puppylove'
               'alaskanmalamute','canecorso_worldwide','bigdoggos','doberman_pinschers','komondordog',
               'newfounlanddog','komondorsofinstagram','blackrussianterriers','blackterrier',
               'irishwolfhoundsofig','oldenglishsheepdogway','bordeauxdogue', 'neomastiff', 'bullmastiffofinstagram',
               'blackrussianterrier', 'irishwolfhoundsofinstagram','neopolitanmastiff','leonbergeroftheday',
               'doguedebordeauxlovers', 'malamuteofinstagram','bordeauxdogge','komondor','irishwolfhounds',
               'leonbergergram','canecorsorule', 'canecorsorule','greatdanemoments','rott','canecorsolovers',
               'mastiffgram','gentlegiant','greatdanelove','dobermanlove','irishwolfhound','k9unit','leonberger',
               'rottweilers_of_instagram','rottweilerworld','bernersofinstagram','greatdanelife','mastifflove',
               'alaskanhusky','newfoundlandsofinstagram','rotweiler','greatdanenation','bernerlove','dobermansofig',
               'malamuteaddicts','bernesemountaindogsofinstagram','canecorsomania','dobermanpinschers',
               'greatdanelovers','malamutelovers','bullmastiffs','gentlegiantsofinstagram','sheepie','mastiffofinstagram',
                'puppylove', 'ilovemydog', 'doggo', 'dogsofinstagram', 'instadog', 'dogs', 'petsofinstagram','pet',
                'doggy', 'doglife', 'dogstagram', 'bigdog', 'puppy', 'puppies', 'doglover']

data = list(set(data))
#ITERATE THROUGH EACH ROW AND ADD TO LIST
for tag in data[:]:

    now = datetime.datetime.now()
    if int(now.hour) > 8 and int(now.hour) < 23:
        angeloIG.like_photos_and_comments(tag=tag)
        print("WAITING FOR NEXT TAG")
        dt = datetime.datetime.now()
        add_hr = datetime.timedelta(hours=1)
        dt = dt + add_hr
        print("THE PROGRAM WILL BEGIN AT: ", dt)
        while datetime.datetime.now() < dt:
            time.sleep(60)

    else:
        time.sleep(60)