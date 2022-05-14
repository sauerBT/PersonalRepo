# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 16:40:38 2019

@author: brian
"""
def FindID(FHXInput, Array_Size):   
    #    Working copy of sect1 main text
    Working_Str = FHXInput
    i = 0
    ID_Array = [0]*int(Array_Size)
    # create an array of all ID numbers

    phrase1 = 'BATCH_PHASE_PARAMETER NAME="'
    phrase2 = 'ID='

    while True:            
        chop_index = Working_Str.find(phrase1)        
        if chop_index == -1:
            print('Exiting ID Finder\n')
            break
        chop_index = chop_index + len(phrase1) - 1
        Working_Str = Working_Str[chop_index + 1:]
        chop_index = Working_Str.find(phrase2)
        chop_index = chop_index + len(phrase2) - 1
        Working_Str = Working_Str[chop_index + 1:]
        chop_index = Working_Str.find('\n')    
        chop_sect_length = len(Working_Str)
        reverse_chop_index = chop_index - chop_sect_length
        ID = Working_Str[:reverse_chop_index]
        # ID = int(ID)
        ID_Array[i] = ID
        Working_Str = Working_Str[chop_index:]
        i += 1
    # Find the total number of recipe parameters
    Array_size = i
    # Remove excess variables from ID_Array
    ID_Array = ID_Array[0:Array_size]
    # Find the last entered recipe parameter ID number
    Current_ID = ID_Array[Array_size - 1]
    Descending_ID = list(map(int, ID_Array))
    Descending_ID.sort(reverse=True)
    Last_ID = Descending_ID[0]
    return (ID_Array, Array_size, Current_ID, Last_ID)


def FindRP(FHXInput, Array_size):
    # Working copy of sect1 main text
    Working_Str = FHXInput
    i = 0
    RP_Array = [' ']*Array_size
    # create an array of all Recipe Parameter 
    phrase1 = 'BATCH_PHASE_PARAMETER NAME="'
    while True:        
        chop_index = Working_Str.find(phrase1)        
        if chop_index == -1 and i == 0:
            Error_Sts = 'Recipe Parameter Finder Failed'
            i = 0
            break
        elif chop_index == -1 and i > 0:
            Error_Sts = 'Recipe Parameter Finder Complete'
            i = 0
            break
        chop_index = chop_index + len(phrase1) - 1
        Working_Str = Working_Str[chop_index + 1:]
        chop_index = Working_Str.find('"')
        chop_sect_length = len(Working_Str)
        reverse_chop_index = chop_index - chop_sect_length
        RP_Array[i] = Working_Str[:reverse_chop_index]
        Working_Str = Working_Str[chop_index:]
        i += 1
    return (RP_Array, Error_Sts)

def FindG(FHXInput, Array_size):
    Working_Str = FHXInput
    i = 0
    G_Array = [' ']*Array_size
    # create an array of all group values
    phrase1 = 'BATCH_PHASE_PARAMETER NAME="'
    phrase2 = 'GROUP="'
    while True:        
        chop_index = Working_Str.find(phrase1)        
        if chop_index == -1:
            print('Exiting Group Finder\n')
            break
        chop_index = chop_index + len(phrase1) - 1
        Working_Str = Working_Str[chop_index + 1:]
        chop_index = Working_Str.find(phrase2)
        chop_index = chop_index + len(phrase2) - 1
        Working_Str = Working_Str[chop_index + 1:]
        chop_index = Working_Str.find('"')    
        chop_sect_length = len(Working_Str)
        reverse_chop_index = chop_index - chop_sect_length
        GROUP = Working_Str[:reverse_chop_index]
        G_Array[i] = GROUP
        Working_Str = Working_Str[chop_index:]
        i += 1
    return G_Array

def FindD(FHXInput, Array_size):
    # Working copy of sect1 main text        
    Working_Str = FHXInput
    i = 0
    D_Array = [' ']*Array_size
    # create an array of all descriptions
    phrase1 = 'BATCH_PHASE_PARAMETER NAME="'
    phrase2 = 'DESCRIPTION="'
    while True:        
        chop_index = Working_Str.find(phrase1)        
        if chop_index == -1:
            print('Exiting Description Finder\n')
            break
        chop_index = chop_index + len(phrase1) - 1
        Working_Str = Working_Str[chop_index + 1:]
        chop_index = Working_Str.find(phrase2)
        chop_index = chop_index + len(phrase2) - 1
        Working_Str = Working_Str[chop_index + 1:]
        chop_index = Working_Str.find('"')    
        chop_sect_length = len(Working_Str)
        reverse_chop_index = chop_index - chop_sect_length
        D = Working_Str[:reverse_chop_index]
        D_Array[i] = D
        Working_Str = Working_Str[chop_index:]
        i += 1
    return D_Array