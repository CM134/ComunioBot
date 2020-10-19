# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 21:38:09 2020

@author: cm
"""

import csv
import re
from io import StringIO
from pprint import pprint
from typing import IO

import requests
from bs4 import BeautifulSoup


def get_report_html():
    res = requests.post('https://classic.comunio.de/login.phtml', data={
        "login": "Mezzo",
        "pass": "chris134",
        "action": "login",
        ">>+Login": "-1"
    })
    res.raise_for_status()
    return res.text


def parse_exchange_details(soup: BeautifulSoup) -> list:
    name_els = soup.select('.article_content_text a')
    person_names = [a.text.strip() for a in name_els]

    exchanges = []

    persons = []
    action = None
    amount = None
    for s in soup.stripped_strings:
        if s in person_names:
            persons.append(s)

        # determine exchange direction
        if 'von Computer zu' in s:
            action = 'withdraw'
        elif 'zu Computer' in s:
            action = 'deposit'

        # look for numbers
        m = re.search('(\d[\d.]+)', s)
        if m:
            amount = m.group(1)

        # did we collect all exchange details
        if len(persons) == 2 and action and amount:
            p1, p2 = persons
            if action == 'deposit':
                from_, to = p2, 'computer'
            else:
                from_, to = 'computer', p2

            exc = {
                'who': p1,
                'amount': amount,
                'from': from_,
                'to': to
            }
            exchanges.append(exc)

            # reset for the next exchange
            persons = []
            action = None
            amount = None
    return exchanges

def write_csv(file: IO, report: list):
    fields = list(report[0].keys())
    w = csv.DictWriter(file, fieldnames=fields)
    for item in report:
        w.writerow(item)

if __name__ == '__main__':
    html = '''
<div class="article_content2">
 <div class="article_content_text">
  <a>B. Hübner</a> wechselt für 3.711.638 von Computer zu <a>Marcel</a> .
  <br/>
  <a>Ginczek</a> wechselt für 2.845.000 von Computer zu <a>Max</a> .
  <br/>
  <a>Embolo</a> wechselt für 6.640.000 von Computer zu <a>Chrissi</a> .
  <br/>
  <br/>
  <a>Jäkel</a> wechselt für 220.000 von <a>Thilo</a> zu Computer.
  <br/>
  <a>Raphaël Guerreiro</a> wechselt für 3.640.000 von <a>Malte</a> zu Computer.
  <br/>
  <br/>
 </div>
</div>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    exchanges = parse_exchange_details(soup)
    pprint(exchanges, width=200)

    file = StringIO()
    # or `with open('filename.csv', 'w') as file:` 
    write_csv(file, exchanges)
    file.seek(0)
    print(file.read())