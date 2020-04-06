from datetime import datetime as dt
import datetime
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from graphs.plotly_renders.current_covid_map import request_map
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
from graphs.plotly_renders.eight_day_bar_graph import animation_graph

# table = tabe_view_async.main('2020-03-20')
PLOTLY_LOGO = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Favatars3.githubusercontent.com%2Fu%2F40912998%3Fs%3D400%26v%3D4&f=1&nofb=1.png"
BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"

app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])
server = app.server
app.title = 'Covid-19 Map'

# Master Data


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
        dbc.DropdownMenuItem("Project Github", href='https://github.com/cryptopotluck/alpha_vantage_tutorial'),
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
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
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
tab_usa_map = html.Div(
    [
        dbc.Row([
            dbc.Col(html.Div(""), width=3),
            dbc.Col(html.Div(dbc.Form([
                dbc.FormGroup(
                    [
                        dbc.Label("Slider", html_for="slider"),
                        dcc.Slider(id="slider", min=1, max=1000, step=10, value=400),
                    ]
                )])), width=3),

            dbc.Col(html.H1(id='rate-slider'), width=3),
        ]),
        dbc.Row([dbc.Col(html.Div(id='rate-scale')), dbc.Col(html.Div(dcc.Graph(figure=animation_graph(data=fetch_to_date.main('2020-03-28')), style={'height': '100vh'})))]),

    ]
)


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


tab_home = dbc.Card(
    dbc.CardBody(
        [
            dbc.Col(dbc.Alert(["Stay up to date & Check Out the ", dbc.Badge("CDC Information", color="danger",
                                                                             href='https://www.cdc.gov/coronavirus/2019-ncov/',
                                                                             className="mr-1")], color="dark")),
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
                            dcc.Graph(figure=request_map(),
                                      style={'height': '100vh'}))),
                    dbc.Col(
                        html.Div(
                            dcc.Graph(figure=global_growth_graph(),
                                      style={'height': '100vh'})))]),
        ]
    ),
    className="mt-3",
)

tab_snapshot = dbc.Row(
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
        dbc.Row([dbc.Col(html.Div(id='updated-world-map', style={'height': '100vh'}), style={'width': '100vw'}),
                 dbc.Col(html.Div(id='barchart', style={'height': '100vh'}))]),
        dbc.Row([]),
        dbc.Row([dbc.Col(html.Div(), width=2), dbc.Col(html.Div(id='date-content')), dbc.Col(html.Div(), width=2)])
    ]
)

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
        dbc.Tab(tab_snapshot, label="Snapshot & Curve"),
    ]
)

"""Body"""
# rows
body = html.Div(
    [
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
    date_data = request_map_date(date)
    print()
    print('map')
    print(date_data)
    print()

    return dcc.Graph(figure=date_data, style={'height': '100vh'})


@app.callback(Output('barchart', 'children'),
              [
                  Input('date-picker-single', 'date')
              ])
def display_worldmap(date):
    date_data = three_d(date)

    return dcc.Graph(figure=date_data, style={'height': '100vh'})


@app.callback(
            Output('rate-scale', 'children'),
              [
                  Input('slider', 'value')
              ])
def slider_scale_rate(value):

    data = fetch_today.main(value=value, usa_only=True)
    date_data = request_usa_map(data)

    return dcc.Graph(figure=date_data, style={'height': '100vh'})


@app.callback(
                Output('rate-slider', 'children'),
              [
                  Input('slider', 'value')
              ])
def slider_scale_rate(value):

    return f'Scale: {value}'

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