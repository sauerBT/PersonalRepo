# main.py
from fastapi import FastAPI
import pandas as pd
import redis


app = FastAPI()
r = redis.Redis(host="redis", port=6379)

import debugpy
debugpy.listen(("0.0.0.0", 5678))

site = Site('https://controlassociates0.sharepoint.com/sites/MerckKenilworth-MFCSReplacementPerfusion', auth=cred)





@app.get("/listsp")
def listsp():
    data = sp_list.GetListItems('All Items') # this will retrieve all items from list
    # this creates pandas data frame you can perform any operation you like do within 
    # pandas capabilities     

    data_df = pd.DataFrame(data[0:])
    return parse_csv(data_df)