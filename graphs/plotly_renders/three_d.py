import plotly.graph_objects as go
import datetime
import pandas as pd
from graphs.objects import tabe_view_data_async
from async_pull import fetch_to_date


def three_d(data):
    print(data[-1]['lastUpdate'][0])

    graphs = []
    for x in data:
        graphs.append(go.Bar(
            x=x['lastUpdate'],
            y=x['confirmed'],
            text=x['countryRegion'],
            name=str(x['lastUpdate'][0]),
            customdata=x.loc[:, ['confirmed']],
            hovertemplate=
            "<b>%{text}</b><br><br>" +
            "Confirmed: %{customdata[0]}<br>" +
            "<extra></extra>",
        ))

    layout = go.Layout(
        paper_bgcolor='#060606',
        plot_bgcolor='rgba(0,0,0,0)',
        barmode='stack',
        title='Daily Growth By Country',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        ),
        xaxis={'rangeslider_visible': True,
               'range': [data[-1]['lastUpdate'][0],
                         str(datetime.date.today() - datetime.timedelta(days=1))
                         ]

    },

    )
    fig = go.Figure(data=graphs, layout=layout)

    return fig




if __name__ == '__main__':
    fetch_data = fetch_to_date.main('2020-03-28', usa_only=False)
    date_data = three_d(fetch_data).show()

