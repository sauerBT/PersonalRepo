# main.py

from fastapi import FastAPI
import redis

app = FastAPI()

r = redis.Redis(host="redis", port=6379)

import debugpy
debugpy.listen(("0.0.0.0", 5678))

@app.get("/")
async def root():
    return {"message": "Hello World!123"}

@app.get("/hits")
async def root():
    r.incr("hits")
    return {"number of hits": r.get("hits")}
