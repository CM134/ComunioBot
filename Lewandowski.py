# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 21:30:25 2020

Only for the Lewa page:https://classic.comunio.de/bundesligaspieler/31663-Lewandowski.html


@author: cm
"""

import requests

from bs4 import BeautifulSoup

url = "https://stats.comunio.de/"
response = requests.get(url)

page = response.content

# start soup
soup = BeautifulSoup(page, 'html.parser')

table = soup.find('table',attrs={'class':'tablecontent03'})
print(table)
