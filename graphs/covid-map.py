import requests
from pandas import DataFrame as df
import plotly.graph_objects as go


def request_map():
    r = requests.get('https://coronavirus-tracker-api.herokuapp.com/v2/locations')

    r = df(r.json()['locations'])

    deaths = []
    death_size = []
    confirmed = []
    confirmed_size = []
    recovered = []
    recovered_size = []
    for x in r['latest']:
        confirmed.append(x['confirmed'])
        confirmed_size.append(float(x['confirmed']) / 500)
        deaths.append(x['deaths'])
        death_size.append(float(x['deaths']) / 100)
        recovered.append(x['recovered'])
        recovered_size.append(float(x['recovered']) / 500)

    lon = []
    lat = []
    for x in r['coordinates']:
        lon.append(x['longitude'])
        lat.append(x['latitude'])

    r['confirmed'] = df(confirmed)
    r['confirmed_size'] = df(confirmed_size)
    r['deaths'] = df(deaths)
    r['death_size'] = df(death_size)
    r['recovered'] = df(recovered)
    r['recovered_size'] = df(recovered_size)
    r['lat'] = df(lat)
    r['lon'] = df(lon)

    map_confirmed = go.Scattermapbox(
        name='Confirmed Cases',
        lon=r['lon'],
        lat=r['lat'],
        text=r['country'],
        customdata=r.loc[:, ['confirmed', 'deaths', 'recovered']],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Confirmed: %{customdata[0]}<br>" +
        "<extra></extra>",
        mode='markers',
        fillcolor='mediumturquoise',
        showlegend=True,
        marker=go.scattermapbox.Marker(
            size=r['confirmed_size'],
            color='mediumturquoise',
            opacity=0.7
        )

    )

    map_deaths = go.Scattermapbox(
        name='Deaths',
        lon=r['lon'],
        lat=r['lat'],
        text=r['country'],
        customdata=r.loc[:, ['confirmed', 'deaths', 'recovered']],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Deaths: %{customdata[1]}<br>" +
        "<extra></extra>",
        mode='markers',
        fillcolor='rgb(242, 177, 172)',
        showlegend=True,
        marker=go.scattermapbox.Marker(
            size=r['death_size'],
            color='salmon',
            opacity=0.7
        )
    )

    map_recovered = go.Scattermapbox(
        customdata=r.loc[:, ['confirmed', 'deaths', 'recovered']],
        # deaths = r['deaths'],
        # recovered = r['recovered'],
        name='recovered',
        lon=r['lon'],
        lat=r['lat'],
        text=r['country'],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Recovered: %{customdata[2]}<br>" +
        "<extra></extra>",
        mode='markers',
        fillcolor='purple',
        showlegend=True,
        marker=go.scattermapbox.Marker(
            size=r['recovered_size'],
            color='green',
            opacity=0.7
        )
    )

    layout = go.Layout(
        height=800,
        mapbox_style="white-bg",
        autosize=True,
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
        plot_bgcolor='rgba(0,0,0,0)'
    )

    data = [map_confirmed, map_deaths, map_recovered]

    fig = go.Figure(data=data, layout=layout)

    return fig


if __name__ == '__main__':
    request_map()



