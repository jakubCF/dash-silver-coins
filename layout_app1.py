import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from customFce import *

def serve_layout_app1():
    df = get_df_sqlite()
    df_products = get_products()
    df_rates = get_df_rates()
    layout = dbc.Container([
        dcc.Interval(id = "auto-refresh", interval = 60*1000),
        dcc.Interval(id = "auto-refresh2", interval = 60*1000),
        dcc.Interval(id = "auto-refresh-third-row", interval = 60*1000),
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
                        html.H4(children=[df[df["shortname"]=="Maple Leaf 1 Oz"].query("update_date == update_date.max()")["price"].values[0], " Kč"], style={"height":"50px"}),
                        dcc.Link(children=["Přejít na produkt"], href=df_products[df_products["shortname"]=="Maple Leaf 1 Oz"]["url"].values[0], target="_blank")
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
                        html.H4(children=[df[df["shortname"]=="Wiener Philharmoniker 1 Oz"].query("update_date == update_date.max()")["price"].values[0], " Kč"], style={"height":"50px"}),
                        dcc.Link(children=["Přejít na produkt"], href=df_products[df_products["shortname"]=="Wiener Philharmoniker 1 Oz"]["url"].values[0], target="_blank")
                    ], width={"size":9})
                ], className="border border-primary rounded ml-2 py-2")
            ], width={"size":5})
        ], justify="center", className="mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Img(id='image-tl2', src=df_products[df_products["shortname"] == "The Yale 2 Oz"]["imgurl"].values[0], className="img-fluid")
                    ], width={"size":3}, className="my-auto"),
                    dbc.Col([
                        html.H3("The Yale 2 Oz"),
                        html.Div(id="last-update-tl2"),
                        dcc.Graph(id="sparkline-tl2", config=dict(displayModeBar=False, staticPlot=True), style={"max-width":"200px", "height":"50px", "float":"left"}),
                        html.H4(children=[df[df["shortname"]=="The Yale 2 Oz"].query("update_date == update_date.max()")["price"].values[0], " Kč"], style={"height":"50px"}),
                        dcc.Link(children=["Přejít na produkt"], href=df_products[df_products["shortname"]=="The Yale 2 Oz"]["url"].values[0], target="_blank")
                    ], width={"size":9})
                ], className="border border-primary rounded mr-2 py-2")
            ], width={"size":5}),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Img(id='image-coin-wg2', src=df_products[df_products["shortname"] == "The Falcon 2 Oz"]["imgurl"].values[0], className="img-fluid")
                    ], width={"size":3}, className="my-auto"),
                    dbc.Col([
                        html.H3("The Falcon 2 Oz"),
                        html.Div(id="last-update-wg2"),
                        dcc.Graph(id="sparkline-wg2", config=dict(displayModeBar=False, staticPlot=True), style={"max-width":"200px", "height":"50px", "float":"left"}),
                        html.H4(id="price-wg2", children=[df[df["shortname"]=="The Falcon 2 Oz"].query("update_date == update_date.max()")["price"].values[0], " Kč"], style={"height":"50px"}),
                        dcc.Link(children=["Přejít na produkt"], href=df_products[df_products["shortname"]=="The Falcon 2 Oz"]["url"].values[0], target="_blank")
                    ], width={"size":9})
                ], className="border border-primary rounded ml-2 py-2")
            ], width={"size":5})
        ], justify="center", className="mb-3"),
        dbc.Row([], id="third-row", justify="center", className="mb-3"),
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
