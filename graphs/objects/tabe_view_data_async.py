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


def main(selected_date):
    # Create the asyncio Loop
    loop: AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    t0 = datetime.datetime.now()
    print(colorama.Fore.LIGHTGREEN_EX + 'App started', flush=True)
    result = loop.run_until_complete(get_covid_data(loop, date=selected_date))
    dt = datetime.datetime.now() - t0
    print(colorama.Fore.LIGHTGREEN_EX + "App exiting, total time: {:,.2f} sec.".format(dt.total_seconds()), flush=True)
    return result


async def get_covid_data(loop: AbstractEventLoop, date: str):
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
        finished_fetch = await clean_data(data)
        finished.append(finished_fetch)
    print('finished')
    print(str(finished[0]))

    return finished[0]

async def get_api(date: str) -> str:


    url = f'https://covid19.mathdro.id/api/daily/{date}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=ssl_context) as resp:
            resp.raise_for_status()

            api = await resp.json()
            return api

async def clean_data(c_data):



    return c_data[['provinceState','countryRegion', 'lastUpdate', 'confirmed', 'deaths', 'recovered', 'lat', 'long']]




if __name__ == '__main__':
    print(main(selected_date='2020-03-20'))

