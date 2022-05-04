# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
"""
Get the new articles of 20 minuten
using their rss feed.
Articles are considered as new if published after the last check date
"""
# import dataiku
import pandas as pd
import numpy as np
# from dataiku import pandasutils as pdu
import feedparser
import datetime

# Get feed
feed = feedparser.parse('https://partner-feeds.20min.ch/rss/20minuten/zentralschweiz')
print(f"Articles in feed : {len(feed.entries)}")

# Get last check date from dataiku global varialbles, and convert to date object
last_check_date = dataiku.get_custom_variables()["20min_last_check_subs"]
last_datetime = pd.to_datetime(last_check_date)
print(last_datetime)

articles_to_keep = []
# keep only articles published after last check
for entry in feed.entries:
    entry_date = pd.to_datetime(entry.published)
    print(f"Entry date : {entry_date}")
    if last_datetime < entry_date:
        articles_to_keep.append(entry)
print(f"New articles in feed since last check : {len(articles_to_keep)}")

# Compute a Pandas dataframe to write into luzern-zeitung-initialdataset
liverss_df = pd.DataFrame.from_dict(articles_to_keep, orient='columns')
liverss_df['published'] = pd.to_datetime(liverss_df['published'])

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Write recipe outputs
liverss = dataiku.Dataset("20min_liverss")
liverss.write_with_schema(liverss_df)