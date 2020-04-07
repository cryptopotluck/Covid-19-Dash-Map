import plotly.express as px
from async_pull import fetch_to_date
import plotly.graph_objects as go
import datetime
import pandas as pd

def animation_graph(data):

    data=data

    graphs = []
    for x in data:


        graphs.append(go.Bar(
                            x = x['lastUpdate'],
                            y = x['confirmed'],
                            text=x['provinceState'],
                            name=str(x['lastUpdate'][0][0:10]),
                            customdata=x.loc[:, ['confirmed']],
                            hovertemplate =
                            "<b>%{text}</b><br><br>" +
                            "Confirmed: %{customdata[0]}<br>" +
                            "<extra></extra>",
                                                ))




    layout = go.Layout(
        height=800,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        barmode='stack',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )



    fig = go.Figure(data=graphs, layout=layout)

    return fig

if __name__ == '__main__':
    animation_graph(data=fetch_to_date.main('2020-03-28')).show()

