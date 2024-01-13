from fastapi import FastAPI
import uvicorn
import numpy as np
import monte_carlo as mc
import feeder_model as fm
import graphing as g

app = FastAPI()

@app.get("/models/saturatedFeedFactor/run")
def run_sat_density(bulk_density: float,vpr: float) -> dict[str, list[float]]:
    x = list(np.random.normal(bulk_density,.1,10000))
    y = list(np.random.normal(vpr,.05,10000))
    z = mc.monte_carlo(fm.sat_feed_factor, mc.mc_arg([x,y]))
    g.graph_3d(x,y,z)
    
    return {"saturated feed factor" : z}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=30000)




