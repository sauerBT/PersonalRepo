# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os, time, csv

path_to_watch = "C:\\Users\\brian\Desktop\Shared"

before = dict ([(f, None) for f in os.listdir (path_to_watch)])
i = 0
while 1:
    time.sleep (1)
    after = dict ([(f, None) for f in os.listdir (path_to_watch)])
    added = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]
    if added: 
        
        print("Added: ", ", ".join (added))
        file = added[0]
        filename = path_to_watch + '\\' +  file
        fileSizeOld = os.stat(filename).st_size
        # First time
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            line_count = 0
            headerList = ['']*1000
            a = {}
            for row in csv_reader:
                numRows = len(row)
                if line_count == 0:
                    for j in range(numRows):
                        #print(j)
                        #print(f'{(row[j])}')
                        headerList[j] = row[j]
                        key = row[j]
                        a.setdefault(key, [])
                        
                    line_count += 1
                else:
                    for j in range(numRows):
                        #print(f'{(row[j])}')
                        a[headerList[j]].append(row[j])
                    
                    line_count += 1
            print(f'Processed {line_count} lines.')
            lineCountHold = line_count - 1
        i = 1
    if removed: print("Removed: ", ", ".join (removed))
    before = after
    
    if i != 0:
        
        fileSizeNew = os.stat(filename).st_size
        
        if fileSizeNew > fileSizeOld:
            fileSizeOld = fileSizeNew
            print("File Changed")

        # Second time
            with open(filename) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    #print(row)
                    if line_count > lineCountHold:
                        numRows = len(row)
                        for j in range(numRows):
                            #print(f'{(row[j])}')
                            a[headerList[j]].append(row[j])
                    line_count += 1                           
                print(f'Processed {line_count} lines.')