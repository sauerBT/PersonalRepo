# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 14:02:03 2019

@author: brian
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://finance.yahoo.com/quote/VTIAX/history?p=VTIAX"
html = urlopen(url)
soup = BeautifulSoup(html,"html.parser")
type(soup)
#bs4.BeautifulSoup
title = soup.title
print(title)
text = soup.get_text()
# print(text)
rows = soup.find_all('tr')
for row in rows:
    row_td = row.find_all('td')
print(row_td)
type(row_td)
str_cells = str(row_td)
cleantext = BeautifulSoup(str_cells, "lxml").get_text()
print(cleantext)