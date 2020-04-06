import plotly.graph_objects as go
from graphs.objects import tabe_view_data_async
# from datetime import date, timedelta, datetime
import datetime
import pandas as pd
import plotly.express as px
from functools import reduce


def layered_bar_chart(start_date):

    start = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()

    end =datetime.date.today()- start




    data = []
    for x in range(int(end.days)):
        search_date = str((datetime.date.today() - datetime.timedelta(days=1)) - datetime.timedelta(days=x))
        r = tabe_view_data_async.main(search_date)

        data.append(r)

    r = pd.concat(data)

    confirmed_line = go.Scatter(x=r['lastUpdate'], y=r['confirmed'].values, name='Confirmed', mode='markers')
    recovered_line = go.Scatter(x=r['lastUpdate'], y=r['recovered'].values, name='Recovered', mode='markers')
    death_line = go.Scatter(x=r['lastUpdate'], y=r['deaths'].values, name='Deaths', mode='markers')


    # df_merged = pd.concat(master_df, ignore_index=True, sort=False)
    #
    # confirmed_line = go.Scatter(x=df_merged['lastUpdate'], y=df_merged['confirmed'])
    # recovered_line = go.Scatter(x=df_merged['lastUpdate'], y=df_merged['recovered'])
    # death_line = go.Scatter(x=df_merged['lastUpdate'], y=df_merged['deaths'])
    #
    # candle = go.Candlestick(
    #     x=df_merged['lastUpdate'],
    #     open=df_merged['confirmed'],
    #     high=df_merged['confirmed'],
    #     low=df_merged['deaths'],
    #     close=df_merged['deaths'],
    #     increasing={'line': {'color': '#00CC94'}},
    #     decreasing={'line': {'color': '#F50030'}},
    #     name='candlestick'
    # )
    #
    #
    data =[confirmed_line, recovered_line, death_line]

    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
    )

    fig = {'data': data, 'layout':layout}

    return fig


    # print(df_merged)
    #
    # for x in df_merged.head():
    #     print(x)
    #
    # print('----------------')
    # # print(df_merged['countryRegion'].loc[:,['US']])
    # print('----------------')
    #
    #
    # fig = go.Figure(go.Bar(x=df_merged['lastUpdate'], y=df_merged['confirmed'], name='bar-chart'))
    #
    # for x in df_merged:
    #     print('----------------')
    #     print(x)
    #     print(type(x))
    #     print('----------------')
    #     fig.add_trace(go.Bar(x=x['lastUpdate'], y=x['confirmed'], name=x['countryRegion']))
    #
    #
    #
    #
    # fig.update_layout(barmode='stack', xaxis={'categoryorder': 'array', 'categoryarray': df_merged['lastUpdate']})
    # fig.show()




    # r = tabe_view_data_async.main(date)


    # x=['b', 'a', 'c', 'd']
    # fig = go.Figure(go.Bar(x=x, y=[2,5,1,9], name='Montreal'))
    # fig.add_trace(go.Bar(x=x, y=[1, 4, 9, 16], name='Ottawa'))
    # fig.add_trace(go.Bar(x=x, y=[6, 8, 4.5, 8], name='Toronto'))
    #
    # fig.update_layout(barmode='stack', xaxis={'categoryorder':'array', 'categoryarray':['d','a','c','b']})
    # fig.show()

if __name__ == '__main__':
    print(layered_bar_chart('2020-03-28'))