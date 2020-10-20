# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 19:55:50 2020

This script tries to scape content from stats.comunio.de

@author: cm
"""

import requests


from bs4 import BeautifulSoup

#%% Get the page

url = "https://stats.comunio.de/"
response = requests.get(url)

page = response.content

# print(page)


#%% Start working with data
soup = BeautifulSoup(page, 'html.parser')


# get player name

importantContent = soup.find('table', {'class':'playersTable stretch autoColor'})
print('important Content:')
print(importantContent)

Players = importantContent.find_all('a', attrs={'class':'playerName nowrap'})
print()
print('Players:')
#print(Players)

for span in Players:
    print(span.string)

Prize = importantContent.find_all('span', attrs={'class':'abbr nowrap'})
print()
print('Prize:')
#print(Prize)

for span in Prize:
    print(span.string)