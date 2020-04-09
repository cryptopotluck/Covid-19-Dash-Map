import plotly.graph_objects as go
from graphs.plotly_renders.data import request_map_data
from graphs.BadWayToRequestData.mathdro import map_data
import plotly.express as px
from async_pull import fetch_to_date
import time


def request_map(data):

    print()
    print()
    print('THE FUCK ARE YOU DOING?')
    print(data)
    for r in data:
        r['confirmed_size'] = r['confirmed'].apply(lambda x: int(x)/500)
        r['death_size'] = r['deaths'].apply(lambda x: int(x) / 500)
        r['recovered_size'] = r['recovered'].apply(lambda x: int(x) / 500)


    maps = []
    for r in data:

        map_confirmed = go.Scattermapbox(
            name='Confirmed Cases',
            lon=r['long'],
            lat=r['lat'],
            text=r['countryRegion'],
            customdata=r.loc[:, ['confirmed']],
            hovertemplate=
            "<b>%{text}</b><br><br>" +
            "Confirmed: %{customdata[0]}<br>" +
            "<extra></extra>",
            mode='markers',
            fillcolor='mediumturquoise',
            showlegend=True,
            ids=r['lastUpdate'],
            marker=go.scattermapbox.Marker(
                size=r['confirmed_size'],
                color='mediumturquoise',
                opacity=0.5
            ),
            opacity=0.5,

        )

        map_deaths = go.Scattermapbox(
            name='Deaths',
            lon=r['long'],
            lat=r['lat'],
            text=r['countryRegion'],
            customdata=r.loc[:, ['deaths']],
            hovertemplate=
            "<b>%{text}</b><br><br>" +
            "Deaths: %{customdata[0]}<br>" +
            "<extra></extra>",
            mode='markers',
            fillcolor='rgb(242, 177, 172)',
            showlegend=True,
            ids=r['lastUpdate'],
            marker=go.scattermapbox.Marker(
                size=r['death_size'],
                color='salmon',
                opacity=0.5
            ),
            opacity=0.5,
        )

        map_recovered = go.Scattermapbox(
            customdata=r.loc[:, ['recovered']],
            # deaths = r['deaths'],
            # recovered = r['recovered'],
            name='recovered',
            lon=r['long'],
            lat=r['lat'],
            text=r['countryRegion'],
            hovertemplate=
            "<b>%{text}</b><br><br>" +
            "Recovered: %{customdata[0]}<br>" +
            "<extra></extra>",
            mode='markers',
            fillcolor='purple',
            showlegend=True,
            ids=r['lastUpdate'],
            marker=go.scattermapbox.Marker(
                size=r['recovered_size'],
                color='green',
            ),
            opacity=0.5,
        )
        maps.append((map_confirmed, map_recovered, map_deaths))

    layout = go.Layout(
        height=800,
        mapbox_style="white-bg",
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None])])],
        autosize=True,
        xaxis=dict(autorange=True),
        yaxis=dict(autorange=True),
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ],
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )


    frames = []
    for l in maps:
        frames.append(go.Frame(data=l))

    fig = go.Figure(data=[maps[0][0], maps[0][1], maps[0][2]], layout=layout, frames=frames[::-1])

    return fig


if __name__ == '__main__':
    map = request_map(fetch_to_date.main(date='2020-03-24', usa_only=False, value=500))
    map.show()
    print(map)




