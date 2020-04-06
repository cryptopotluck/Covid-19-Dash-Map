import requests
from pandas import DataFrame as df
import plotly.graph_objects as go

def request_map_data():
    r = requests.get('https://coronavirus-tracker-api.herokuapp.com/v2/locations')

    r = df(r.json()['locations'])

    deaths = []
    death_size = []
    confirmed = []
    confirmed_size = []
    recovered = []
    recovered_size = []
    for x in r['latest']:
        confirmed.append(x['confirmed'])
        confirmed_size.append(abs(float(x['confirmed']) / 500))
        deaths.append(x['deaths'])
        death_size.append(abs(float(x['deaths']) / 100))
        recovered.append(x['recovered'])
        recovered_size.append(abs(float(x['recovered']) / 500))

    lon = []
    lat = []
    for x in r['coordinates']:
        lon.append(x['longitude'])
        lat.append(x['latitude'])

    r['confirmed'] = df(confirmed)
    r['confirmed_size'] = df(confirmed_size)
    r['deaths'] = df(deaths)
    r['death_size'] = df(death_size)
    r['recovered'] = df(recovered)
    r['recovered_size'] = df(recovered_size)
    r['lat'] = df(lat)
    r['lon'] = df(lon)
    return r

if __name__ == '__main__':
    print(request_map_data())

