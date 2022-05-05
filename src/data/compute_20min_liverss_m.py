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

# Computing the newly aquired articles -> not used up to now (04.05.2022)
articles_to_keep = []
for entry in feed.entries:
    entry_date = pd.to_datetime(entry.published)
    #print(f"Entry date : {entry_date}")
    articles_to_keep.append(entry)
print(f"New articles in feed since last check : {len(articles_to_keep)}")

# Compute a Pandas dataframe to write into 20min initialdataset
liverss_df = pd.DataFrame.from_dict(articles_to_keep, orient='columns')
liverss_df['published'] = pd.to_datetime(liverss_df['published'])

# Saving generated data to raw data folder
liverss_df.to_csv(r'~/SocialMediaMonitor/data/raw/liverss_20min.csv', index = False)