import plotly.express as px
from async_pull import fetch_historic
import plotly.graph_objects as go
import datetime
import pandas as pd


def global_growth_graph(data=fetch_historic.main()):
        data = data

        graphs = [
            go.Scatter(
                x=data['reportDate'],
                line=dict(color='rgb(111, 231, 219)'),
                y=data['totalConfirmed'],
                name='Total Cases',
                fill='tonexty',

            ),
            go.Scatter(
                x=data['reportDate'],
                y=data['mainlandChina'],
                line=dict(color='red'),
                name='China Cases',
                fill='tozeroy',

            ),
        ]

        layout = go.Layout(
            title='Covid-19 Growth Rate',
            height=800,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            barmode='stack',
            xaxis={'rangeslider_visible':True},
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            )
        )

        fig = go.Figure(data=graphs, layout=layout)

        return fig

if __name__ == '__main__':
    global_growth_graph(data=fetch_historic.main()).show()

