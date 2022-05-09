# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import pandas as pd, numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ChromeOptions
from datetime import timedelta
import math
import time

'''
Computing the comments for 20 minutes of the liverss news
'''

# get the date of the moste recent article in the merged dataset
liverss_and_coms_path = pathlib.Path.home() / 'SocialMediaMonitor' / 'data' / 'raw' / 'liverss_and_coms_20min.csv'
liverss_and_coms_df = pd.read_csv(liverss_and_coms_path)
liverss_and_coms_df['published'] = pd.to_datetime(liverss_and_coms_df['published'])
most_recent_article = liverss_and_coms_df['published'].max()

# get the ids of the articles that are less than 15 days old
recent_date = pd.to_datetime(most_recent_article-timedelta(15), utc=True)
mask = (liverss_and_coms_df['published'] > recent_date) # & (total_df['is_com_or_sub'] == 'sub')
recent_articles = liverss_and_coms_df.loc[mask]
recent_articles_id = recent_articles['id'].tolist()
#print(recent_articles_id[:3])
print(len(recent_articles_id))

# Configure the Chrome webdriver
driver = webdriver.Chrome('/users/michaellappert/Downloads/chromedriver') # Needs to be adjusted client independently



# get the commenents of those articles
new_coms_df = pd.DataFrame(columns = ['author', 'published', 'summary', 'is_com_or_sub', 'link'])

for article_id in recent_articles_id:
    # print(article)
    url = 'https://www.20min.ch/comment/'
    comments_url = url + str(article_id)
    # print(comments_url)
    driver.get(comments_url)
    
    # scroll to load entire page (uses lazy loading)
    check_height = driver.execute_script('return document.body.scrollHeight;')
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        height = driver.execute_script("return document.body.scrollHeight;") 
        if height == check_height: 
            break 
        check_height = height
    
    # get authors
    authors = driver.find_elements_by_class_name('CommentCard_authorNickname__booTY')
    # print(authors)
    author_list = [author.get_attribute('innerHTML') for author in authors]
    # print(author_list)

    # get publication dates
    published_date = driver.find_elements_by_class_name('CommentCard_createdAt__LxEL2')
    # print(published_date)
    date_list = [pd.to_datetime(date.get_attribute('innerHTML'), format = '%d.%m.%Y, %H:%M', utc = True) for date in published_date]
    # print(len(date_list))
    # print(date_list)
    
    # get text bodys
    bodys = driver.find_elements_by_class_name("CommentCard_body__KWmXR")
    # print(bodys)
    body_list = [body.get_attribute('innerHTML') for body in bodys]
    # print(body_list)
    
    # assesrt to make sure that we have all the data for every com
    # may fail if the webdriver didn't wait for the page to load
    assert len(body_list) == len(date_list) == len(author_list), "Assertion problem, probably due to page parsing before page is fully loaded"
    
    # create a temporary dataframe with the data and write it to the new_coms_df
    temp_df = pd.DataFrame(list(zip(author_list, date_list, body_list)), columns =['author', 'published', 'summary'])
    # print(temp_df)
    temp_df['id'] = article_id
    # temp_df.head()
    temp_df['is_com_or_sub'] = 'com'
    # print(temp_df.head())
    # time.sleep(2)
    temp_df['link'] = comments_url
    # print(temp_df.head())
    # time.sleep(2)
    # temp_df = temp_df[temp_df['published'] > last_com_check] # -> GLOBAL VARIABLE FOR LAST_COM_CHECK MUST BE INCLUDED
    print(f'Article {comments_url} has {len(temp_df)} comments')
    if len(temp_df) >0:
        new_coms_df = pd.concat([new_coms_df, temp_df], ignore_index=True, axis=0)

# new_coms_df.head()
driver.quit()

# get latest coms check date
if len(new_coms_df) > 0:
    new_last_check_coms = new_coms_df['published'].max()


# Saving the gotten coms to a csv file
liverss_comments_df = new_coms_df # For this sample code, simply copy input to output

# Saving generated data to raw data folder
liverss_comments_df.to_csv(r'~/Desktop/SocialMediaMonitor/data/raw/liverss_comments_20Min.csv', index = False)