from datetime import datetime as dt
import datetime
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from graphs.plotly_renders.home.current_covid_map import request_home_map
from graphs.plotly_renders.country_lookup.candle_graph import request_candlestick
import dash_table
import dash_core_components as dcc
from graphs.BadWayToRequestData.mathdro import c_d_r_Stats
from graphs.plotly_renders.usa_map.usa_only import request_usa_map
from async_pull import fetch_today, fetch_to_date
from graphs.plotly_renders.global_growth import global_growth_graph
import os
import redis
from tasks2 import start_celery
import json
import pandas as pd
import colorama
from graphs.BadWayToRequestData.request_geo_location import grab_users_geo



# table = tabe_view_async.main('2020-03-20')
PLOTLY_LOGO = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fbigredmarkets.com%2Fwp-content%2Fuploads%2F2020%2F03%2FCovid-19.png&f=1&nofb=1"

BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"

external_scripts = [{
        'type': 'text/javascript', #depends on your application
        'src': "https://cdn.flourish.rocks/flourish-live-v4.4.1.min.js",
    }]

app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG], external_scripts=external_scripts)

server = app.server
app.title = 'Covid-19 Map'

"""------------------------------------------Data Management---------------------------------------------------------"""
port = int(os.environ.get('PORT', 6379))
listen = ['TO_Date', 'USA_Today']

TIMEOUT = 60


# Run Heroku
ON_HEROKU = os.environ.get('ON_HEROKU')
os.environ.get('ON_HEROKU')

if ON_HEROKU:
    # get the heroku port
    port = int(os.environ.get('PORT', 17995))  # as per OP comments default is 17995


redis_url = os.getenv('REDIS_URL', f'redis://localhost:{port}')

conn = redis.from_url(redis_url)

redis_instance = redis.StrictRedis.from_url(redis_url)


start_celery()

"""----------------------------------------Final Fetch----------------------------------"""
get_users_geo = grab_users_geo()

def get_growth_rate():
    jsonified_df = redis_instance.get(
        'growth_rate_data'
    ).decode("utf-8")
    df = pd.DataFrame(json.loads(jsonified_df))
    return df

def get_country(country):

    jsonified_df = redis_instance.get(
        'table_data'
    ).decode("utf-8")
    df = pd.DataFrame(json.loads(jsonified_df))

    if country == 'United States':
        return df['countryRegion'].str.contains('US')
    else:
        try:
            df2 = df['countryRegion'].str.contains(country)
            return df[df2]
        except:
            return df



def get_home_map_animation():
    today = datetime.date.today()

    week_ago = today - datetime.timedelta(days=14)
    print(week_ago)

    days = []
    while week_ago != today:
        week_ago = week_ago + datetime.timedelta(days=1)
        days.append(week_ago)

    print(f'days = {days}')

    finished_redis_fetch = []
    for day in days:
        print(f'searching redis on: {day}-dataframe')
        jsonified_df = redis_instance.get(
            f'{day}-dataframe'
        ).decode("utf-8")

        df = pd.DataFrame(json.loads(jsonified_df))
        finished_redis_fetch.append(df)

    print('This is the DF to Focus on')
    print(finished_redis_fetch)

    return finished_redis_fetch

def get_basic_country_geo():
    jsonified_df = redis_instance.get(
        'country-basic-geo-dataframe'
    ).decode("utf-8")
    df = pd.DataFrame(json.loads(jsonified_df))
    return df


def get_usa_scale_map():
    jsonified_df = redis_instance.get(
        'usa_map_data'
    ).decode("utf-8")
    df = pd.DataFrame(json.loads(jsonified_df))
    print('Anything here?')
    print(df)
    return df




# def get_home_growthrate_data():
#     """Retrieve the dataframe from Redis
#         This dataframe is periodically updated through the redis task
#         """
#     jsonified_df = redis_instance.hget(
#         tasks2.REDIS_HASH_NAME, tasks2.REDIS_KEYS["DATASET"]
#     ).decode("utf-8")
#     df = pd.DataFrame(json.loads(jsonified_df))
#     print('Focus on ME ')
#     print(df)
#     return df

# def home_map_animation():
#     """Retrieve the dataframe from Redis
#         This dataframe is periodically updated through the redis task
#         """
#     jsonified_df = redis_instance.hget(
#         tasks2.REDIS_HASH_NAME, tasks2.REDIS_KEYS["DATASET"]
#     ).decode("utf-8")
#
#     animation_list = []
#     for df in jsonified_df:
#         df = pd.DataFrame(json.loads(df))
#         animation_list.append(df)
#
#     return request_home_map(animation_list)



