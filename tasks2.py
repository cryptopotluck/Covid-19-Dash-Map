import datetime
import os
import redis
from celery import Celery
import json
import plotly
from functools import reduce
import pandas as pd
from async_pull import fetch_today, fetch_historic, fetch_to_date, fetch_snapshot_table
from graphs.BadWayToRequestData.request_geo_location import grab_users_geo
port = int(os.environ.get('PORT', 6379))
import colorama
import requests
from bs4 import BeautifulSoup


# Run Heroku
ON_HEROKU = os.environ.get('ON_HEROKU')
os.environ.get('ON_HEROKU')

if ON_HEROKU:
    # get the heroku port
    port = int(os.environ.get('PORT', 17995))  # as per OP comments default is 17995


redis_url = os.getenv('REDIS_URL', f'redis://localhost:{port}')

celery_app = Celery("Celery App", broker=redis_url)

redis_instance = redis.StrictRedis.from_url(redis_url)

REDIS_HASH_NAME = os.environ.get("DASH_APP_NAME", "app-data")
REDIS_KEYS = {"DATASET": 'DATASET', "DATE_UPDATED": "DATE_UPDATED"}

"""Management"""
"""Start"""
@celery_app.on_after_configure.connect
def start_celery(**kwargs):
        # snapshot_table_data()
        map_today_data(usa_only=False, scale=400)
        # home_animation_data()
        render_growth_rate_data()
        dataframe_to_date()
        scrape_google_task()






"""Example"""
# @celery_app.task
# def update_data():
#     print("----> update_data")
#     # Create a dataframe with sample data
#     # In practice, this function might be making calls to databases,
#     # performing computations, etc
#     N = 100
#     df = pd.DataFrame(
#         {
#             "time": [
#                 datetime.datetime.now() - datetime.timedelta(seconds=i)
#                 for i in range(N)
#             ],
#             "value": np.random.randn(N),
#         }
#     )
#
#     # Save the dataframe in redis so that the Dash app, running on a separate
#     # process, can read it
#     redis_instance.hset(
#         REDIS_HASH_NAME,
#         REDIS_KEYS["DATASET"],
#         json.dumps(
#             df.to_dict(),
#             # This JSON Encoder will handle things like numpy arrays
#             # and datetimes
#             cls=plotly.utils.PlotlyJSONEncoder,
#         ),
#     )
#     # Save the timestamp that the dataframe was updated
#     redis_instance.hset(
#         REDIS_HASH_NAME, REDIS_KEYS["DATE_UPDATED"], str(datetime.datetime.now())
#     )

# @celery_app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     print("----> setup_periodic_tasks")
#     sender.add_periodic_task(
#         45,  # seconds
#         # an alternative to the @app.task decorator:
#         # wrap the function in the app.task function
#         # usa_barchart_data.s(),
#         snapshot_table_data.s(),
#         usa_map_data.s(),
#         home_animation_data.s(),
#         render_growth_rate_data.s(),
#         dataframe_to_date.s(),
#         name="GroupTask",
#     )


# render table
# @celery_app.task
# def snapshot_table_data(date='2020-03-20'):
#         df_list = fetch_snapshot_table.main(date)
#
#         redis_instance.set(
#             'table_data',
#             json.dumps(
#                 df_list.to_dict(),
#                 # This JSON Encoder will handle things like numpy arrays
#                 # and datetimes
#                 cls=plotly.utils.PlotlyJSONEncoder,
#             ),
#         )
#         # Save the timestamp that the dataframe was updated
#         redis_instance.hset(
#         REDIS_HASH_NAME, REDIS_KEYS["DATASET"], f'{str(datetime.datetime.now())}')

# """Start"""
# @celery_app.on_after_configure.connect
# def snapshot_table_task(sender, **kwargs):
#     print("----> setup_periodic_tasks")
#     sender.add_periodic_task(
#         45,  # seconds
#         # an alternative to the @app.task decorator:
#         # wrap the function in the app.task function
#         snapshot_table_data.s(),
#         name="snapshot_table_data",
#     )


@celery_app.task
def map_today_data(usa_only, scale):
    # We should connect the last expensive data querying steps needed to render the graphs with this data

    # Get Today's Date
    date = str(datetime.date.today() - datetime.timedelta(days=1))

    # Create Variable = Async Data Fetch requesting only today's dataframe
    data = fetch_today.main(date=date, value=scale, usa_only=usa_only)

    # Does this graph only want to be focused on the US?
    if usa_only == True:
        usa_only = data['countryRegion'].str.contains('US')
        data = data[usa_only]

    df = data

    print('check df')
    print(df)

    redis_instance.set(
        f'today-dataframe',
        json.dumps(
            df.to_dict(),
            # This JSON Encoder will handle things like numpy arrays
            # and datetimes
            cls=plotly.utils.PlotlyJSONEncoder,
        ),
    )


"""Start"""
@celery_app.on_after_configure.connect
def usa_map_task(sender, **kwargs):
    print("----> setup_periodic_tasks")
    sender.add_periodic_task(
        45,  # seconds
        # an alternative to the @app.task decorator:
        # wrap the function in the app.task function
        map_today_data.s(),
        name="usa_map_data",
    )


