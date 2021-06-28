from flask import Flask
from dash import Dash
import dash_bootstrap_components as dbc

from layout_app1 import serve_layout_app1
import callbacks

server = Flask(__name__)
app = Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = 'Silver Dash'
app.layout = serve_layout_app1

if __name__ == '__main__':
    app.run_server(host = "0.0.0.0", port = 8090, dev_tools_ui=True, debug=True,
              dev_tools_hot_reload =True, threaded=True)