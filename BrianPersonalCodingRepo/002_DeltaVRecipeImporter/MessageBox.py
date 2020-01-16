# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 06:36:49 2019

@author: brian
"""
import ctypes  # An included library with Python install.
def MSGB(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)
