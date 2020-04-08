import plotly.graph_objects as go
import datetime
import pandas as pd
from graphs.objects import tabe_view_data_async
from async_pull import fetch_to_date


def three_d(start_date, usa_only=False):

    r = fetch_to_date.main(start_date)


    r = pd.concat(r)

    dates = tuple(r['lastUpdate'])


    confirmed = go.Bar(
        y=r['confirmed'],
        x=dates,
        name='confirmed',
        customdata=r.loc[:, ['confirmed', 'countryRegion']],
        hovertemplate=
        "%{customdata[1]} Confirmed: %{customdata[0]}<br>" +
        "<extra></extra>"
    )
    deaths = go.Bar(
        x=dates,
        y=r['deaths'],
        name='deaths',
        customdata=r.loc[:, ['deaths', 'countryRegion']],
        hovertemplate=
        "%{customdata[1]} Confirmed: %{customdata[0]}<br>" +
        "<extra></extra>"
    )

    recovered = go.Bar(
        x=dates,
        y=r['recovered'],
        name='recovered',
        customdata = r.loc[:, ['recovered', 'countryRegion']],
                 hovertemplate =
        "%{customdata[1]} Confirmed: %{customdata[0]}<br>" +
        "<extra></extra>"
    )


    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        barmode='stack',
        title='Daily Growth By Country',
        xaxis={'rangeslider_visible': True,
         'range': [start_date,
                  str(datetime.date.today() - datetime.timedelta(days=1))
                  ]
    },


    )
    fig = go.Figure(data=[deaths, recovered, confirmed], layout=layout)

    return fig




if __name__ == '__main__':
    three_d('2020-03-28').show()
    print(three_d('2020-03-28'))

