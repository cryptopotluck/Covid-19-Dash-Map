import requests
import pandas as pd
import colorama
import csv
import sys
import pygeoip
import geoip2.webservice
import geocoder
import ssl
import certifi

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())

def pygeo_test():
    my_ip_address = requests.get('https://api.ipifly.org').text

    gip = pygeoip.GeoIP('GeoLiteCity.dat')
    res = gip.record_by_addr(my_ip_address)
    print(res)

    return res


def grab_users_geo():
    url = "https://geoplugin.p.rapidapi.com/ip/json.gp"

    querystring = {"ip":"IPv4%20or%20IPv6%20address"}

    headers = {
        'x-rapidapi-host': "geoplugin.p.rapidapi.com",
        'x-rapidapi-key': "70e2388a24msh461fdbee95e5d4ep1d6c45jsnfaaaf5710f9a"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()

    df = pd.DataFrame(response, index=[0])

    return df


def grab_country_df_location():
    g = geocoder.google('Mountain View, CA')
    print(g)

    return g.latlng


if __name__ == '__main__':

    """grab_country_df_location"""
    country_location_test = grab_country_df_location()
    print(country_location_test)
    print(f'Type: {type(country_location_test)}')


    # get_user_geo_test = grab_users_geo()
    # print(f'Returns: {get_user_geo_test}')
    # print(f'Type: {type(get_user_geo_test)}')
    #
    # for x in get_user_geo_test:
    #     print(colorama.Fore.LIGHTGREEN_EX + f'{x}: ' + colorama.Fore.CYAN +f'{get_user_geo_test[x][0]}')
    #
    # for key, val in res.items():
    #     print(colorama.Fore.LIGHTGREEN_EX + f'{key}: ' + colorama.Fore.CYAN +f'{val}')
    #
    # try:
    #     print("Scanning list of IPs ")
    #
    #     with open('ip-list.csv', 'r',newline='') as input_file:
    #
    #         with open('ip-list-updated.csv', 'w',newline='') as output_file:
    #
    #             ip_reader = csv.reader(input_file, delimiter=' ')
    #             print(ip_reader)
    #
    #             ip_writer = csv.writer(output_file)
    #             print(ip_writer)
    #
    #             api_response = get_user_geo_test
    #
    #             current_ip = api_response['get_user_geo_test']
    #             print(f"Getting details for IP: {current_ip}")
    #             ip_city = api_response["geoplugin_city"] if api_response["geoplugin_city"] != '' else api_response["geoplugin_region"][0]
    #             ip_country = api_response["geoplugin_countryName"]
    #             ip_latitude = api_response["geoplugin_latitude"]
    #             ip_longitude = api_response["geoplugin_longitude"]
    #             print([current_ip, ip_city, ip_country, ip_latitude, ip_longitude])
    #             ip_writer.writerow([current_ip, ip_city, ip_country, ip_latitude, ip_longitude])
    #
    #             output_file.close()
    #
    #             input_file.close()
    #
    #
    # except TypeError as e:
    #
    #     print(e)
    #     print("Type Error...Aborting")
    #
    # except csv.Error as e:
    #
    #     print(e)
    #     print("CSV Error...Aborting")
    #
    # except Exception as e:
    #
    #     print("Major Exception ...Aborting")
    #     sys.exit(e)