# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 11:46:46 2021

Webscape Ligainsider: Verletzungen und Sperren

@author: cm
"""

import requests                             # to get url
import pandas as pd                         # for dataframe
from bs4 import BeautifulSoup               # for Webscaping
from datetime import datetime, timedelta    # for timestamp
# import pickle                             # for saving and loading variables
import matplotlib.pyplot as plt
import numpy as np



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
    head =  TableContent.find('div') # 0th item is the header row
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
    del df["Marktwert-Trend"]
    
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
        
    df.insert(0,'Date',now)
    return df


#%%


url = 'https://www.ligainsider.de/bundesliga/verletzte-und-gesperrte-spieler/'

#%% make the soup8
response = requests.get(url)

page = response.content
#print(page)
soup = BeautifulSoup(page, 'html.parser')