import requests
from pandas import DataFrame as df


def total(ask_value):
    r = requests.get('https://covid2019-api.herokuapp.com/v2/total')
    r = df(r.json())

    return r['data'][ask_value]


if __name__ == '__main__':
    print(total('confirmed'))
