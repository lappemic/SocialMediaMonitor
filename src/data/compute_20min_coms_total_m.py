import pandas as pd
import numpy as np
import csv
import pathlib

# Importing the config file
import sys
sys.path.append('~/SocialMediaMonitor/src')
import config

'''
Append the new articels of 20min to the logged articles
and update the last_check_articles_20min variable
'''

# Reading the newly aquired articles in the temporary csv
liverss_path = pathlib.Path.home() / 'SocialMediaMonitor' / 'data' / 'raw' / 'liverss_20min.csv'
liverss_csv = open(liverss_path, 'r', newline = '')
liverss_obj = csv.reader(liverss_csv)

# Reading the log csv of articles and coms file and write the new articles to it
liverss_and_coms_path = pathlib.Path.home() / 'SocialMediaMonitor' / 'data' / 'raw' / 'liverss_and_coms_20min.csv'
liverss_and_coms_csv = open(liverss_and_coms_path, 'w', newline = '')
liverss_and_coms_obj = csv.writer(liverss_and_coms_csv)
liverss_and_coms_obj.writerows(liverss_obj)
liverss_and_coms_csv.close()

# Reading the newly enriched log csv and updating the last_check_articles_20min
liverss_and_coms_path = pathlib.Path.home() / 'SocialMediaMonitor' / 'data' / 'raw' / 'liverss_and_coms_20min.csv'
liverss_and_coms_df = pd.read_csv(liverss_and_coms_path)
last_check_articles_20min = liverss_and_coms_df['published'].max()
