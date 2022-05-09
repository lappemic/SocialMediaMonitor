"""
Get the new articles of 20 minuten
using their rss feed.
Articles are considered as new if published after the last check date
"""
import pandas as pd
import numpy as np
import feedparser
import datetime

# Get the RSS feed
url = 'https://partner-feeds.20min.ch/rss/20minuten/zentralschweiz'
feed = feedparser.parse(url)
print(f"Articles in feed : {len(feed.entries)}")

# Get last check date from global last_check_articles_20min

# Computing the newly aquired articles -> not used up to now (04.05.2022)
articles_to_keep = []
for entry in feed.entries:
    entry_date = pd.to_datetime(entry.published)
    if last_check_articles_20min < entry_date:
        articles_to_keep.append(entry)
print(f"New articles in feed since last check : {len(articles_to_keep)}")

# Compute temporary Pandas dataframe to further process beneath
liverss_tmp_df = pd.DataFrame.from_dict(articles_to_keep, orient='columns')
liverss_tmp_df['published'] = pd.to_datetime(liverss_tmp_df['published'])
liverss_tmp_df.head()

# Cleaning created dataframe of 20min liverss_tmp_df
liverss_df = pd.DataFrame()
liverss_df['title'] = liverss_tmp_df['title']
liverss_df['summary'] = liverss_tmp_df['summary']
liverss_df['link'] = liverss_tmp_df['link']
liverss_df['id'] = liverss_tmp_df['id'].str[-12:]
liverss_df['published'] = liverss_tmp_df['published']
liverss_df['published_parsed'] = liverss_tmp_df['published_parsed']
liverss_df.head()

# Saving generated data to raw data folder
liverss_df.to_csv(r'~/Desktop/SocialMediaMonitor/data/raw/liverss_20Min.csv', index = False)