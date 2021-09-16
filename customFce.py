import datetime
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import string
import random
from flask_caching import Cache
from app import app
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

if "dash_cache" in os.environ:
    dash_cache = os.getenv('dash_cache')
else:
    dash_cache = "cache/"

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': dash_cache
    })

cache.clear()

db_file = os.getenv('db_silver')

def clear_cache():
    cache.clear()
    return True

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

def create_sparkline(df):
    ##print("####### creating sparklines #######")

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

def highlight_box(product_name):
    df = get_df_sqlite()
    df = df[df["shortname"]==product_name]
    alltimehigh = df["price"].max()
    df = df[df["update_date"] >= (df["update_date"].max() - pd.DateOffset(30, 'D'))].sort_values("update_date")
    
    df_products = get_products()
    letters = string.ascii_lowercase
    randomstr = ''.join(random.choice(letters) for i in range(3))
    html_block = dbc.Row([
                        dbc.Col([
                            html.Img(id='image-coin-' + randomstr, src=df_products[df_products["shortname"] == product_name]["imgurl"].values[0], className="img-fluid")
                        ], width={"size":3}, className="my-auto"),
                        dbc.Col([
                            html.H3(product_name),
                            dbc.Col([
                                html.Div(id="last-update-" + randomstr, children=["Last update: " + str(df["update_date"].max())]),
                                dcc.Graph(id="sparkline-" + randomstr, figure=create_sparkline(df), config=dict(displayModeBar=False, staticPlot=True), style={"width":"200px", "height":"50px", "float":"left"}),
                                html.H4(id="price-" + randomstr, children=[df.query("update_date == update_date.max()")["price"].values[0], " Kč"], style={"height":"50px"}),
                                dcc.Link(children=["Přejít na produkt"], href=df_products[df_products["shortname"]==product_name]["url"].values[0], target="_blank")
                            ], width={"size":8}, className="float-left"),
                            dbc.Col([
                                html.Div([
                                    html.Span(["All time high: "]),
                                    html.B([str(alltimehigh)]),
                                    html.P()
                                ]),
                                html.Div([
                                    html.Span(["30 day MAX: "]),
                                    html.B([str(df["price"].max())])
                                ]),
                                html.Div([
                                    html.Span(["30 day MIN: "]),
                                    html.B([str(df["price"].min())])
                                ])
                            ], width={"size":4}, className="my-auto float-right")
                        ]),
                        
                    ], className="border border-primary rounded ml-2 py-2")
    return html_block