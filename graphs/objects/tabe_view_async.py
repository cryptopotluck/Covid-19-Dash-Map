import asyncio
import datetime
from asyncio import AbstractEventLoop
import aiohttp
import colorama
import socket
import requests

from pandas import DataFrame as df
import pandas as pd
import dash_bootstrap_components as dbc
import dash_html_components as html
import urllib.request
import platform
import os
import ssl
import certifi
import time

date=str(datetime.date.today()-datetime.timedelta(days=1))

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())

print(f'holly date {date}')

def main(selected_date):
    # Create the asyncio Loop
    loop: AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    t0 = datetime.datetime.now()
    print(colorama.Fore.LIGHTGREEN_EX + 'App started', flush=True)
    result = loop.run_until_complete(get_covid_data(loop, dates=[date, selected_date]))
    dt = datetime.datetime.now() - t0
    print(colorama.Fore.LIGHTGREEN_EX + "App exiting, total time: {:,.2f} sec.".format(dt.total_seconds()), flush=True)
    return result


async def get_covid_data(loop: AbstractEventLoop, dates: list):
    tasks = []

    for d in dates:
        tasks.append((loop.create_task(get_api(date=d))))

    print(f'tasks = {tasks}')
    finished = []
    for task in tasks:
        api = await task
        # print('--------------')
        data = pd.DataFrame(api)
        # print(data)
        # print('--------------')
        finished_fetch = await clean_data(data)
        finished.append(finished_fetch)
    print('finished')
    print(str(finished[0]))
        # print(colorama.Fore.WHITE + f"symbol Finished: {finished_fetch}", flush=True)
    return finished[0]

async def get_api(date: str) -> str:


    url = f'https://covid19.mathdro.id/api/daily/{date}'
    # print(x)
    # url = requests.get(f'https://covid19.mathdro.id/api/daily/{date}')
    # daily_report_url = opener.open(f'https://covid19.mathdro.id/api/daily/{date}', timeout=2)

    # print(f'type: {type(url)}')
    # print(f'URL DUMN: {url}')
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=ssl_context) as resp:
            resp.raise_for_status()

            api = await resp.json()
            return api

async def clean_data(c_data):

    headers = []
    for x in c_data.head():
        print(c_data[x].name)
        headers.append(html.Th(c_data[x].name))

    table_header = [
        html.Thead(html.Tr([html.Th(x) for x in headers]))
    ]

    table_values = []

    provinceState = c_data['provinceState'].values

    countryRegion = c_data['countryRegion'].values

    lastUpdate = c_data['lastUpdate'].values

    confirmed = c_data['confirmed'].values

    deaths = c_data['deaths'].values

    recovered = c_data['recovered'].values

    for p, region, l, c, d, r in zip(provinceState, countryRegion, lastUpdate, confirmed, deaths, recovered):
        # print(html.Tr([html.Td(p), html.Td(region), html.Td(l), html.Td(c), html.Td(d), html.Td(r)]))
        table_values.append(html.Tr([html.Td(p), html.Td(region), html.Td(l), html.Td(c), html.Td(d), html.Td(r)]))

    table_body = [html.Tbody(table_values)]

    return dbc.Row([dbc.Col(html.Div(), width=2), dbc.Col(dbc.Table(table_header + table_body, bordered=True)), dbc.Col(html.Div(), width=2)])




if __name__ == '__main__':
    print(main(selected_date='2020-03-20'))
    # # print(main(selected_date='2020-03-20'))
    #
    #
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main(selected_date='2020-03-20'))
    #
    # def drive(c):
    #     while True:
    #         try:
    #             print('look here')
    #             print(c)
    #             print()
    #             susp_val = c.send(None)
    #             if susp_val is not None and susp_val[0] == 'sleep':
    #                 time.sleep(susp_val[1])
    #         except StopIteration as e:
    #             return e.value


    # fetch today news
    # today_news_list = []
    # for n in main(selected_date='2020-03-20'):
    #     today_news_list.append(n)
    #
    # print(today_news_list)