# # Ask For Todays Data Only
# def query_today(usa_only, scale):
#     # We should connect the last expensive data querying steps needed to render the graphs with this data
#
#     # Get Today's Date
#     date = str(datetime.date.today() - datetime.timedelta(days=1))
#
#     # Create Variable = Async Data Fetch requesting only today's dataframe
#     data = fetch_today.main(date=date, value=scale, usa_only=usa_only)
#
#     # Does this graph only want to be focused on the US?
#     if usa_only == True:
#         usa_only = data['countryRegion'].str.contains('US')
#         data = data[usa_only]
#
#     # Add to todays dataframe the bubble size needed ( x / size )
#     data['confirmed_size'] = data.loc[:, 'confirmed'].apply(lambda x: int(x) / scale)
#     data['death_size'] = data.loc[:, 'deaths'].apply(lambda x: int(x) / scale)
#     data['recovered_size'] = data.loc[:, 'recovered'].apply(lambda x: int(x) / scale)
#
#     # We name this new redis storage as USA_Today, compressing the dataframe
#     return conn.setex('USA_Today', TIMEOUT, zlib.compress(pickle.dumps(data)))
#
# #ask from date -> today's data
# def query_to_date(date, usa_only, scale):
#
#     data = fetch_to_date.main(date=date, value=scale, usa_only=usa_only)
#
#     return conn.setex('TO_Date', TIMEOUT, zlib.compress(pickle.dumps(data)))
#
# # ask for global growth rate for the right graph on the home page
# def query_global_growth_rate():
#
#     data = fetch_historic.main()
#
#     return conn.setex('Growth_Rate', TIMEOUT, zlib.compress(pickle.dumps(data)))
#
# # ask for table data
# def query_table_data():
#
#     data = fetch_snapshot_table.main('2020-04-20')
#
#     return conn.setex('Snapshot_Table', TIMEOUT, zlib.compress(pickle.dumps(data)))


"""------------------------------------------Layout------------------------------------------------------------------"""

"""Navbar"""
# dropdown Items

# make a reuseable navitem for the different examples
nav_item = dbc.NavItem(dbc.NavLink("Join the Pip Install Crew",
                                   href="https://pipinstallpython.com/"))

# make a reuseable dropdown for the different examples
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Youtube Channel",
                             href='https://www.youtube.com/channel/UC-pBvv8mzLpj0k-RIbc2Nog?view_as=subscriber'),
        dbc.DropdownMenuItem("Udemy Dash", href='https://www.udemy.com/course/plotly-dash/?referralCode=16FC11D8981E0863E557'),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Project Github", href='https://github.com/cryptopotluck/covid-country-compare'),
        dbc.DropdownMenuItem("Plotly / Dash", href='https://dash.plot.ly/'),
        dbc.DropdownMenuItem("Dash Bootstrap", href='https://dash-bootstrap-components.opensource.faculty.ai/'),
    ],
    nav=True,
    in_navbar=True,
    label="Important Links",
)

# Navbar Layout
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="40px")),
                        dbc.Col(dbc.NavbarBrand("Covid-19 Dashboard Course", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="https://plot.ly",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [nav_item,
                     dropdown,
                     ], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-5",
)



"""Tab Body"""
# Structure Top Cards
def total_data_card(request, header):
    card_content = [
        dbc.CardHeader(header),
        dbc.CardBody(
            [
                html.H5(f'{c_d_r_Stats(request):,}', className="card-title"),
            ]
        ),
    ]
    return card_content


# Home Tab
tab_home = dbc.Card(
    dbc.CardBody(
        [
            # Quick Link Useful Information
            dbc.Col(dbc.Alert([dbc.Row([

                dbc.Button("Ask r/Covid-19", color="dark",
                                                     href='https://www.amadb.xyz/',
                                                     className="mr-1"),

                dbc.Button("CDC Information", color="dark",
                                                     href='https://www.cdc.gov/coronavirus/2019-ncov/',
                                                     className="mr-1")

            ])], color="dark")),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(total_data_card(request='confirmed', header='Confirmed Cases'), color="primary", inverse=True)),
                    dbc.Col(
                        dbc.Card(total_data_card(request='recovered', header='Total Recovered'), color="success", inverse=True)),
                    dbc.Col(dbc.Card(total_data_card(request='deaths', header='Total Deaths'), color="danger", inverse=True)),
                ]),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            dcc.Graph(figure=request_home_map(get_home_map_animation()),
                                      style={'height': '75vh'})
                        ), md=12, lg=6),
                    dbc.Col(
                        html.Div(
                            dcc.Graph(figure=global_growth_graph(get_growth_rate()),
                                      style={'height': '75vh'})
                        ), md=12, lg=6)]
            ),
        ]
    ),
    className="mt-3",
)


