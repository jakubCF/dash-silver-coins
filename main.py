from flask import Flask
from dash import Dash
import dash_bootstrap_components as dbc

from layout_app1 import serve_layout_app1
import callbacks

app = Flask(__name__)
dash_app = Dash(
    __name__,
    server=app,
    url_base_pathname="/",
    external_stylesheets=[dbc.themes.BOOTSTRAP])

dash_app.title = 'Silver Dash'
dash_app.layout = serve_layout_app1

if __name__ == '__main__':
    app.run_server(host = "0.0.0.0", port = 8090, dev_tools_ui=True, debug=True,
              dev_tools_hot_reload =True, threaded=True)