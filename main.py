from app import app
from layout_app1 import serve_layout_app1
import callbacks

app.layout = serve_layout_app1

if __name__ == '__main__':
    app.run_server(host = "0.0.0.0", port = 8090, dev_tools_ui=True, debug=True,
              dev_tools_hot_reload =True, threaded=True)