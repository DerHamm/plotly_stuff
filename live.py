import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

import plotly
import plotly.express as px
from dash.dependencies import Input, Output

from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

COINS = 'bitcoin'
REFRESH_INTERVAL = 60

#chart = cg.get_coin_market_chart_by_id(id=COINS, vs_currency='usd', days=14)
#good_chart = []
#for t, p in chart['prices']:
#    good_chart.append([datetime.datetime.utcfromtimestamp(t / 1000), p])
#df = pd.DataFrame(good_chart)
#df.rename(columns={0: 'timestamp', 1: 'bitcoin'}, inplace=True)
#INITIAL_FRAME = df



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    html.Div([
        html.H4('Live Feed'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000*REFRESH_INTERVAL,
            n_intervals=0
        )
    ])
)


#@app.callback(Output('live-update-text', 'children'),
#              Input('interval-component', 'n_intervals'))
#def update_metrics(n):
#    lon, lat, alt = (1, 2, 3)
#    style = {'padding': '5px', 'fontSize': '16px'}
#    return [
#        html.Span('Longitude: {0:.2f}'.format(lon), style=style),
#        html.Span('Latitude: {0:.2f}'.format(lat), style=style),
#        html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
#    ]

prices = cg.get_price(ids=COINS, vs_currencies='usd')
prices['timestamp'] = datetime.datetime.now()
data = pd.DataFrame(prices)

# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    global data
    prices = cg.get_price(ids=COINS, vs_currencies='usd')
    prices['timestamp'] = datetime.datetime.now()
    df = pd.DataFrame(prices)


    data = data.append(df)
    fig = px.line(data, x='timestamp', y='bitcoin')

    # keep zoom
    fig['layout']['uirevision'] = True

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
