import requests
from pandas import DataFrame as df
import pandas as pd
import datetime


def c_dates(date=str(datetime.date.today()-datetime.timedelta(days=1))):

    link = f'https://covid19.mathdro.id/api/daily/{date}'

    r = requests.get(link)
    r = df(r.json())


    return r


def c_d_r_Stats(ask_value):
    r = requests.get('https://covid19.mathdro.id/api')
    r = df(r.json())

    case_stats = r[ask_value]['value']

    return case_stats

def map_data():
    deaths = requests.get('https://covid19.mathdro.id/api/deaths')
    deaths = df(deaths.json())

    confirmed = requests.get('https://covid19.mathdro.id/api/confirmed')
    confirmed = df(confirmed.json())

    recovered = requests.get('https://covid19.mathdro.id/api/recovered')
    recovered = df(recovered.json())

    frames = [deaths, confirmed, recovered]

    result = pd.concat(frames)
    return result








if __name__ == '__main__':
    c_dates()

