import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

x = range(4)
app.layout = html.Div([
    html.H1('Square Root Slider Graph'),
    dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
    dcc.Slider(
        id='slider-updatemode',
        marks={
            0: {'label': '0 °C', 'style': {'color': '#77b0b1'}},
            26: {'label': '26 °C'},
            37: {'label': '37 °C'},
            100: {'label': '100 °C', 'style': {'color': '#f50'}}
        },
        max=3,
        value=2,
        step=0.01,
        updatemode='drag'
    ),
    html.Div(id='updatemode-output-container', style={'margin-top': 20})
])


@app.callback([
    Output('slider-graph', 'figure'),
    Output('updatemode-output-container', 'children')
],
    [Input('slider-updatemode', 'value')])
def display_value(value):
    x = []
    for i in range(value):
        x.append(i)

    y = []
    for i in range(value):
        y.append(i * i)

    graph = go.Scatter(
        x=x,
        y=y,
        name='Manipulate Graph'
    )
    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[min(x), max(x)]),
        yaxis=dict(range=[min(y), max(y)]),
        font=dict(color='white'),

    )


    return {'data': [graph], 'layout': layout}, f'Value: {round(value, 1)} Square: {value * value}'


if __name__ == '__main__':
    app.run_server(debug=True)