def fileOnChangeRead(df,dfJson):  
    import os
    for f in range(len(df.columns)):
        fileSizeNew = os.stat(df[df.columns[f]]['filename']).st_size
        if fileSizeNew > int(df[df.columns[f]]['filesizeold']):           
            data_mine = pd.read_csv(df[df.columns[f]]['filename'],index_col = 'date_time', parse_dates=[['date', 'time']])
            df[df.columns[f]]['latestLineCount'] = len(data_mine.index)
            dfJson[df.columns[f]] = [json.loads(data_mine.to_json(orient='index')),list(json.loads(data_mine.to_json(orient='index')).keys())]
            df[df.columns[f]]['filesizeold'] = fileSizeNew
            df[df.columns[f]]['transmissionFlag'] = True
            print(df.columns[f], " updated.")
    return (df,dfJson)

def websocketTransmission(df,dfJson):
    from websocket import create_connection
    
    for f in range(df.shape[1]):  #iterate through each active file
        if df[df.columns.astype(str)[f]]['transmissionFlag']:
            print("New transmission ", df.columns[f]  )
            ws = create_connection("ws://192.168.1.112:1880/ws/example")
            #if df[df.columns.astype(str)[f]]['initFileTransmission']:
            for j in range(int(df[df.columns.astype(str)[f]]['transmittedLineCount']),int(df[df.columns.astype(str)[f]]['latestLineCount'])):  #iterate through each column index
                #print(dfJson[dfJson.columns.astype(str)[f]]['JsonString'][dfJson[dfJson.columns.astype(str)[f]]['JsonKeys'][j]])
                ws.send(json.dumps(dfJson[dfJson.columns.astype(str)[f]]['JsonString'][dfJson[dfJson.columns.astype(str)[f]]['JsonKeys'][j]]))
                result =  ws.recv()
                #print("Received '%s'" % result)
                print(j)
            ws.close()
            df[df.columns.astype(str)[f]]['transmittedLineCount'] = df[df.columns.astype(str)[f]]['latestLineCount']
            df[df.columns.astype(str)[f]]['transmissionFlag'] = False 
    return (df,dfJson)

def watchdogInitialize(csvOut):
    jsonIndex = ['JsonString','JsonKeys']
    dfJson = pd.DataFrame(index = jsonIndex)
    try: #CSV file is not empty
        df = pd.read_csv(csvOut)
        metaDataIndex = pd.Series(['filename','filesizeold','latestLineCount','transmittedLineCount','transmissionFlag','headerlist'])
        df = df.set_index(metaDataIndex)
        before = dict ([(f, None) for f in os.listdir (path_to_watch)])
        #before = dict ([(f, None) for f in list(df.columns)])
        #if 'A' in df.columns:
        if len(df.columns) >= len(before.keys()):
            maxNumOfFiles = len(df.columns)
        else:
            maxNumOfFiles = len(before.keys())
                
        for f in reversed(range(maxNumOfFiles)):
            if f <= (len(before.keys())-1):
                if not list(before.keys())[f] in df.columns:
                    print("Removing before: ", list(before.keys())[f])
                    del before[list(before.keys())[f]]
            if f <= (len(df.columns)-1):
                if not df.columns[f] in list(before.keys()):
                    print("Removing df: ", df.columns[f])
                    del df[df.columns[f]]
            
        for f in range(len(df.columns)): 
            data_mine = pd.read_csv(df[df.columns[f]]['filename'],index_col = 'date_time', parse_dates=[['date', 'time']])
            dfJson[df.columns[f]] = [json.loads(data_mine.to_json(orient='index')),list(json.loads(data_mine.to_json(orient='index')).keys())]
        print("Files re-established: ", list(dfJson.columns))
        print('Metadata CSV file read')
    
    except: #CSV file is empty
        metaDataIndex = ['filename','filesizeold','latestLineCount','transmittedLineCount','transmissionFlag','headerlist']
        df = pd.DataFrame(index = metaDataIndex)
        before = dict()
        print('Metadata CSV file not read')
    
    return(df,dfJson,before)
"""
-------------------------------------------------------------------------------
Logic Starts Here

- needs:
    On Change Websocket sends - also add on change for new header columns
    On start df additions and websocket sends
-------------------------------------------------------------------------------
"""        
import os, time, csv, json
import numpy as np
import pandas as pd 

path_to_watch = "C:\\Users\\brian\\Desktop\\Share" 
csvOut = "C:\\Users\\brian\\Desktop\\metadata\\metadata.csv" 
sleepTime = 1
[df,dfJson,before] = watchdogInitialize(csvOut)
 
try:
    while 1:
        time.sleep(sleepTime)
        after = dict ([(f, None) for f in os.listdir (path_to_watch)])
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]
        if added: 
            print("Added: ", ", ".join (added))
            for f in range(len(added)):  
                print(f)
                filename = path_to_watch + '\\' +  added[f]
                fileSizeOld = os.stat(filename).st_size
                with open(filename, 'r') as infile:
                    reader = csv.DictReader(infile)
                    headerList = reader.fieldnames
                    data_mine = pd.read_csv(filename,index_col = 'date_time', parse_dates=[['date', 'time']])
                    latestLineCount = len(data_mine.index)
                    transmittedLineCount = 0
                    publishTransmission = True
                    df[added[f]] = [filename,fileSizeOld,latestLineCount,transmittedLineCount,publishTransmission,headerList]
                    dfJson[added[f]] = [json.loads(data_mine.to_json(orient='index')),list(json.loads(data_mine.to_json(orient='index')).keys())]      
            print("New files loaded: ", df.columns)
        if removed: 
            print("Removed: ", ", ".join (removed))
            for f in range(len(removed)): 
                del df[removed[f]]
                if not dfJson.empty:
                    del dfJson[removed[f]]
        before = after
        if not df.empty:
            [df,dfJson] = fileOnChangeRead(df,dfJson)
            [df,dfJson] = websocketTransmission(df,dfJson)
            df.to_csv(csvOut, index=False)   
except KeyboardInterrupt:
    pass

#import re, string
#    re.sub('[\W_]+', '', string.printable)   