# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 19:18:04 2020

Script to get the market values of all players from one club.

Template from: https://towardsdatascience.com/web-scraping-scraping-table-data-1665b6b2271c

Added to GitHub.

TODO:
    - Get daytime
    - Get trend
    - Find good data structure to make it plotable
    - Run script automatically
    - import points from matchday

@author: cm
"""

import requests                             # to get url
import pandas as pd                         # for dataframe
from bs4 import BeautifulSoup               # for Webscaping
from datetime import datetime, timedelta    # for timestamp
import pickle                               # for saving and loading variables

#%% Init
url = ["https://stats.comunio.de/squad/1-FC+Bayern+M%C3%BCnchen",
       "https://stats.comunio.de/squad/5-Borussia+Dortmund",
       "https://stats.comunio.de/squad/92-RB+Leipzig",
       "https://stats.comunio.de/squad/3-Borussia+M'gladbach",
       "https://stats.comunio.de/squad/8-Bayer+04+Leverkusen",
       "https://stats.comunio.de/squad/62-1899+Hoffenheim",
       "https://stats.comunio.de/squad/12-VfL+Wolfsburg",
       "https://stats.comunio.de/squad/21-SC+Freiburg",
       "https://stats.comunio.de/squad/9-Eintracht+Frankfurt",
       "https://stats.comunio.de/squad/7-Hertha+BSC",
       "https://stats.comunio.de/squad/109-1.+FC+Union+Berlin",
       "https://stats.comunio.de/squad/10-FC+Schalke+04",
       "https://stats.comunio.de/squad/18-1.+FSV+Mainz+05",
       "https://stats.comunio.de/squad/13-1.+FC+K%C3%B6ln",
       "https://stats.comunio.de/squad/68-FC+Augsburg",
       "https://stats.comunio.de/squad/6-SV+Werder+Bremen",
       "https://stats.comunio.de/squad/16-Arminia+Bielefeld",
       "https://stats.comunio.de/squad/14-VfB+Stuttgart"
       ]


def make_the_soup(url):
    response = requests.get(url)

    page = response.content
    #print(page)
    soup = BeautifulSoup(page, 'html.parser')
    return soup


def scrape_the_page(soup):
    # import the whole table
    TableContent = soup.find('table', {'class':'rangliste'})
    return TableContent
    
def get_the_headings(TableContent):
    # Lets now iterate through the head HTML code and make list of clean headings
    # Head values (Column names) are the first items of the body list
    head =  TableContent.find('thead') # 0th item is the header row
    # Declare empty list to keep Columns names
    headings = []
    for item in head.find_all("th"): # loop through all th elements
        # convert the th elements to text and strip "\n"
        heading = (item.text).rstrip("\n")
        # append the clean column name to headings
        headings.append(heading)
    # print(headings)
    return headings

def get_the_body(TableContent,all_rows):
    body = TableContent.find_all('tbody')
    body_rows = body[0].find_all('tr')
    # print(body_rows)
    
    # Next is now to loop though the rest of the rows
    for row_num in range(len(body_rows)): # A row at a time
        row = [] # this will old entries for one row
        for row_item in body_rows[row_num].find_all("td"): #loop through all row entries
            # row_item.text removes the tags from the entries
            # the following regex is to remove \xa0 and \n and comma from row_item.text
            # xa0 encodes the flag, \n is the newline and comma separates thousands in numbers
            aa = row_item.text
            #append aa to row - note one row entry is being appended
            row.append(aa)
        # append one row to all_rows
        all_rows.append(row)
    return all_rows

def create_dataframe(all_rows,headings,now):
    # We can now use the data on all_rowsa and headings to make a table
    # all_rows becomes our data and headings the column names
    df = pd.DataFrame(data=all_rows,columns=headings)
    df.head()
    
    # Dont need column "Auszeichnungen"
    del df["Auszeichnungen"]
    # Trend is empty hence also delete
    del df["Trend"]
    
    # Transform Marktwert to integer
    for i in range(0,len(df['Marktwert'])):
        string = df.loc[i,'Marktwert']
        #print(string)
        number = string.replace('.','')
        #print(number)
        integer = int(number)
        #print(integer)
        df.loc[i,'Marktwert'] = integer
    
    # Transform Punkte to integer
    for i in range(0,len(df['Pkt.'])):
        string = df.loc[i,'Pkt.']
        #print(string)
        number = string.replace('.','')
        #print(number)
        integer = int(number)
        #print(integer)
        df.loc[i,'Pkt.'] = integer
        
    df.insert(0,'Date',now.date())
    return df

#%% Main

# if __name__ == '__main__':
    
# Load the data
df_all = pd.read_csv('ClubScrape.csv')
    
# Compare time and from last update to now. 
# Load the last time 
last_time = pickle.load(open('timestamp','rb'))
# get the time now and safe it in timestamp to be last_time when script executed next time
now = datetime.now()
pickle.dump(now, open('timestamp','wb'))

# Comunio updates market value once per day
OneDay = timedelta(days=1)
TimePassed = now - last_time
if TimePassed >= OneDay: 

    all_rows = [] # will be a list for list for all rows
    for link in url:
        soup = make_the_soup(link)
        TableContent = scrape_the_page(soup)
        headings = get_the_headings(TableContent)
        all_rows = get_the_body(TableContent,all_rows)
        
    df_update = create_dataframe(all_rows, headings,now)
    
else:
    print('')
    print('Not a whole day passed. Until now only {0} passed'.format(TimePassed))


if 'df_update' in globals() or 'df' in locals():
    print('df in exists')
    df_all.append(df_update, ignore_index=True)
# Export dataframe
df_all.to_csv('ClubScrape.csv', index = None)


#%% Test

df = df_all
 
# # test list 
# data = [['tom', 'abw', '10',10000], ['nick', 'tor', '10',1000000015], ['juli', 'abw', '10',10000]] 
  
# # Create the pandas DataFrame 
# testframe = pd.DataFrame(data,columns=list(df.columns.values)) 

# newdf = df.append(testframe, ignore_index=True)

# insert a new column for daytime e.g.
# date = 'today'
# dateframe = newdf.insert(0,'Date',date)

# Search for items in list template
Tor_idx = df['Spieler'].str.contains('Lewandowski')
Tor = df[Tor_idx]

# # file= open('variable_dump','wb')
# # pickle.dump(['Tor'],  open('variable_dump','wb') )

# file= open('variable_dump','rb')
# d= pickle.load(open('variable_dump','rb'))
# print(d)
# d.append('abw')
# a='test'

# pickle.dump(d,  open('variable_dump','wb') )
# d= pickle.load(open('variable_dump','rb'))
# print(d)
