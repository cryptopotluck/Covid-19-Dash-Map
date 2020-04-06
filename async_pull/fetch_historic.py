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


def main():
    # Create the asyncio Loop
    loop: AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    t0 = datetime.datetime.now()
    print(colorama.Fore.LIGHTGREEN_EX + 'App started', flush=True)
    result = loop.run_until_complete(get_covid_data(loop))
    dt = datetime.datetime.now() - t0
    print(colorama.Fore.LIGHTGREEN_EX + "App exiting, total time: {:,.2f} sec.".format(dt.total_seconds()), flush=True)
    return result


async def get_covid_data(loop: AbstractEventLoop):
    tasks = []


    tasks.append((loop.create_task(get_api())))

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

    print(colorama.Fore.WHITE + f"Task Finished: {finished[0]}", flush=True)
    return finished[0]


async def get_api() -> str:

    url = f'https://covid19.mathdro.id/api/daily'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=ssl_context) as resp:
            resp.raise_for_status()

            api = await resp.json()
            return api


async def clean_data(data):

    data['fill_value_confirmed'] =  data['totalConfirmed'][::-1]
    data['fill_value_china'] = data['mainlandChina'][::-1]

    return data[['totalConfirmed', 'fill_value_confirmed','mainlandChina','fill_value_china', 'otherLocations', 'deltaConfirmed',  'reportDate']]


if __name__ == '__main__':

    print(colorama.Fore.CYAN + f"symbol Finished: {main()}", flush=True)
