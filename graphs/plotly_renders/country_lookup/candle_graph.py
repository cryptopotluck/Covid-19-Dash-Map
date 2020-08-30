import plotly.graph_objects as go
from async_pull import fetch_to_date


def request_candlestick(redis_data, country):
    df_list = redis_data


    print(f'type of country: {type(country)}')
    if type(country) != type(dict()):
        print('Triggered Check')
        for df in df_list:
            data = []
            for c in country:
                df2 = df['countryRegion'].str.contains(c)
                df = df[df2]
                close = []
                for c, d in zip(df['confirmed'], df['deaths']):
                    close.append(float(c[0]) / float(d[0]))

                data.append(go.Line(name=f'{df["countryRegion"]} - Confirmed',
                                    text=df['confirmed'],
                                    hovertemplate=
                                    "Confirmed #: %{text}<br>" +
                                    "<extra></extra>",
                                    x=df['lastUpdate'],
                                    y=df['confirmed'],
                                    marker=dict(
                                        size=df['confirmed_size'][0],
                                        color='yellow',
                                    ),
                                    ))
                data.append(go.Line(name=f'{df["countryRegion"]} - Deaths',
                                    text=close,
                                    hovertemplate=
                                    "Death Rate: %{text}<br>" +
                                    "<extra></extra>",
                                    x=df['lastUpdate'],
                                    y=df['deaths'],
                                    marker=dict(
                                        size=df['death_size'][0],
                                        color='salmon',
                                    ),
                                    ))
                data.append(go.Line(name=f'{df["countryRegion"]} - Recovered',
                                    text=df['recovered'],
                                    hovertemplate=
                                    "Recovered: %{text}<br>" +
                                    "<extra></extra>",
                                    x=df['lastUpdate'],
                                    y=df['recovered'],
                                    marker=dict(
                                        size=df['recovered_size'][0],
                                        color='green',
                                    ),
                                    ))

    else:
        data = []
        for df in df_list:
            df2 = df['countryRegion'].str.contains(country['countryRegion'])

            df = df[df2]

            close = []
            for c, d in zip(df['confirmed'], df['deaths']):
                close.append(float(c[0])/float(d[0]))

            data.append(go.Line(name='Confirmed',
                                text=df['confirmed'],
                                hovertemplate=
                                "Confirmed #: %{text}<br>" +
                                "<extra></extra>",
                                x=df['lastUpdate'],
                                y=df['confirmed'],
                                marker=dict(
                                    size=df['confirmed_size'][0],
                                    color='yellow',
                                ),
                                ))
            data.append(go.Line(name='Deaths',
                                text=close,
                                hovertemplate=
                                "Death Rate: %{text}<br>" +
                                "<extra></extra>",
                                x=df['lastUpdate'],
                                y=df['deaths'],
                                marker=dict(
                                    size=df['death_size'][0],
                                    color='salmon',
                                ),
                                ))
            data.append(go.Line(name='Recovered',
                                text=df['recovered'],
                                hovertemplate=
                                "Recovered: %{text}<br>" +
                                "<extra></extra>",
                                x=df['lastUpdate'],
                                y=df['recovered'],
                                marker=dict(
                                    size=df['recovered_size'][0],
                                    color='green',
                                ),
                                ))

        layout = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            )
        )

        fig = go.Figure(data=data, layout=layout)

        return fig


if __name__ == '__main__':
    map = request_candlestick()
    map.show()
    print(map)




