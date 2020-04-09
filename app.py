from datetime import datetime as dt
import datetime
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from graphs.plotly_renders.time_map import request_map
from graphs.plotly_renders.current_covid_map import request_home_map

from graphs.plotly_renders.date_selected_map import request_map_date
import dash_table
import dash_core_components as dcc
from graphs.BadWayToRequestData.mathdro import c_d_r_Stats
from graphs.objects import tabe_view_data_async
from graphs.plotly_renders.three_d import three_d
from graphs.plotly_renders.usa_only import request_usa_map
from async_pull import fetch_today
from async_pull import fetch_to_date
from graphs.plotly_renders.global_growth import global_growth_graph
from graphs.plotly_renders.eight_day_bar_graph import usa_barchart
import os
from flask_caching import Cache
import pandas as pd
import redis
import zlib
import pickle


# table = tabe_view_async.main('2020-03-20')
PLOTLY_LOGO = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fbigredmarkets.com%2Fwp-content%2Fuploads%2F2020%2F03%2FCovid-19.png&f=1&nofb=1"

BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"

app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])


server = app.server
app.title = 'Covid-19 Map'



"""REDIS SETUP & DATA HOME"""
# Setup Redis Server

port = int(os.environ.get('PORT', 6379))
listen = ['TO_Date', 'USA_Today']

TIMEOUT = 140

cache = Cache(app.server, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', f'redis://localhost:{port}')
})

# Run Heroku
ON_HEROKU = os.environ.get('ON_HEROKU')
os.environ.get('ON_HEROKU')

if ON_HEROKU:
    # get the heroku port
    port = int(os.environ.get('PORT', 17995))  # as per OP comments default is 17995

# Run Local
redis_url = os.getenv('REDIS_URL', f'redis://localhost:{port}')


conn = redis.from_url(redis_url)
app.config.suppress_callback_exceptions = True

@cache.memoize(timeout=TIMEOUT)
def query_today(usa_only, scale):
    date = str(datetime.date.today() - datetime.timedelta(days=1))


    data = fetch_today.main(date=date, value=scale, usa_only=usa_only)

    if usa_only == True:
        usa_only = data['countryRegion'].str.contains('US')

        data = data[usa_only]

    data['confirmed_size'] = data.loc[:, 'confirmed'].apply(lambda x: int(x) / scale)
    data['death_size'] = data.loc[:, 'deaths'].apply(lambda x: int(x) / scale)
    data['recovered_size'] = data.loc[:, 'recovered'].apply(lambda x: int(x) / scale)
    print('why you acting up data?')
    print(data)
    print(type(data))
    print(conn.setex('USA_Today', TIMEOUT, zlib.compress(pickle.dumps(data))))
    return conn.setex('USA_Today', TIMEOUT, zlib.compress(pickle.dumps(data)))

@cache.memoize(timeout=TIMEOUT)
def query_to_date(date='2020-03-24', usa_only=False, scale=500):

    data = fetch_to_date.main(date=date, value=scale, usa_only=usa_only)

    return conn.setex('TO_Date', TIMEOUT, zlib.compress(pickle.dumps(data)))



def dataframe_usa_only_map(usa_only, scale):
    return query_today(usa_only=usa_only, scale=scale)


def dataframe_to_date(usa_only, scale, date):
    return query_to_date(usa_only=usa_only, scale=scale, date=date)

# Master Data
# q = Queue(connection=conn)
#
# worker_to_date = q.enqueue(dataframe_to_date(date='2020-03-24', usa_only=False, scale=500), redis_url)
#

"""Navbar"""
# dropdown Items

# make a reuseable navitem for the different examples
nav_item = dbc.NavItem(dbc.NavLink("Dash Udemy Course",
                                   href="https://www.udemy.com/course/plotly-dash/?referralCode=16FC11D8981E0863E557"))

# make a reuseable dropdown for the different examples
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Youtube Channel",
                             href='https://www.youtube.com/channel/UC-pBvv8mzLpj0k-RIbc2Nog?view_as=subscriber'),
        dbc.DropdownMenuItem("Potluck App", href='https://cryptopotluck.com/'),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Project Github", href='https://github.com/cryptopotluck/Covid-19-Dash-Map'),
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

