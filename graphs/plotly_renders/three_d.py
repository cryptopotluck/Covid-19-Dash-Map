import plotly.graph_objects as go
import datetime
import pandas as pd
from graphs.objects import tabe_view_data_async


def three_d(start_date):
    print(start_date)
    print(type(start_date))
    start = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()

    end = datetime.date.today() - start

    dates =[]
    for x in range(int(end.days)):

            search_date = str((datetime.date.today() - datetime.timedelta(days=1)) - datetime.timedelta(days=x))
            dates.append(search_date)

    data = []
    for x in dates:
        print(x)
        r = tabe_view_data_async.main(x)

        data.append(r)

    r = pd.concat(data)
    print('------------------')
    print([max(r['deaths'].values)])
    print([max(r['deaths'].values)])
    print('------------------')

    confirmed = []
    for x in r['confirmed']:
        x = x + x
        confirmed.append(x)

    confirmed = go.Histogram(
        y=r['confirmed'],
        x=r['lastUpdate'],
        cumulative_enabled=True,
        name='confirmed'
    )
    deaths = go.Histogram(
        x=r['lastUpdate'].values,
        y=r['deaths'].values,
        cumulative_enabled=True,
        name='deaths'


    )
    recovered = go.Histogram(
        x=r['lastUpdate'].values,
        y=r['recovered'].values,
        cumulative_enabled=True,
        name='recovered'


    )


    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        barmode='stack',
        title='Daily Growth Rate'
    )
    fig = go.Figure(data=[confirmed, deaths, recovered], layout=layout)

    return fig




if __name__ == '__main__':
    three_d('2020-03-28').show()
    print(three_d('2020-03-28'))

