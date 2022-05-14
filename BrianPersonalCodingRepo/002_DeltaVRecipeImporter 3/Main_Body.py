# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 14:59:36 2019

@author: bsauer
"""
from MessageBox import MSGB # Import the message box function
from tkinter.filedialog import askopenfilename  # Import file explorer 
from RP_Op import FindID, FindRP, FindG, FindD
from RP_Update import RPImport, RPDateUpdate
from FHXFMTDateTime import FMTDate
"""
Prompt user to browse for phase FHX file that will be used 
"""
filename = askopenfilename()
"""
Open the file that was browsed and save the text within the file
"""

file = open(filename, 'r', encoding="utf16"); main_text = file.read(); file.close()


# find beginning and end indices for recipe parameter section 1
chop1_index1 = main_text.find('BATCH_EQUIPMENT_PHASE_CLASS NAME')
chop1_index2 = main_text.find('PHASE_CLASS_ALGORITHM NAME')
# generate section 1 text parameter
RP_sect1 = main_text[chop1_index1:chop1_index2 - 1]


# Find all recipe parameter IDs
[ID_Array, Array_size, Current_ID, Last_ID] = FindID(RP_sect1, 99)
# Find all recipe parameter names
[RP_Array, Error_Sts] = FindRP(RP_sect1, Array_size)
# Find all recipe parameter groups
G_Array = FindG(RP_sect1, Array_size)
# Find all recipe parameter descriptions
D_Array = FindD(RP_sect1, Array_size)

"""
Import recipe parameter section
"""
# Prompt user decide whether to import new recipe parameters or to exit program
initialize_import = input('Add a new recipe parameter? (Y/N)')
# Set prompt input to lower case to make it easier to match inputs
initialize_import = initialize_import.lower()
if initialize_import ==  'y':
    [FMTTime, EpochTime] = FMTDate()
    Updated_Main_Text = RPImport(main_text, Last_ID, RP_Array, Array_size)
    [Updated_Main_Text, OldEpochTime, New_time] = RPDateUpdate(Updated_Main_Text, EpochTime, FMTTime)
else:
    print("Exiting program")