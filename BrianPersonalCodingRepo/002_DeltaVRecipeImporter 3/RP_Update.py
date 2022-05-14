# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 18:16:43 2019

@author: brian
"""
def RPImport(main_text, Last_ID, RP_Array, Array_size):
    ## import and activate file containing new recipe parameters (To Be Completed Later)
    #import_file = notepad.prompt('Enter file name(MUST BE A DELIMINATED TEXT FILE)')
    #import_file = import_file.lower()
    # initialize the incrementing index logic
    # Section 1 incrementing index logic initialize
    incrementing_index_sect1 = 0
    incrementing_index_sect1 = main_text.find('BATCH_EQUIPMENT_PHASE_CLASS NAME')
    # Section 2 incrementing index logic initialize
    incrementing_index_sect2 = 0
    incrementing_index_sect2 = main_text.find('BATCH_EQUIPMENT_PHASE_CLASS NAME')
    # Section 3 incrementing index logic initialize
    incrementing_index_sect3 = 0
    incrementing_index_sect3 = main_text.find('BATCH_EQUIPMENT_PHASE_CLASS NAME')
    incrementing_index_sect3 = main_text.find('PHASE_CLASS_ALGORITHM NAME',incrementing_index_sect3)
    incrementing_index_sect3 = main_text.find('ATTRIBUTE NAME="',incrementing_index_sect3)
    # Section 4 incrementing index logic initialize
    incrementing_index_sect4 = 0
    incrementing_index_sect4 = main_text.find('BATCH_EQUIPMENT_PHASE_CLASS NAME')
    incrementing_index_sect4 = main_text.find('PHASE_CLASS_ALGORITHM NAME',incrementing_index_sect4)
    incrementing_index_sect4 = main_text.find('ATTRIBUTE NAME="',incrementing_index_sect4)
    incrementing_index_sect4 = main_text.find('ATTRIBUTE_INSTANCE NAME="',incrementing_index_sect4)
    
    main_text.find('PHASE_CLASS_ALGORITHM NAME')
    # Find the index where the section 1 of recipe parameters will be imported
    incrementing_index_sect1 = main_text.find('BATCH_PHASE_PARAMETER NAME="', incrementing_index_sect1)
    Last_ID_String_Index = 'ID=' + str(Last_ID)
    incrementing_index_sect1 = main_text.find(Last_ID_String_Index, incrementing_index_sect1)
    Sect1_End_String = '}\n'
    Sect1_End_Len = len(Sect1_End_String)
    incrementing_index_sect1 = main_text.find(Sect1_End_String, incrementing_index_sect1)
    incrementing_index_sect1 = incrementing_index_sect1 + Sect1_End_Len
    # Find the index where the section 2 of recipe parameters will be imported
    Sect2_RP_String = 'ATTRIBUTE_INSTANCE NAME="%s"' % (RP_Array[Array_size - 1])
    Sect2_End_String = '}\n    }\n'
    Sect2_End_Len = len(Sect2_End_String)
    incrementing_index_sect2 = main_text.find(Sect2_RP_String, incrementing_index_sect2)
    incrementing_index_sect2 = main_text.find(Sect2_End_String, incrementing_index_sect2)
    incrementing_index_sect2 = incrementing_index_sect2 + Sect2_End_Len
    # Find the index where the section 3 of recipe parameters will be imported
    Sect3_RP_String = 'ATTRIBUTE NAME="%s"' % ((RP_Array[Array_size - 1]))
    Sect3_End_String = '\n    }\n'
    Sect3_End_Len = len(Sect3_End_String)
    incrementing_index_sect3 = main_text.find(Sect3_RP_String,incrementing_index_sect3)
    incrementing_index_sect3 = main_text.find(Sect3_End_String,incrementing_index_sect3)
    incrementing_index_sect3 = incrementing_index_sect3 + Sect3_End_Len
    # Find the index where the section 4 of recipe parameters will be imported
    Sect4_RP_String = 'ATTRIBUTE_INSTANCE NAME="%s"' % ((RP_Array[Array_size - 1]))
    Sect4_End_String = '\n    }\n'
    Sect4_End_Len = len(Sect4_End_String)
    incrementing_index_sect4 = main_text.find(Sect4_RP_String, incrementing_index_sect4)
    incrementing_index_sect4 = main_text.find(Sect4_End_String, incrementing_index_sect4)
    incrementing_index_sect4 = incrementing_index_sect4 + Sect4_End_Len
    #Specify Recipe Parameter configuration information (to be improved later)
    Recipe_Parameter_Name = 'R_BRIAN_PARAM'
    Recipe_Parameter_Type = 'STRING'
    new_Last_ID = int(Last_ID) + 1
    Recipe_Parameter_ID = new_Last_ID
    Last_ID = str(new_Last_ID)
    Recipe_Parameter_Group = ''
    Recipe_Parameter_Description = 'Declan is gonna lose this bet'
    Recipe_Parameter_HI = '1234'
    Recipe_Parameter_LO = '12'
    Recipe_Parameter_Default = '111'
    Recipe_Parameter_Units = 'kg'
    Recipe_Parameter_Set = ''
    Recipe_Parameter_Set_Value = ''
    #Generate the strings to be imported into the FHX file
    #Section 1 string generation
    if Recipe_Parameter_Type == 'REAL':
        TYPE = 'BATCH_PARAMETER_REAL'
    elif Recipe_Parameter_Type == 'INTEGER':
        TYPE = 'BATCH_PARAMETER_INTEGER'
    elif Recipe_Parameter_Type == 'STRING':
        TYPE = 'UNICODE_STRING'
    elif Recipe_Parameter_Type == 'NAMEDSET':
        TYPE = 'ENUMERATION_VALUE'
    Sect1_Entry_Part1 = '    BATCH_PHASE_PARAMETER NAME="%s" TYPE=%s DIRECTION=INPUT\n' % (Recipe_Parameter_Name,TYPE)
    Sect1_Entry_Part2 = '    {\n      ID=%s\n      GROUP="%s"\n      DESCRIPTION="%s"\n    }\n' % (Recipe_Parameter_ID, Recipe_Parameter_Group, Recipe_Parameter_Description)
    Sect1_Entry = Sect1_Entry_Part1 + Sect1_Entry_Part2
    print(Sect1_Entry)
    #Section 2 string generation
    Sect2_Entry_Part1 = '    ATTRIBUTE_INSTANCE NAME="%s"\n    {\n      VALUE' % (Recipe_Parameter_Name)
    #Section 2 Part 2 String is dependent on the type of recipe parameter entered
    if Recipe_Parameter_Type == 'REAL':
        Sect2_Entry_Part2 =  ' { DESCRIPTION="" HIGH=%s LOW=%s SCALABLE=F CV=%s UNITS="%s" }\n    }\n' % (Recipe_Parameter_HI, Recipe_Parameter_LO, Recipe_Parameter_Default, Recipe_Parameter_Units)
    elif Recipe_Parameter_Type == 'INTEGER':
        Sect2_Entry_Part2 = ' { DESCRIPTION="" HIGH=%s LOW=%s SCALABLE=F CV=%s UNITS="%s" }\n    }\n' % (Recipe_Parameter_HI, Recipe_Parameter_LO, Recipe_Parameter_Default, Recipe_Parameter_Units)
    elif Recipe_Parameter_Type == 'STRING':
        Sect2_Entry_Part2 = ' { CV="%s" }\n    }\n' % (Recipe_Parameter_Default)
    elif Recipe_Parameter_Type == 'NAMEDSET':
        Sect2_Entry_Part2 = '\n      {\n        SET="%s"\n        STRING_VALUE="%s"\n        CHANGEABLE=F\n      }\n    }\n' % (Recipe_Parameter_Set, Recipe_Parameter_Default)
    Sect2_Entry = Sect2_Entry_Part1 + Sect2_Entry_Part2
    print(Sect2_Entry)
    #Section 3 string generation
    if Recipe_Parameter_Type == 'REAL':
        TYPE = 'FLOAT'
    elif Recipe_Parameter_Type == 'INTEGER':
        TYPE = 'INT32'
    elif Recipe_Parameter_Type == 'STRING':
        TYPE = 'UNICODE_STRING'
    elif Recipe_Parameter_Type == 'NAMEDSET':
        TYPE = 'ENUMERATION_VALUE'
    Sect3_Entry_Part1 = '    ATTRIBUTE NAME="%s" TYPE=%s\n    {\n      INDEX=%s\n      EDITABLE=F\n      RECTANGLE= { X=-50 Y=-50 H=1 W=1 }\n' % (Recipe_Parameter_Name, TYPE, new_Last_ID)
    if Recipe_Parameter_Group != '':    
        Sect3_Entry_Part2 = '      GROUP="%s"\n    }\n' % (Recipe_Parameter_Group)
    elif Recipe_Parameter_Group == '':
        Sect3_Entry_Part2 = '    }\n'
    Sect3_Entry = Sect3_Entry_Part1 + Sect3_Entry_Part2
    print(Sect3_Entry)
    #Section 4 string generation
    Sect4_Entry_Part1 = '    ATTRIBUTE_INSTANCE NAME="%s"\n    {\n      VALUE' % (Recipe_Parameter_Name)
    #Section 4 Part 2 String is dependent on the type of recipe parameter entered
    if Recipe_Parameter_Type == 'REAL':
        Sect4_Entry_Part2 = ' { CV=%s }\n    }\n' % (Recipe_Parameter_Default)
    elif Recipe_Parameter_Type == 'INTEGER':
        Sect4_Entry_Part2 = ' { CV=%s }\n    }\n' % (Recipe_Parameter_Default)
    elif Recipe_Parameter_Type == 'STRING':
        Sect4_Entry_Part2 = ' { CV="%s" }\n    }\n' % (Recipe_Parameter_Default)
    elif Recipe_Parameter_Type == 'NAMEDSET':
        Sect4_Entry_Part2 = '\n      {\n        SET="%s"\n        STRING_VALUE="%s"\n        CHANGEABLE=F\n      }\n    }\n' % (Recipe_Parameter_Set, Recipe_Parameter_Default)
    Sect4_Entry = Sect4_Entry_Part1 + Sect4_Entry_Part2
    print(Sect4_Entry)
    #Add new string at the proper index of the text file
    new_main_text = main_text[:incrementing_index_sect1] + Sect1_Entry + main_text[(incrementing_index_sect1):incrementing_index_sect2]    + Sect2_Entry + main_text[(incrementing_index_sect2):incrementing_index_sect3] + Sect3_Entry + main_text[(incrementing_index_sect3):incrementing_index_sect4] + Sect4_Entry + main_text[(incrementing_index_sect4):]
    return new_main_text

def RPDateUpdate(main_text, Epoch_Time, FMT_Time):
    replacement_string = 'time=%s/* "%s" */' % (Epoch_Time,FMT_Time)
    epoch_time_index = main_text.find('BATCH_EQUIPMENT_PHASE_CLASS NAME')
    epoch_time_index = main_text.find('user=',epoch_time_index)
    epoch_time_index = main_text.find('time=',epoch_time_index)
    epoch_time_index_end = main_text.find('/*', epoch_time_index)
    epoch_time_index_end = epoch_time_index_end + len('/*')
    epoch_time_index_end = main_text.find('*/', epoch_time_index_end)
    epoch_time_index_end = epoch_time_index_end + len('*/')
    epoch_time_string_old = main_text[epoch_time_index:epoch_time_index_end]
    new_main_text = main_text[:epoch_time_index] + replacement_string + main_text[epoch_time_index_end:]
    return (new_main_text, epoch_time_string_old, replacement_string)