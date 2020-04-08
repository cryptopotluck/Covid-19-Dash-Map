import asyncio
import datetime
from asyncio import AbstractEventLoop
import aiohttp
import colorama

import pandas as pd
import ssl
import certifi


ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())


def main(date='2020-03-24', value=400, usa_only=False):
    start = datetime.datetime.strptime(date, '%Y-%m-%d').date()

    end = datetime.date.today() - start

    dates = []
    for x in range(int(end.days)):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        search_date = yesterday - datetime.timedelta(days=x)
        dates.append(search_date.strftime('%Y-%m-%d'))

    print(dates)
    # Create the asyncio Loop
    loop: AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    t0 = datetime.datetime.now()
    print(colorama.Fore.LIGHTGREEN_EX + 'App started', flush=True)
    result = loop.run_until_complete(get_covid_data(loop, dates=dates, value=value, usa_only=usa_only))
    dt = datetime.datetime.now() - t0
    print(colorama.Fore.LIGHTGREEN_EX + "App exiting, total time: {:,.2f} sec.".format(dt.total_seconds()), flush=True)
    return result


async def get_covid_data(loop: AbstractEventLoop, dates: list, value: int, usa_only:bool):
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
        finished_fetch = await clean_data(data, scale=value, usa_only=usa_only)
        finished.append(finished_fetch)
    print('finished')

    # finished = pd.concat(finished)
    print(finished)

    return finished


async def get_api(date: str) -> str:

    url = f'https://covid19.mathdro.id/api/daily/{date}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=ssl_context) as resp:
            resp.raise_for_status()

            api = await resp.json()
            return api


async def clean_data(c_data, scale, usa_only):
    r=c_data

    if usa_only == True:
        usa_only = c_data['countryRegion'].str.contains('US')

        r = c_data[usa_only]

    r['confirmed_size'] = r.loc[:, 'confirmed'].apply(lambda x: int(x) / scale)
    r['death_size'] = r.loc[:, 'deaths'].apply(lambda x: int(x) / scale)
    r['recovered_size'] = r.loc[:, 'recovered'].apply(lambda x: int(x) / scale)

    dates = []
    for x in r['lastUpdate']:
        if str(x[4]) != '-':

           print(x[0:7])

           try:
                print(datetime.datetime.strptime(str(x[0:7]), '%m/%d/%y').date())
                x = datetime.datetime.strptime(str(x[0:7]), '%m/%d/%y').date()
                print('%m/%d/%y')
                print(x)
                print()
           except:
                print(datetime.datetime.strptime(str(x[0:6]), '%m/%d/%y').date())
                x = datetime.datetime.strptime(str(x[0:6]), '%m/%d/%y').date()
                print('%m/%d/%y')
                print(x)
                print()

        else:
            print('other')
            print(x)
            print()
            x = datetime.datetime.strptime(str(x[0:10]), '%Y-%m-%d').date()

        dates.append(x)

    r['lastUpdate'] = pd.DataFrame(dates)

    return r[['provinceState','countryRegion', 'lastUpdate', 'confirmed', 'confirmed_size', 'deaths', 'death_size', 'recovered', 'recovered_size', 'lat', 'long']]


if __name__ == '__main__':
    print(colorama.Fore.CYAN + f"symbol Finished: {main(date='2020-03-24')}", flush=True)