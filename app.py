from flask import Flask
from dash import Dash
import dash_bootstrap_components as dbc

server = Flask(__name__)
app = Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = 'Silver Dash'
