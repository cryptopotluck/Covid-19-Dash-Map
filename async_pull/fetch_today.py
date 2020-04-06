import asyncio
import datetime
from asyncio import AbstractEventLoop
import aiohttp
import colorama

import pandas as pd
import ssl
import certifi


date=str(datetime.date.today()-datetime.timedelta(days=1))

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())


def main(date=date, value=400, usa_only=False):
    # Create the asyncio Loop
    loop: AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    t0 = datetime.datetime.now()
    print(colorama.Fore.LIGHTGREEN_EX + 'App started', flush=True)
    result = loop.run_until_complete(get_covid_data(loop, date=date, value=value, usa_only=usa_only))
    dt = datetime.datetime.now() - t0
    print(colorama.Fore.LIGHTGREEN_EX + "App exiting, total time: {:,.2f} sec.".format(dt.total_seconds()), flush=True)
    return result


async def get_covid_data(loop: AbstractEventLoop, date: str, value: int, usa_only: bool):
    tasks = []


    tasks.append((loop.create_task(get_api(date=date))))

    print(f'tasks = {tasks}')
    finished = []
    for task in tasks:
        api = await task
        # print('--------------')
        data = pd.DataFrame(api)
        # print(data)
        # print('--------------')
        finished_fetch = await clean_data(data, scale=value, usa_only=usa_only)
        finished.append(finished_fetch)

    print(colorama.Fore.WHITE + f"Task Finished: {finished[0]}", flush=True)
    return finished[0]


async def get_api(date: str) -> str:

    url = f'https://covid19.mathdro.id/api/daily/{date}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=ssl_context) as resp:
            resp.raise_for_status()

            api = await resp.json()
            return api


async def clean_data(data, scale, usa_only):

    if usa_only == True:
        usa_only = data['countryRegion'].str.contains('US')
        data = data[usa_only]


    data['confirmed_size'] = data.loc[:, 'confirmed'].apply(lambda x: int(x) / scale)
    data['death_size'] = data.loc[:, 'deaths'].apply(lambda x: int(x) / scale)
    data['recovered_size'] = data.loc[:, 'recovered'].apply(lambda x: int(x) / scale)

    return data[['provinceState','countryRegion', 'lastUpdate', 'confirmed', 'confirmed_size', 'deaths', 'death_size', 'recovered', 'recovered_size', 'lat', 'long']]


if __name__ == '__main__':

    print(colorama.Fore.CYAN + f"symbol Finished: {main(date='2020-03-24')}", flush=True)
