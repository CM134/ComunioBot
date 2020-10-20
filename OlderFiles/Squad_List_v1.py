# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 19:18:04 2020

Script to get the market values of all players from one club

@author: cm
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

#%% Get the page

#url = "https://stats.comunio.de/squad/1-FC+Bayern+M%C3%BCnchen"
url = "https://stats.comunio.de/squad/5-Borussia+Dortmund"
response = requests.get(url)

page = response.content

print(page)

#%% Start working with data
soup = BeautifulSoup(page, 'html.parser')


# import the whole table

TableContent = soup.find('table', {'class':'rangliste'})
print('important Content:')
#print(TableContent)

body = TableContent.find_all('tbody')
body_rows = body[0].find_all('tr')
print(body_rows)

# Head values (Column names) are the first items of the body list
head =  TableContent.find('thead') # 0th item is the header row

# Lets now iterate through the head HTML code and make list of clean headings

# Declare empty list to keep Columns names
headings = []
for item in head.find_all("th"): # loop through all th elements
    # convert the th elements to text and strip "\n"
    heading = (item.text).rstrip("\n")
    # append the clean column name to headings
    headings.append(heading)
print(headings)

# Next is now to loop though the rest of the rows

all_rows = [] # will be a list for list for all rows
for row_num in range(len(body_rows)): # A row at a time
    row = [] # this will old entries for one row
    for row_item in body_rows[row_num].find_all("td"): #loop through all row entries
        # row_item.text removes the tags from the entries
        # the following regex is to remove \xa0 and \n and comma from row_item.text
        # xa0 encodes the flag, \n is the newline and comma separates thousands in numbers
        aa = re.sub("(\xa0)|(\n)|,","",row_item.text)
        #append aa to row - note one row entry is being appended
        row.append(aa)
    # append one row to all_rows
    all_rows.append(row)


# We can now use the data on all_rowsa and headings to make a table
# all_rows becomes our data and headings the column names
df = pd.DataFrame(data=all_rows,columns=headings)
df.head()

# Dont need column "Auszeichnungen"
del df["Auszeichnungen"]
# Trend is empty hence also delete
del df["Trend"]


#%%
# get player names
Players = TableContent.find_all('a', attrs={'class':'playerName nowrap'})
print()
print('Players:')
#print(Players)

for span in Players:
    print(span.string)
    
# get market value
MarketValue = TableContent.find_all('span', attrs={'class':'abbr nowrap'})
print()
print('Prize:')
#print(Prize)

for span in MarketValue:
    print(span.string)


# get position
# Position =