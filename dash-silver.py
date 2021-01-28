# To add a new cell, type '# '
# To add a new markdown cell, type '#  [markdown]'
#  [markdown]
# # Initialize DASH and create simple plot #

# 
import datetime
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from flask_caching import Cache
import os


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache'
    })

cache.clear()
#  [markdown]
# Get data from DB to pandas

# 
db_file = os.getenv('db_silver')

@cache.memoize(timeout=300)
def get_df_sqlite():
    df = pd.DataFrame()
    # 
    conn = sqlite3.connect(db_file)
    query = '''SELECT products.name, coins_price.price, coins_price.update_date, coins_price.product_id, products.shortname 
        FROM coins_price JOIN products ON coins_price.product_id = products.id'''

    df = pd.read_sql_query(query, conn, parse_dates="update_date")
    return df.sort_values("update_date")

@cache.memoize(timeout=300)
def get_df_rates():
    conn = sqlite3.connect(db_file)
    query = '''SELECT * FROM rates'''
    df_rates = pd.read_sql_query(query, conn, parse_dates="update_date")
    df_rates["oz_czk"] = round((df_rates["oz_usd"] * df_rates["czk_usd"]), 2)
    return df_rates.sort_values("update_date")
    

@cache.memoize(timeout=300)
def get_grouped():

    df = get_df_sqlite()
    
    df = df.set_index("update_date")
    df = df.groupby([df["shortname"], df.index.year, df.index.month, df.index.day])["price"].agg([
        "max", "min", "last", "first"]).rename_axis(["coin","year", "month", "day"]).reset_index(level=[0,1,2,3])
    df = df.set_index(pd.to_datetime(df[["year","month","day"]])).drop(["year","month","day"], axis=1)
    return df

@cache.memoize(timeout=60*60)
def get_products():
    conn = sqlite3.connect(db_file)
    query2 = "SELECT *  FROM products"
    df_products = pd.read_sql_query(query2, conn)
    df_products = df_products.sort_values(by=['shortname'])
    return df_products


## Get unique list of products - obsolent
# names = df["name"].tolist()
# ddnames = set(names)
# options_list = []
# for ddname in ddnames:
#     options_list.append({"label": ddname, "value": ddname})

def create_sparkline(shortname, df):

    df = df[df["shortname"] == shortname]
    df = df[df["update_date"] >= (df["update_date"].max() - pd.DateOffset(30, 'D'))].sort_values("update_date")

    fig_sparkline = px.line(df, x="update_date", y="price",
        labels={"price":"Price", "update_date":"Date"}, height= 50)
    fig_sparkline.update_xaxes(visible=False, fixedrange=True)
    fig_sparkline.update_yaxes(visible=False, fixedrange=True)
    fig_sparkline.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(t=10,l=10,b=10,r=10),
        hovermode=False
    )
    return fig_sparkline

def serve_layout():
    df = get_df_sqlite()
    df_products = get_products()
    df_rates = get_df_rates()
    layout = dbc.Container([
        dcc.Interval(id = "auto-refresh", interval = 60*60*1000),
        html.Div(id='refresh-status'),
        dbc.Row([
            dbc.Col([html.H2('Dash - Silver Coins Price', className="text-center mt-3"),
                html.P('''Visualising time series with Plotly - Dash''', className="text-center mb-3")
            ], width={"size":10})
        ], justify="center"),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Img(id='image-mapleleaf', src=df_products[df_products["shortname"] == "Maple Leaf 1 Oz"]["imgurl"].values[0], className="img-fluid")
                    ], width={"size":3}, className="my-auto"),
                    dbc.Col([
                        html.H3("Maple Leaf 1 Oz"),
                        html.Div(id="last-update-ml"),
                        dcc.Graph(id="sparkline-ml", config=dict(displayModeBar=False, staticPlot=True), style={"max-width":"200px", "height":"50px", "float":"left"}),
                        html.H4(children=[df[df["shortname"]=="Maple Leaf 1 Oz"].query("update_date == update_date.max()")["price"].values[0], " Kč"])
                    ], width={"size":9})
                ], className="border border-primary rounded mr-2 py-2")
            ], width={"size":5}),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Img(id='image-coin-wiener', src=df_products[df_products["shortname"] == "Wiener Philharmoniker 1 Oz"]["imgurl"].values[0], className="img-fluid")
                    ], width={"size":3}, className="my-auto"),
                    dbc.Col([
                        html.H3("Wiener Philharmoniker 1 Oz"),
                        html.Div(id="last-update-wp"),
                        dcc.Graph(id="sparkline-wp", config=dict(displayModeBar=False, staticPlot=True), style={"max-width":"200px", "height":"50px", "float":"left"}),
                        html.H4(children=[df[df["shortname"]=="Wiener Philharmoniker 1 Oz"].query("update_date == update_date.max()")["price"].values[0], " Kč"])
                    ], width={"size":9})
                ], className="border border-primary rounded ml-2 py-2")
            ], width={"size":5})
        ], justify="center", className="mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Img(id='image-tl2', src=df_products[df_products["shortname"] == "The Lion 2 Oz"]["imgurl"].values[0], className="img-fluid")
                    ], width={"size":3}, className="my-auto"),
                    dbc.Col([
                        html.H3("The Lion 2 Oz"),
                        html.Div(id="last-update-tl2"),
                        dcc.Graph(id="sparkline-tl2", config=dict(displayModeBar=False, staticPlot=True), style={"max-width":"200px", "height":"50px", "float":"left"}),
                        html.H4(children=[df[df["shortname"]=="The Lion 2 Oz"].query("update_date == update_date.max()")["price"].values[0], " Kč"])
                    ], width={"size":9})
                ], className="border border-primary rounded mr-2 py-2")
            ], width={"size":5}),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Img(id='image-coin-wg2', src=df_products[df_products["shortname"] == "The White Greyhound 2 Oz"]["imgurl"].values[0], className="img-fluid")
                    ], width={"size":3}, className="my-auto"),
                    dbc.Col([
                        html.H3("The White Greyhound 2 Oz"),
                        html.Div(id="last-update-wg2"),
                        dcc.Graph(id="sparkline-wg2", config=dict(displayModeBar=False, staticPlot=True), style={"max-width":"200px", "height":"50px", "float":"left"}),
                        html.H4(children=[df[df["shortname"]=="The White Greyhound 2 Oz"].query("update_date == update_date.max()")["price"].values[0], " Kč"])
                    ], width={"size":9})
                ], className="border border-primary rounded ml-2 py-2")
            ], width={"size":5})
        ], justify="center", className="mb-3"),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='dropdown-chart',
                    options=[{"label":shortname, "value":shortname}
                        for shortname in df_products["shortname"]],
                    multi=False,
                    clearable=False,
                    value='Maple Leaf 1 Oz',
                    className="ml-5 float-dropdown"
                    ),
                dbc.RadioItems(
                    id="radio-chart",
                    options=[
                        {'label': 'Line Chart', 'value': 'line'},
                        {'label': 'OHLC Chart', 'value': 'ohlc'}
                    ],
                    value='line',
                    className="btn-group btn-group-toggle",
                    labelClassName="btn btn-secondary",
                    labelCheckedClassName="btn btn-secondary active"
                ), 
                dcc.Graph(id='graph-container')
            ], width={"size":7}),
            dbc.Col([
                html.Img(id='image-coin'),
            ], width={"size":3}, className="my-auto text-center")
        ], justify="center", className="mt-5 border rounded mx-3 py-4"),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='dropdown-rates',
                    options=[{"label":"OZ/USD", "value":"oz_usd"},{"label":"OZ/CZK", "value":"oz_czk"},{"label":"USD/CZK", "value":"czk_usd"}],
                    multi=False,
                    clearable=False,
                    value='oz_usd',
                    className="ml-5",
                    style={"max-width":"300px"}
                    ), 
                dcc.Graph(id='graph-rates')
            ], width={"size":7}),
        ], justify="center", className="mt-5 border rounded mx-3 py-4")  
    ], fluid=True)

    return layout

