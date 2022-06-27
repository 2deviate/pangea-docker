import os
from run import app

host = os.environ.get("FLASK_HOST")
port = os.environ.get("FLASK_PORT")
debug = os.environ.get("FLASK_DEBUG")

if __name__ == "__main__":
    app.run(host=host, port=port, debug=debug)
    