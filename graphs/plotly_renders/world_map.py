import plotly.graph_objects as go
from async_pull import date_to_today_list
from mapbox_token import mapbox_token

def request_world_map(redis_data, lat=0, long=0):
    token = mapbox_token

    maps = []

    print(redis_data)

    for df in redis_data[::-1]:
        print('problem is here')
        print(df)

        map_confirmed = go.Scattermapbox(
            name='Confirmed',
            lon=df['long'],
            lat=df['lat'],
            text=df['countryRegion'],
            customdata=df.loc[:, ['confirmed']],
            hovertemplate=
            "<b>%{text}</b><br><br>" +
            "Deaths: %{customdata[0]}<br>" +
            "<extra></extra>",
            mode='markers',
            fillcolor='rgb(242, 177, 172)',
            showlegend=True,
            ids=df['lastUpdate'],
            marker=go.scattermapbox.Marker(
                size=df['confirmed_size'],
                color='yellow',
                opacity=0.5
            ),
            opacity=0.5,
        )

        map_deaths = go.Scattermapbox(
                name='Deaths',
                lon=df['long'],
                lat=df['lat'],
                text=df['countryRegion'],
                customdata=df.loc[:, ['deaths']],
                hovertemplate=
                "<b>%{text}</b><br><br>" +
                "Deaths: %{customdata[0]}<br>" +
                "<extra></extra>",
                mode='markers',
                fillcolor='rgb(242, 177, 172)',
                showlegend=True,
                ids=df['lastUpdate'],
                marker=go.scattermapbox.Marker(
                    size=df['death_size'],
                    color='salmon',
                    opacity=1
                ),
                opacity=1,
            )

        map_recovered = go.Scattermapbox(
                customdata=df.loc[:, ['recovered']],
                name='recovered',
                lon=df['long'],
                lat=df['lat'],
                text=df['countryRegion'],
                hovertemplate=
                "<b>%{text}</b><br><br>" +
                "Recovered: %{customdata[0]}<br>" +
                "<extra></extra>",
                mode='markers',
                fillcolor='purple',
                showlegend=True,
                ids=df['lastUpdate'],
                marker=go.scattermapbox.Marker(
                    size=df['recovered_size'],
                    color='green',
                ),
                opacity=0.5,
            )


        maps.append((map_confirmed, map_recovered, map_deaths))

    if lat and long != 0:

        layout = go.Layout(
            title='Past 7 Days Growth Animation',
            height=800,
            autosize=True,
            mapbox_accesstoken=token,
            mapbox_style="stamen-watercolor",
            mapbox_center={"lat": float(lat), "lon": float(long)},
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                              method="animate",
                              args=[None])])],
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            ),
            mapbox = dict(
                center=dict(
                    lat=float(lat),
                    lon=float(lat)
                ),
                pitch=0,
                zoom=3,
            )
        )
        layout.mapbox.style = "stamen-watercolor"

    else:
        layout = go.Layout(
            title='Past 7 Days Growth Animation',
            height=800,
            mapbox_accesstoken=token,
            mapbox_style="stamen-watercolor",
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
                }]
            ,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            )
        )
        layout.mapbox.style = "stamen-watercolor"

    frames = []
    for m in maps:
        frames.append(go.Frame(data=m))

    fig = go.Figure(data=[maps[0][0], maps[0][1], maps[0][2]], frames=frames, layout=layout)

    return fig


if __name__ == '__main__':
    map = request_world_map(date_to_today_list.main(date='2020-08-24'))
    map.show()
    print(map)




