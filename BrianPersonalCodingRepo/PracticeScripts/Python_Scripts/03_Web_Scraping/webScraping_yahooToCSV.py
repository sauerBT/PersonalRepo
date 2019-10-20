import yfinance as yf

import pandas as pd  

import re
 
msft = yf.Ticker("MSFT")
print(msft)
yahooMSFTHistorical = msft.history(period="max")
OpenType = type(yahooMSFTHistorical["Open"])
Open = yahooMSFTHistorical["Open"].toList()