tab_usa_map = html.Div(dbc.Card(
    dbc.CardBody(

    [
        dbc.Row([
            dbc.Col(html.Div(""), width=1),
            dbc.Col(html.Div(dbc.Form([
                dbc.FormGroup(
                    [
                        dbc.Label("Cases / Scale", html_for="slider"),
                        dcc.Slider(id="slider", min=100, max=10000, step=100, value=400),
                    ]
                )])), width=3),

            dbc.Col(html.H1(id='rate-slider',), width=3),
        ]),
        dbc.Row([dbc.Col(html.Div(id='rate-scale-map'), md=12, lg=12), dbc.Col()]),
    #              html.Div(dcc.Graph(figure=render_usa_barchart(), style={'height': '75vh'})), md=12, lg=6)]

    ]
    )
)
)



tab_snapshot = dbc.Card(
    dbc.CardBody(
    [
    dbc.Row(
    [
        # Header
        dbc.Row([dbc.Col(html.Div(), width=3),
                 dbc.Col(dcc.DatePickerSingle(
                     id='date-picker-single',
                     min_date_allowed=dt(2020, 3, 23),
                     max_date_allowed=datetime.date.today() - datetime.timedelta(days=1),
                     initial_visible_month=datetime.date.today() - datetime.timedelta(days=1),
                     date=datetime.date.today() - datetime.timedelta(days=12)
                 ), width=6),
                 dbc.Col(html.Div(), width=3)
                 ]
                ),
        # Body
        dbc.Row([
            dbc.Col(html.Div(id='updated-world-map', style={'height': '85vh'}), style={'width': '100vw'}, lg=6, md=12),
            dbc.Col(html.Div(id='barchart', style={'height': '85vh'}), lg=6, md=12)]),
        dbc.Row([]),
        dbc.Row([dbc.Col(html.Div(),  md=2, lg=2), dbc.Col(html.Div(id='date-content'),  md=8, lg=8), dbc.Col(html.Div(),  md=2, lg=2)])
    ]
)
    ]))


def get_dropdown_options():
    options = []
    df = get_basic_country_geo()
    df = df.to_dict()
    for x, y in zip(df['country'], df['name']):
        options.append({'label': df['name'][y], 'value': df['name'][y]})

    return options


tab_country_lookup = dbc.Card(
    dbc.CardBody(
        [
            # Quick Link Useful Information
            dbc.Row([
                dbc.Col(
                   dbc.FormGroup(
                    [
                        dcc.Dropdown(
                            id="country_location",
                            options=get_dropdown_options(),
                        ),
                    ]
                ), sm=6, md=3
                ),
                dbc.Col(dbc.Button("Search", color="light", id='button-search-location', className="mr-1")),
            ]),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(total_data_card(request='confirmed', header='Confirmed Cases'), color="primary", inverse=True)),
                    dbc.Col(
                        dbc.Card(total_data_card(request='recovered', header='Total Recovered'), color="success", inverse=True)),
                    dbc.Col(dbc.Card(total_data_card(request='deaths', header='Total Deaths'), color="danger", inverse=True)),
                ]),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(id='seven-day-map'
                        ), md=12, lg=6),
                    dbc.Col(
                        html.Div(id='candle-graph'
                                 ), md=12, lg=6)]
            ),
            dbc.Row([dbc.Col(html.Div(),  md=2, lg=2), dbc.Col(html.Div(id='search-location'),  md=8, lg=8), dbc.Col(html.Div(),  md=2, lg=2)])
        ]
    ),
    className="mt-3",
)

"""Table"""

tabs = dbc.Tabs(
    [
        dbc.Tab(tab_home, label="Home"),
        dbc.Tab(
            tab_usa_map, label="USA Map"
        ),
        dbc.Tab(
             tab_country_lookup, label="Country Compare"
        ),
    ]
)

"""Body"""
# rows
body = html.Div(
    [
    dbc.Toast(

            dbc.CardLink("Check Out the Home Base", href="https://pipinstallpython.com"),
            id="positioned-toast",
            header="Learn How to Build this Dashboard",
            is_open=True,
            dismissable=True,
            icon="danger",
            # top: 66 positions the toast below the navbar
            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
        ),
        dbc.Row(html.P('')),
        dbc.Row(html.Div(tabs, style={'width': '100%'})),
    ]
)

"""Layout"""

app.layout = html.Div(
    [navbar, body]
)

def get_dataframe():
    """Retrieve the dataframe from Redis
        This dataframe is periodically updated through the redis task
        """
    jsonified_df = redis_instance.get(
        'table_data'
    ).decode("utf-8")
    df = pd.DataFrame(json.loads(jsonified_df))
    print('Focus on ME ')
    print(colorama.Fore.CYAN + f"symbol Finished: {df}", flush=True)
    return df


