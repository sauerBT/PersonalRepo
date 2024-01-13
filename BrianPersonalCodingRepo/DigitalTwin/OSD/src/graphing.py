import plotly.express as px
import pandas as pd

def graph_3d(x,y,z) -> None:
    df = pd.DataFrame(dict(
        x = x,
        y = y,
        z = z
    ))

    fig = px.scatter_3d(df, x="x", y="y", z = "z")
    fig.update_traces(textposition="bottom right")
    fig.show()