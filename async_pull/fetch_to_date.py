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
    # Grab the Data passed through Through the function & turn into date object
    start = datetime.datetime.strptime(date, '%Y-%m-%d').date()

    # Grab today - last day of the week
    end = datetime.date.today() - start

    # Loop through dates & create a list of all the days of that week
    dates = []
    for x in range(int(end.days)):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        search_date = yesterday - datetime.timedelta(days=x)
        dates.append(search_date.strftime('%Y-%m-%d'))

    # print(dates)

    # Create the asyncio Loop
    loop: AbstractEventLoop = asyncio.new_event_loop()

    # Set as a event loop
    asyncio.set_event_loop(loop)

    # Record our Time & Start Speed Test
    t0 = datetime.datetime.now()
    print(colorama.Fore.LIGHTGREEN_EX + 'Async started:', flush=True)

    # Store Our Result
    result = loop.run_until_complete(get_covid_data(loop, dates=dates, value=value, usa_only=usa_only))

    # Finish & Announce Speed Test Results
    dt = datetime.datetime.now() - t0
    print(colorama.Fore.LIGHTGREEN_EX + "Async exiting, total time: {:,.2f} sec.".format(dt.total_seconds()), flush=True)

    return result


async def get_covid_data(loop: AbstractEventLoop, dates: list, value: int, usa_only: bool):
    tasks = []

    # Created a loop & Appended a loop_task that returns the value of get_api()
    for d in dates:
        tasks.append((loop.create_task(get_api(date=d))))

    # print(f'tasks = {tasks}')

    # Loop Through our Tasks and Start the Api Call
    finished = []
    for task in tasks:
        api = await task
        # Turn Returned Values into a Dataframe
        data = pd.DataFrame(api)
        # Throw the Dataframe into our clean_data() Function
        finished_fetch = await clean_data(data, scale=value, usa_only=usa_only)
        # Append & Return the Results
        finished.append(finished_fetch)

    return finished


async def get_api(date: str) -> str:
    # Api add date in string format
    url = f'https://covid19.mathdro.id/api/daily/{date}'

    # Async 'Magic' run Api all Return it as .json
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=ssl_context) as resp:
            resp.raise_for_status()

            api = await resp.json()
            return api


# This is where you unload the demanding changes to the initial data, add new data &
# Return the Final Cleaned Dataframe that will be Used by Plotly to Render something in app.py
async def clean_data(c_data, scale, usa_only):

    r=c_data

    # Check if user only wants to see the USA data & returns a Result
    if usa_only == True:
        usa_only = c_data['countryRegion'].str.contains('US')
        print(colorama.Fore.WHITE + f'{usa_only}')
        r = c_data[usa_only]
        print(colorama.Fore.YELLOW + f'{r}')

    # This is needed to plot the bubbles on the Plotly world map graph that we build
    r['confirmed_size'] = r.loc[:, 'confirmed'].apply(lambda x: int(x) / scale)
    r['death_size'] = r.loc[:, 'deaths'].apply(lambda x: int(x) / scale)
    r['recovered_size'] = r.loc[:, 'recovered'].apply(lambda x: int(x) / scale)

    # Demanding change; Loop Through the Dataframe Column that Holds the Date & Clean Data.
    dates = []
    for x in r['lastUpdate']:
        # The way I turn a str date value into a datetime object by checking the way the date was added to the api
        if str(x[4]) != '-':
           try:
                x = datetime.datetime.strptime(str(x[0:7]), '%m/%d/%y').date()
           except:
                x = datetime.datetime.strptime(str(x[0:6]), '%m/%d/%y').date()

        else:
            x = datetime.datetime.strptime(str(x[0:10]), '%Y-%m-%d').date()

        dates.append(x.strftime('%Y-%m-%d'))

    # Update Dataframe with the New Dates
    r['lastUpdate'] = pd.DataFrame(dates)
    # Set index as date
    r.set_index('lastUpdate')

    # Return just the columns I need from the data
    return r[['provinceState','countryRegion', 'lastUpdate', 'confirmed', 'confirmed_size', 'deaths', 'death_size', 'recovered', 'recovered_size', 'lat', 'long']]


if __name__ == '__main__':
    main(date='2020-03-24', usa_only=True)
    # print(colorama.Fore.CYAN + f"symbol Finished: {main(date='2020-03-24')}", flush=True)