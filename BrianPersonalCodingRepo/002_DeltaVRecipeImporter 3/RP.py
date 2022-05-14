"""
Created on Fri Feb  1 18:30:26 2019

@author: bsauer
"""
def FindID(FHXInput, Array_Size):   
    #    Working copy of sect1 main text
    Working_Str = FHXInput
    print(Working_Str)
    i = 0
    ID_Array = [0]*Array_Size
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
    Last_ID = ID_Array[Array_size - 1]

    return (ID_Array,Last_ID)