# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 06:41:04 2019

File to test importing of CSV Files

@author: brian



04-Jan-2019 09:59:21


21-Feb-2013 06:35:45
"""
def FMTDate()
    import datetime
    import time
    import math

    format = "%d-%b-%Y %H:%M:%S"
    today = datetime.datetime.today()
    s = today.strftime(format)
    seconds = time.time()
    Current_Time_EP = (math.trunc(seconds))
    return (s, Current_Time_EP)