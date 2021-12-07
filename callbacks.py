
from customFce import *
import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from app import app

@app.callback(
    Output('refresh-status', 'children'),
    Input('auto-refresh2', 'n_intervals')
)
def update_dfall(clicks):

    if int(datetime.datetime.now().strftime("%M")) == 40:
        clear_cache()
        # print("Cache clearing successful " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return "Last refresh at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        # print("No cache clearing " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        raise PreventUpdate

@app.callback(
    Output('st-col-one', 'children'),
    Output('st-col-two', 'children'),
    Output('nd-col-one', 'children'),
    Output('nd-col-two', 'children'),
    Output('rd-col-one', 'children'),
    Output('rd-col-two', 'children'),
    Input('auto-refresh-third-row', 'n_intervals')
)
def third_row(clicks):
    ####
    #### The White Horse 2 Oz
    #### The White Greyhound 2 Oz
    #### The Queen´s Beasts 2 Oz
    ####
    html_block1 = highlight_box("Maple Leaf 1 Oz")
    html_block2 = highlight_box("Wiener Philharmoniker 1 Oz") #+ highlight_box("The White Horse 2 Oz")
    html_block3 = highlight_box("Bull 2 Oz")
    html_block4 = highlight_box("The Yale 2 Oz")
    html_block5 = highlight_box("The White Horse 2 Oz")
    html_block6 = highlight_box("The White Greyhound 2 Oz")
    return html_block1, html_block2, html_block3, html_block4, html_block5, html_block6

@app.callback(
    [Output('image-coin', 'src'),
    Output('graph-container', 'figure')],
    [Input('dropdown-chart', 'value'),
    Input('radio-chart', 'value')])
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


@app.callback(
    Output('graph-rates', 'figure'),
    [Input('dropdown-rates', 'value')])
def update_output(value):
    df_rates = get_df_rates()
    fig = px.line(df_rates, x = "update_date", y = value)

    return fig

# @app.callback(
#     Output('sparkline-wg2', 'figure'),
#     Output('last-update-wg2', 'children'),
#     Output('price-wg2', 'children'),
#     Input('auto-refresh2', 'n_intervals'))
# def update_box4(clicks):
#     df = get_df_sqlite()
#     figwg2 = create_sparkline("The Falcon 2 Oz", df)
#     last_uptate_wg2 = "Last update: " + str(df[df["shortname"] == "The Falcon 2 Oz"]["update_date"].max())
#     price = df[df["shortname"]=="The Falcon 2 Oz"].query("update_date == update_date.max()")["price"].values[0], " Kč"
#     return  figwg2, last_uptate_wg2, price


    