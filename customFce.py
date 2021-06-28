import datetime
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from app import server
from flask_caching import Cache

if "dash_cache" in os.environ:
    cache_folder = os.getenv('dash_cache')
else:
    cache_folder = "./cache/"

cache = Cache(server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': cache_folder
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