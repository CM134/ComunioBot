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

def Ligainsider():
    url = 'https://www.ligainsider.de/bundesliga/verletzte-und-gesperrte-spieler/'
    
    # scrape 
    soup = make_the_soup(url)
    
    # import the whole table
    maincontainer = soup.find(id = 'main_container' )
    
    #extract clubs
    club_container = maincontainer.find_all('div', class_ = 'personal_table personal_table_top')
    
    # print('There are', len(club_container), 'clubs')
    
    # get all information
    
    
    headings = ['Player', 'Club', 'Reason', 'Explanation', 'Missing since']
    
    all_rows = np.asarray(headings).reshape(1,-1)
    
    for club in club_container:
    
        # get club name
        
        clubname = club.h2.text
        
        # get all players of club
        
        player_container = club.find_all('div', class_ = 'small_table_row')
        # print('There are', len(player_container), 'players for club', clubname)
        
        if player_container[0].div.span.text == 'Derzeit keine verletzten oder gesperrten Spieler':
            continue
        
        for player in player_container:
            playername = player.strong.text
            
            reason_type = player.div.find('img')['alt']
            
            reason_text = player.find('div', class_ ='small_table_column2' ).span.text

            missing_since = player.find('div', class_ ='small_table_column4' ).span.text

            row = [playername,clubname,reason_type,reason_text,missing_since]

            row = np.asarray(row).reshape(1,-1)
            all_rows = np.append(all_rows, row, axis = 0)
                
        
    # create dataframe
    df_LigaInsider = pd.DataFrame(data=all_rows[1:,:],columns=headings)
    
    return df_LigaInsider
    

#%%


url = 'https://www.ligainsider.de/bundesliga/verletzte-und-gesperrte-spieler/'

#%% make the soup8

soup = make_the_soup(url)



#%% Start working with data

# import the whole table
maincontainer = soup.find(id = 'main_container' )



#%% extract clubs


club_container = maincontainer.find_all('div', class_ = 'personal_table personal_table_top')

# print('There are', len(club_container), 'clubs')

# get all information


headings = ['Player', 'Club', 'Reason', 'Explanation', 'Missing since']

all_rows = np.asarray(headings).reshape(1,-1)

for club in club_container:

    # get club name
    
    clubname = club.h2.text
    
    # get all players of club
    
    player_container = club.find_all('div', class_ = 'small_table_row')
    # print('There are', len(player_container), 'players for club', clubname)
    
    if player_container[0].div.span.text == 'Derzeit keine verletzten oder gesperrten Spieler':
        continue
    
    for player in player_container:
        # try:
        playername = player.strong.text
        # print(playername)
        
        reason_type = player.div.find('img')['alt']
        #row.append(reason_type)
        # print(reason_type)
        
        reason_text = player.find('div', class_ ='small_table_column2' ).span.text
        
        # print(reason_text)
        
        missing_since = player.find('div', class_ ='small_table_column4' ).span.text
        # print(missing_since)
        
        
        row = [playername,clubname,reason_type,reason_text,missing_since]
        # print(row)
            
        # except:
        #     print('No data imported for')            
        #     continue
        
        row = np.asarray(row).reshape(1,-1)
        all_rows = np.append(all_rows, row, axis = 0)
            
    
# create dataframe
df_LigaInsider = pd.DataFrame(data=all_rows[1:,:],columns=headings)


#%%

ret = Ligainsider()