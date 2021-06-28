from customFce import *
from app import app
import dash

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
    dash.dependencies.Output('sparkline-tl2', 'figure')],
    [dash.dependencies.Input('auto-refresh', 'n_intervals')])
def update_df(clicks):
    df = get_df_sqlite()

    figml = create_sparkline("Maple Leaf 1 Oz", df)
    last_update_ml = "Last update: " + str(df[df["shortname"] == "Maple Leaf 1 Oz"]["update_date"].max())

    figwp = create_sparkline("Wiener Philharmoniker 1 Oz", df)
    last_uptate_wp = "Last update: " + str(df[df["shortname"] == "Wiener Philharmoniker 1 Oz"]["update_date"].max())

    figtl2 = create_sparkline("The Yale 2 Oz", df)
    last_uptate_tl2 = "Last update: " + str(df[df["shortname"] == "The Yale 2 Oz"]["update_date"].max())

    return "Last refresh at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), last_update_ml, figml, last_uptate_wp, figwp, last_uptate_tl2, figtl2

@app.callback(
    dash.dependencies.Output('sparkline-wg2', 'figure'),
    dash.dependencies.Output('last-update-wg2', 'children'),
    dash.dependencies.Output('price-wg2', 'children'),
    dash.dependencies.Input('auto-refresh2', 'n_intervals'))
def update_box4(clicks):
    df = get_df_sqlite()
    figwg2 = create_sparkline("The Falcon 2 Oz", df)
    last_uptate_wg2 = "Last update: " + str(df[df["shortname"] == "The Falcon 2 Oz"]["update_date"].max())
    price = df[df["shortname"]=="The Falcon 2 Oz"].query("update_date == update_date.max()")["price"].values[0], " Kč"
    return  figwg2, last_uptate_wg2, price