"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Main entry for running the application
Notifyees: craig@2deviate.com
Category: None
"""

# local imports
import os
from app import create_app
from config import configs

import logging

env = os.environ.get("FLASK_ENV", "dev")

config = configs[env]

host = config.FLASK_HOST
port = config.FLASK_PORT
debug = config.FLASK_DEBUG

loglevel = config.LOGLEVEL
logfile = config.LOGFILENAME

logging.basicConfig(
    filename=logfile,
    level=loglevel,
    format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)

# main entry point of the app
app = create_app(config=config)  # pylint:6 disable=invalid-name

@app.route("/")
def get_index():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    logging.info(f"Flask configuration {config=}")
    logging.info(f"Starting Server {host=}, {port=}, {debug=}")
    
    app.run(host=host, port=port, debug=debug)
    
    logging.info(f"Stopping Server.")
