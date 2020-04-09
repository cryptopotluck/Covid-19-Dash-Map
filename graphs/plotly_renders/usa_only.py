import plotly.graph_objects as go
import datetime
import pandas as pd
from async_pull import fetch_today
import time


def request_usa_map(data):

    map_confirmed = go.Scattermapbox(
        name='Confirmed Cases',
        lon=data['long'],
        lat=data['lat'],
        text=data['countryRegion'],
        customdata=data.loc[:, ['confirmed']],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Confirmed: %{customdata[0]}<br>" +
        "<extra></extra>",
        mode='markers',
        fillcolor='mediumturquoise',
        showlegend=True,
        marker=go.scattermapbox.Marker(
            size=data['confirmed_size'],
            color='mediumturquoise',
            opacity=0.75
        ),
        opacity=0.75,

    )

    map_deaths = go.Scattermapbox(
        name='Deaths',
        lon=data['long'],
        lat=data['lat'],
        text=data['countryRegion'],
        customdata=data.loc[:, ['deaths']],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Deaths: %{customdata[0]}<br>" +
        "<extra></extra>",
        mode='markers',
        fillcolor='rgb(242, 177, 172)',
        showlegend=True,
        marker=go.scattermapbox.Marker(
            size=data['death_size'],
            color='salmon',
            opacity=0.75
        ),
        opacity=0.75,
    )

    map_recovered = go.Scattermapbox(
        customdata=data.loc[:, ['recovered']],
        # deaths = r['deaths'],
        # recovered = r['recovered'],
        name='recovered',
        lon=data['long'],
        lat=data['lat'],
        text=data['countryRegion'],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Recovered: %{customdata[0]}<br>" +
        "<extra></extra>",
        mode='markers',
        fillcolor='purple',
        showlegend=True,
        marker=go.scattermapbox.Marker(
            size=data['recovered_size'],
            color='green',
        ),
        opacity=0.75,
    )
    token = 'pk.eyJ1IjoiY3J5cHRvcG90bHVjayIsImEiOiJjazhtbTN6aHEwa3lwM25taW5qNTdicHAwIn0.xFsCTDqPE_0L-OHwv21qTg'

    layout = go.Layout(
        height=800,
        autosize=True,
        mapbox_accesstoken=token,
        mapbox_style="open-street-map",
        mapbox_center={"lat": 37.0902, "lon": -95.7129},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )

    data = [map_confirmed, map_recovered, map_deaths]

    fig = go.Figure(data=data, layout=layout)
    return fig


if __name__ == '__main__':
    data = fetch_today.main(value=1000)
    request_usa_map(data).show()

