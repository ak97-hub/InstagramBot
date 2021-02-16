'''
This program directly converts the source url into mp4 or jpg and
downloads directly to desktop to be later re-uploaded/reposted.
'''

import requests
from csv import reader
import pandas as pd

#ACTUAL VIDEO DOWNLOADER
def video_downloader(href, ig_name, breed, row_num):
    chunk_size = 256

    r = requests.get(href, stream=True)
    full_path = ig_name + "-" + breed + "-" + str(row_num)
    with open("/Users/AngeloKhan/Desktop/Downloaded_Content/Videos/{}".format(full_path) + ".mp4", "wb") as f:

        for chunk in r.iter_content(chunk_size = chunk_size):
            f.write(chunk)

#ACTUAL PHOTO DOWNLOADER
def image_downloader(href, ig_name, breed, row_num):

        r = requests.get(href).content
        #combine ig_name & breed
        full_path = ig_name + "-" + breed + "-" + str(row_num)
        with open("/Users/AngeloKhan/Desktop/Downloaded_Content/Images/{}".format(full_path) +'.jpg', 'wb') as handler:
         handler.write(r)

#OPENS FILE, ITERATES THROUGH EACH HREF, THEN USES ABOVE PROGRAM TO SAVE
def parent_downloader(filename):
    # open file in read mode
    with open('/Users/AngeloKhan/Desktop/{}'.format(filename), 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        row_num = 0
        for row in csv_reader:

            # row variable is a list that represents a row in csv
            href = row[0]
            #strip href of unnecessary characters
            href = href.replace(']', '').replace('[','').replace("'", "")
            head, sep, tail = href.partition(",")
            href = head
            #Specify each column for each row
            breed = row[1]
            acct = row[2]
            media_type = row[3]

            if media_type == 'Videos':
                print("Here is the Video: " + breed, acct, href)
                video_downloader(href=href, breed=breed, ig_name=acct, row_num=row_num)

            elif media_type == 'Photo':
                print("Here is the Photo: " + breed, acct, href)
                image_downloader(href=href, breed=breed, ig_name=acct, row_num=row_num)

            else:
                pass

            #UNIQUE ROW NUMBER TO ASSIGN TO EACH FILENAME
            row_num += 1

def remove_duplicates(filename):
    # making data frame from csv file
    data = pd.read_csv("/Users/AngeloKhan/Desktop/{}".format(filename))

    # dropping ALL duplicte values
    data = data.drop_duplicates(subset="Href",
                                keep="first")

    # saving data
    data.to_csv("/Users/AngeloKhan/Desktop/{}".format(filename), sep=',', index=False)
    print("Duplicates removed for {}".format(filename))



#ACTIVATE PROGRAM
filepath = "Downloadable_Monthly_Content_Final.csv"
remove_duplicates(filename=filepath)
parent_downloader(filename=filepath)
