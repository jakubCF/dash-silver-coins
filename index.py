import os
import dash_bootstrap_components as dbc

from app import app, server
from layout_app1 import serve_layout_app1
import callbacks

app.layout = serve_layout_app1

if "debug" in os.environ:
    debug_mode = os.getenv('debug')
    if debug_mode == "True":
        debug_mode = True
else:
    debug_mode = False

if __name__ == '__main__':
    app.run_server(host = "0.0.0.0", port = 8090, dev_tools_ui=debug_mode, debug=debug_mode,
              dev_tools_hot_reload=debug_mode, threaded=True)