@celery_app.task
def render_growth_rate_data():

    df = fetch_historic.main()

    redis_instance.set(
        'growth_rate_data',
        json.dumps(
            df.to_dict(),
            # This JSON Encoder will handle things like numpy arrays
            # and datetimes
            cls=plotly.utils.PlotlyJSONEncoder,
        ),
    )

"""Start"""
@celery_app.on_after_configure.connect
def growth_rate_task(sender, **kwargs):
    print("----> setup_periodic_tasks")
    sender.add_periodic_task(
        45,  # seconds
        # an alternative to the @app.task decorator:
        # wrap the function in the app.task function
        render_growth_rate_data.s(),
        name="render_growth_rate_data",
    )

@celery_app.task
def dataframe_to_date(usa_only=False, scale=1000):
    # We should connect the last expensive data querying steps needed to render the graphs with this data

    # Get Today's Date
    today = datetime.date.today()

    # Get the date 7 days ago
    week_ago = today - datetime.timedelta(days=60)

    # Create Variable = Async Data Fetch requesting date
    df_list = fetch_to_date.main(date=str(week_ago), value=scale, usa_only=usa_only)
    # returns a list [df1, df2, ... df7]

    # loop through the list
    for df in df_list:

        print(f'Building Redis Storage on: {df["lastUpdate"][0]}-dataframe')

        # Creates a redis instence to store data, turns df to dictionary & encodes in json
        redis_instance.set(
            f'{df["lastUpdate"][0]}-dataframe',
            json.dumps(
                df.to_dict(),
                # This JSON Encoder will handle things like numpy arrays
                # and datetimes
                cls=plotly.utils.PlotlyJSONEncoder,
            ),
        )

"""Start"""
@celery_app.on_after_configure.connect
def dataframe_to_date_task(sender, **kwargs):
    print("----> setup_periodic_tasks")
    sender.add_periodic_task(
        45,  # seconds
        # an alternative to the @app.task decorator:
        # wrap the function in the app.task function
        dataframe_to_date.s(),
        name="dataframe_to_date",
    )

@celery_app.task
def scrape_google_task():
    # We should connect the last expensive data querying steps needed to render the graphs with this data
    source = requests.get('https://developers.google.com/public-data/docs/canonical/countries_csv')
    soup = BeautifulSoup(source.text, 'html.parser')

    data = []
    for tr in soup.find_all('tr'):
        values = [td.text for td in tr.find_all('td')]
        data.append(values)

    countries = pd.DataFrame(data[1::])

    countries.rename(columns={0: 'country', 1: 'latitude', 2: 'longitude', 3: 'name'}, inplace=True)

    redis_instance.set(
            f'country-basic-geo-dataframe',
            json.dumps(
                countries.to_dict(),
                # This JSON Encoder will handle things like numpy arrays
                # and datetimes
                cls=plotly.utils.PlotlyJSONEncoder,
            ),
        )

    """Start"""

@celery_app.on_after_configure.connect
def dataframe_scrape_google_task(sender, **kwargs):
    print("----> setup_periodic_tasks")
    sender.add_periodic_task(
        45,  # seconds
        # an alternative to the @app.task decorator:
        # wrap the function in the app.task function
        dataframe_to_date.s(),
        name="country-basic-geo-dataframe",
    )



    #
    # # Get the date 7 days ago
    # week_ago = today - datetime.timedelta(days=7)
    #
    # # Create Variable = Async Data Fetch requesting date
    # df_list = fetch_to_date.main(date=str(week_ago), value=scale, usa_only=usa_only)
    # # returns a list [df1, df2, ... df7]
    #
    # # loop through the list
    # for df in df_list:
    #
    #     print(f'Building Redis Storage on: {df["lastUpdate"][0]}-dataframe')
    #
    #     # Creates a redis instence to store data, turns df to dictionary & encodes in json
    #     redis_instance.set(
    #         f'{df["lastUpdate"][0]}-dataframe',
    #         json.dumps(
    #             df.to_dict(),
    #             # This JSON Encoder will handle things like numpy arrays
    #             # and datetimes
    #             cls=plotly.utils.PlotlyJSONEncoder,
    #         ),
    #     )

"""Start"""
@celery_app.on_after_configure.connect
def dataframe_to_date_task(sender, **kwargs):
    print("----> setup_periodic_tasks")
    sender.add_periodic_task(
        45,  # seconds
        # an alternative to the @app.task decorator:
        # wrap the function in the app.task function
        dataframe_to_date.s(),
        name="dataframe_to_date",
    )


if __name__ == "__main__":
    def get_basic_country_geo():
        jsonified_df = redis_instance.get(
            'country-basic-geo-dataframe'
        ).decode("utf-8")
        df = pd.DataFrame(json.loads(jsonified_df))
        return df

    def get_dropdown_options():
        options = []
        df = get_basic_country_geo()
        df=df.to_dict()
        for x, y in zip(df['country'], df['name']):
            options.append({'country_code': df['country'][x], 'country': df['name'][y]})

        return options

    get_basic_country_geo()
    get_dropdown_options()