# HOME

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
                                                     className="mr-1"),
                dbc.Button("Order Masks", color="dark",
                                                     href='https://www.n95breathingmask.com/',
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
                            dcc.Graph(figure=request_home_map(),
                                      style={'height': '75vh'})), md=12, lg=6),
                    dbc.Col(
                        html.Div(
                            dcc.Graph(figure=global_growth_graph(),
                                      style={'height': '75vh'})), md=12, lg=6)]),
        ]
    ),
    className="mt-3",
)


tab_usa_map = html.Div(dbc.Card(
    dbc.CardBody(

    [
        dbc.Row([
            dbc.Col(html.Div(""), width=3),
            dbc.Col(html.Div(dbc.Form([
                dbc.FormGroup(
                    [
                        dbc.Label("Cases / Scale", html_for="slider"),
                        dcc.Slider(id="slider", min=1, max=1000, step=10, value=400),
                    ]
                )])), width=3),

            dbc.Col(html.H1(id='rate-slider',), width=3),
        ]),
        dbc.Row([dbc.Col(html.Div(id='rate-scale'), md=12, lg=6), dbc.Col(html.Div(dcc.Graph(figure=usa_barchart(data=fetch_to_date.main('2020-03-28', usa_only=True)), style={'height': '75vh'})), md=12, lg=6)]),

    ]
    )
)
)


tab_snapshot =dbc.Card(
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
            dbc.Col(html.Div(id='updated-world-map', style={'height': '85vh'}), style={'width': '100vw'}),
            dbc.Col(html.Div(id='barchart', style={'height': '85vh'}))]),
        dbc.Row([]),
        dbc.Row([dbc.Col(html.Div(),  md=2, lg=2), dbc.Col(html.Div(id='date-content'),  md=8, lg=8), dbc.Col(html.Div(),  md=2, lg=2)])
    ]
)
    ]))

"""Table"""

tabs = dbc.Tabs(
    [
        dbc.Tab(tab_home, label="Home"),
        dbc.Tab(
            tab_usa_map, label="USA Map"
        ),
        # dbc.Tab(
        #     date_tabe(),
        #     label="Deaths",
        # ),
        dbc.Tab(
            "This tab's content is never seen", label="Recoveries", disabled=True
        ),
        dbc.Tab(tab_snapshot, label="Global Snapshot"),
    ]
)

"""Body"""
# rows
body = html.Div(
    [
    dbc.Toast(

            dbc.CardLink("Check Out Project Update Video", href="https://youtu.be/etWtvJC-dtQ"),
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

"""Call back"""
@app.callback(Output('date-content', 'children'),
              [
                  Input('date-picker-single', 'date')
              ])
def display_value(date):
    date_data = tabe_view_data_async.main(str(date))

    return dash_table.DataTable(
        id='table',
        columns=[{'name': i, 'id': i} for i in date_data.columns],
        data=date_data.to_dict('rows'),
        style_header={'backgroundColor': 'rgb(30, 30, 30)'},
        style_cell={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        })


@app.callback(Output('updated-world-map', 'children'),
              [
                  Input('date-picker-single', 'date')
              ])
def display_worldmap(date):

    dataframe_to_date(date=date, usa_only=False, scale=500)

    # map = request_map(date_data)
    get_redis = pickle.loads(zlib.decompress(conn.get('TO_Date')))

    # Add data to map
    data = request_map(get_redis[::-1])

    return dcc.Graph(figure=data, style={'height': '85vh'})


@app.callback(Output('barchart', 'children'),
              [
                  Input('date-picker-single', 'date')
              ])
def display_worldmap(date):
    fetch_data = fetch_to_date.main(date, usa_only=False)
    date_data = three_d(fetch_data)

    return dcc.Graph(figure=date_data, style={'height': '85vh'})

@app.callback(
            Output('rate-scale', 'children'),
              [
                  Input('slider', 'value')
              ])
def slider_scale_rate(value):
    # Run Data
    dataframe_usa_only_map(scale=value, usa_only=True)
    # Fetch from Redis
    get_redis = pickle.loads(zlib.decompress(conn.get('USA_Today')))
    print('getredis mother fucker')
    print(get_redis)
    # Add data to map
    data = request_usa_map(get_redis)

    return dcc.Graph(figure=data, style={'height': '85vh'})


@app.callback(
                Output('rate-slider', 'children'),
              [
                  Input('slider', 'value')
              ])
def slider_scale_rate(value):

    return f'{value}'

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
    app.run_server(debug=False)
