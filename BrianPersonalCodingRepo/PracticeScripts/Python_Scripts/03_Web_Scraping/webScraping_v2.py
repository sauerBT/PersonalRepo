# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 14:02:03 2019

@author: brian
"""
#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
import ast
import os
from urllib.request import Request, urlopen

# For ignoring SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Input from the user
url = input('Enter Yahoo Finance Company Url- ')
# Making the website believe that you are accessing it using a Mozilla browser
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
# Creating a BeautifulSoup object of the HTML page for easy extraction of data.

soup = BeautifulSoup(webpage, 'html.parser')
html = soup.prettify('utf-8')
company_json = {}
other_details = {}
for span in soup.findAll('span',
                         attrs={'class': 'Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)'
                         }):
    company_json['PRESENT_VALUE'] = span.text.strip()
for div in soup.findAll('div', attrs={'class': 'D(ib) Va(t)'}):
    for span in div.findAll('span', recursive=False):
        company_json['PRESENT_GROWTH'] = span.text.strip()
for td in soup.findAll('td', attrs={'data-test': 'PREV_CLOSE-value'}):
    for span in td.findAll('span', recursive=False):
        other_details['PREV_CLOSE'] = span.text.strip()
for td in soup.findAll('td', attrs={'data-test': 'OPEN-value'}):
    for span in td.findAll('span', recursive=False):
        other_details['OPEN'] = span.text.strip()
for td in soup.findAll('td', attrs={'data-test': 'BID-value'}):
    for span in td.findAll('span', recursive=False):
        other_details['BID'] = span.text.strip()
for td in soup.findAll('td', attrs={'data-test': 'ASK-value'}):
    for span in td.findAll('span', recursive=False):
        other_details['ASK'] = span.text.strip()
for td in soup.findAll('td', attrs={'data-test': 'DAYS_RANGE-value'}):
    for span in td.findAll('span', recursive=False):
        other_details['DAYS_RANGE'] = span.text.strip()
for td in soup.findAll('td',
                       attrs={'data-test': 'FIFTY_TWO_WK_RANGE-value'}):
    for span in td.findAll('span', recursive=False):
        other_details['FIFTY_TWO_WK_RANGE'] = span.text.strip()
for td in soup.findAll('td', attrs={'data-test': 'TD_VOLUME-value'}):
    for span in td.findAll('span', recursive=False):
        other_details['TD_VOLUME'] = span.text.strip()
for td in soup.findAll('td',
                       attrs={'data-test': 'AVERAGE_VOLUME_3MONTH-value'
                       }):
    for span in td.findAll('span', recursive=False):
        other_details['AVERAGE_VOLUME_3MONTH'] = span.text.strip()
for td in soup.findAll('td', attrs={'data-test': 'MARKET_CAP-value'}):
    for span in td.findAll('span', recursive=False):
        other_details['MARKET_CAP'] = span.text.strip()
for td in soup.findAll('td', attrs={'data-test': 'BETA_3Y-value'}):
    for span in td.findAll('span', recursive=False):
        other_details['BETA_3Y'] = span.text.strip()
for td in soup.findAll('td', attrs={'data-test': 'PE_RATIO-value'}):
    for span in td.findAll('span', recursive=False):
        other_details['PE_RATIO'] = span.text.strip()
for td in soup.findAll('td', attrs={'data-test': 'EPS_RATIO-value'}):
    for span in td.findAll('span', recursive=False):
        other_details['EPS_RATIO'] = span.text.strip()
for td in soup.findAll('td', attrs={'data-test': 'EARNINGS_DATE-value'
                       }):
    other_details['EARNINGS_DATE'] = []
    for span in td.findAll('span', recursive=False):
        other_details['EARNINGS_DATE'].append(span.text.strip())
for td in soup.findAll('td',
                       attrs={'data-test': 'DIVIDEND_AND_YIELD-value'}):
    other_details['DIVIDEND_AND_YIELD'] = td.text.strip()
for td in soup.findAll('td',
                       attrs={'data-test': 'EX_DIVIDEND_DATE-value'}):
    for span in td.findAll('span', recursive=False):
        other_details['EX_DIVIDEND_DATE'] = span.text.strip()
for td in soup.findAll('td',
                       attrs={'data-test': 'ONE_YEAR_TARGET_PRICE-value'
                       }):
    for span in td.findAll('span', recursive=False):
        other_details['ONE_YEAR_TARGET_PRICE'] = span.text.strip()
company_json['OTHER_DETAILS'] = other_details
with open('data.json', 'w') as outfile:
    json.dump(company_json, outfile, indent=4)
print(company_json)
with open('output_file.html', 'wb') as file:
    file.write(html)
print('----------Extraction of data is complete. Check json file.----------')