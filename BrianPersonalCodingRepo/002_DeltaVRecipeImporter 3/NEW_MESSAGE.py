# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 19:01:29 2019

@author: bsauer
"""
import ctypes  # An included library with Python install.
def MSGB(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)