"""Call back"""
# @app.callback(Output('date-content', 'children'),
#               [
#                   Input('date-picker-single', 'date')
#               ])
# def display_value(date):
#     # data = snapshot_table_data(date)
#     df = get_dataframe()
#     print(df)
#
#     return dash_table.DataTable(
#         id='table',
#         columns=[{'name': i, 'id': i} for i in df.columns],
#         data=df.to_dict('rows'),
#         style_header={'backgroundColor': 'rgb(30, 30, 30)'},
#         style_cell={
#             'backgroundColor': 'rgb(50, 50, 50)',
#             'color': 'white'
#         }
#     )


# @app.callback(Output('updated-world-map', 'children'),
#               [
#                   Input('date-picker-single', 'date')
#               ])
# def display_worldmap(date):
#
#     # data_last_updated = redis_instance.hget(
#     #     tasks2.REDIS_HASH_NAME, tasks2.REDIS_KEYS["DATE_UPDATED"]
#     # ).decode("utf-8")
#     # print()
#     # print('wtf are you?')
#     # print(data_last_updated)
#     # print(type(data_last_updated))
#     # print()
#     # # Add data to map
#
#     return dcc.Graph(figure='', style={'height': '85vh'})



# @app.callback(Output('barchart', 'children'),
#               [
#                   Input('date-picker-single', 'date')
#               ])
# def display_barchart(date):
#     fetch_data = fetch_to_date.main(date, usa_only=False)
#     # date_data = three_d(fetch_data)
#
#     return dcc.Graph()


@app.callback(
                Output('rate-scale-map', 'children'),
              [
                Input('slider', 'value')
              ])
def slider_scale_rate(value):

    data = fetch_today.main(value=value, usa_only=True)

    return dcc.Graph(figure=request_usa_map(data), style={'height': '85vh'})


@app.callback(
                Output('rate-slider', 'children'),
              [
                  Input('slider', 'value')
              ])
def slider_scale_rate(value):


    return f'{value}'

"""Country Lookup"""

#Render table
@app.callback(
    Output("search-location", "children"),
    [Input("button-search-location", "n_clicks"), Input('country_location', 'value')]
)
def on_button_click(n, v):
    if n is None:
        return 'None'
    else:
        print('Bookmark this location')
        df = get_country(v)
        print(df)
        for x in df.head():
            print(x)

        return dash_table.DataTable(
        id='table',
        columns=[{'name': i, 'id': i} for i in df.columns],
        data=df.to_dict('rows'),
        style_header={'backgroundColor': 'rgb(30, 30, 30)'},
        style_cell={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        })

@app.callback(
    Output("seven-day-map", "children"),
    [Input("button-search-location", "n_clicks"), Input('country_location', 'value')]
)
def on_button_click2(n, v):
    if n is None:
        return 'None'
    else:
        df = get_country(v)
        print('Bookmark this location2')



        return dcc.Graph(figure=request_home_map(get_home_map_animation(), lat=df['lat'][0], long=df['long'][0]),
                                      style={'height': '75vh'})


@app.callback(
    Output("candle-graph", "children"),
    [Input("button-search-location", "n_clicks"), Input('country_location', 'value')]
)
def on_button_click3(n, v):
    if n is None:
        return 'None'
    else:
        df = get_country(v)
        print('length Check')
        length = 0
        locations = []

        if len(df) == 1:
            locations.append({'provinceState': df['provinceState'][0], 'countryRegion': df['countryRegion'][0]})
            print('some strange shit')
            print({'provinceState': df['provinceState'][0], 'countryRegion': df['countryRegion'][0]})
            return dcc.Graph(figure=request_candlestick(get_home_map_animation(), country=locations[0]),
                             style={'height': '75vh'})
        else:
            for x in df:
                length = length + 1
                print('Sup focus on me')
                print(type(x))
                print(x)
                print(x['combinedKey'])
                print()
                print({'provinceState': x['provinceState'][0], 'countryRegion': x['countryRegion'][0]})
                locations.append({'provinceState': x['provinceState'][0], 'countryRegion': x['countryRegion'][0]})

            return dcc.Graph(figure=request_candlestick(get_home_map_animation(), country=df['combinedKey'][0]),
                                          style={'height': '75vh'})


def total_data_card(request, header):
    card_content = [
        dbc.CardHeader(header),
        dbc.CardBody(
            [
                html.H5(f'{c_d_r_Stats(request):,}', className="card-title"),
            ]
        ),
    ]
    return card_content


# we use a callback to toggle the collapse on small screens
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# the same function (toggle_navbar_collapse) is used in all three callbacks
for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

if __name__ == "__main__":
    app.run_server(debug=False, port=50630)
