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


def main(country='USA', value=400):
    # Create the asyncio Loop
    loop: AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    t0 = datetime.datetime.now()
    print(colorama.Fore.LIGHTGREEN_EX + 'App started', flush=True)
    result = loop.run_until_complete(get_covid_data(loop, country=country, value=value))
    dt = datetime.datetime.now() - t0
    print(colorama.Fore.LIGHTGREEN_EX + "App exiting, total time: {:,.2f} sec.".format(dt.total_seconds()), flush=True)
    return result


async def get_covid_data(loop: AbstractEventLoop, country: str, value: int):
    tasks = []


    tasks.append((loop.create_task(get_api(country=country))))

    print(f'tasks = {tasks}')
    finished = []
    for task in tasks:
        api = await task
        # print('--------------')
        data = pd.DataFrame(api)
        # print(data)
        # print('--------------')
        finished_fetch = await clean_data(data, scale=value, country=country)
        finished.append(finished_fetch)

    print(colorama.Fore.WHITE + f"Task Finished: {finished[0]}", flush=True)
    return finished[0]


async def get_api(country: str) -> str:

    url = f'https://covid19.mathdro.id/api/countries/{country}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=ssl_context) as resp:
            resp.raise_for_status()

            api = await resp.json()
            return api

async def get_api_c_r_d(country: str) -> str:

    url_c = f'https://covid19.mathdro.id/api/countries/{country}/confirmed/'
    url_r = f'https://covid19.mathdro.id/api/countries/{country}/recovered/'
    url_d = f'https://covid19.mathdro.id/api/countries/{country}/deaths/'

    df = []
    async with aiohttp.ClientSession() as session:
        for url in [url_c, url_d, url_r]:
            async with session.get(url, ssl=ssl_context) as resp:
                resp.raise_for_status()

                api = await resp.json()
                df.append(api)

    print(pdf)
    return df


async def clean_data(data, scale, country):

    c_r_d_overview = []
    for x in data.head():
        c_r_d_overview.append({x:data[x][0]})

    print(c_r_d_overview)



    # if country == 'USA':
    #     usa_only = data['countryRegion'].str.contains('US')
    #     data = data[usa_only]


    # data['confirmed_size'] = data.loc[:, 'confirmed'].apply(lambda x: int(x) / scale)
    # data['death_size'] = data.loc[:, 'deaths'].apply(lambda x: int(x) / scale)
    # data['recovered_size'] = data.loc[:, 'recovered'].apply(lambda x: int(x) / scale)

    return data


if __name__ == '__main__':
    start_script = main(country='USA')
    print(colorama.Fore.CYAN + f"symbol Finished: {start_script}", flush=True)