app.layout = serve_layout

@app.callback(
    dash.dependencies.Output('graph-rates', 'figure'),
    [dash.dependencies.Input('dropdown-rates', 'value')])
def update_output(value):
    df_rates = get_df_rates()
    fig = px.line(df_rates, x = "update_date", y = value)
    return fig

@app.callback(
    [dash.dependencies.Output('image-coin', 'src'),
    dash.dependencies.Output('graph-container', 'figure')],
    [dash.dependencies.Input('dropdown-chart', 'value'),
    dash.dependencies.Input('radio-chart', 'value')])
def update_output(value, radio):
    df = get_grouped()
    df_products = get_products()
    selected_df = df[df["coin"]==value]

    if radio == "line":
        fig = px.line(selected_df, x=selected_df.index, y="last",
            labels={"last":"Price", "index":"Date"})

    elif radio == "ohlc":
        fig = go.Figure(data=[go.Candlestick(x=selected_df.index,
                    open=selected_df['first'],
                    high=selected_df['max'],
                    low=selected_df['min'],
                    close=selected_df['last'])])
    else:
        fig = []
    
    url = df_products[df_products["shortname"] == value]["imgurl"].values[0]
    return url, fig

@app.callback([
    dash.dependencies.Output('refresh-status', 'children'),
    dash.dependencies.Output('last-update-ml', 'children'),
    dash.dependencies.Output('sparkline-ml', 'figure'),
    dash.dependencies.Output('last-update-wp', 'children'),
    dash.dependencies.Output('sparkline-wp', 'figure'),
    dash.dependencies.Output('last-update-tl2', 'children'),
    dash.dependencies.Output('sparkline-tl2', 'figure'),
    dash.dependencies.Output('last-update-wg2', 'children'),
    dash.dependencies.Output('sparkline-wg2', 'figure')],
    [dash.dependencies.Input('auto-refresh', 'n_intervals')])
def update_df(clicks):
    df = get_df_sqlite()

    figml = create_sparkline("Maple Leaf 1 Oz", df)
    last_update_ml = "Last update: " + str(df[df["shortname"] == "Maple Leaf 1 Oz"]["update_date"].max())

    figwp = create_sparkline("Wiener Philharmoniker 1 Oz", df)
    last_uptate_wp = "Last update: " + str(df[df["shortname"] == "Wiener Philharmoniker 1 Oz"]["update_date"].max())

    figtl2 = create_sparkline("The Lion 2 Oz", df)
    last_uptate_tl2 = "Last update: " + str(df[df["shortname"] == "The Lion 2 Oz"]["update_date"].max())

    figwg2 = create_sparkline("The White Greyhound 2 Oz", df)
    last_uptate_wg2 = "Last update: " + str(df[df["shortname"] == "The White Greyhound 2 Oz"]["update_date"].max())

    return "Last refresh at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), last_update_ml, figml, last_uptate_wp, figwp, last_uptate_tl2, figtl2, last_uptate_wg2, figwg2


if __name__ == '__main__':
    app.run_server(host = "0.0.0.0", port = 8090, dev_tools_ui=True, debug=True,
              dev_tools_hot_reload =True, threaded=True)

