"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Main entry for running the application
Notifyees: craig@2deviate.com
Category: None
"""

# local imports
import os
import logging
from config import configs
from app import create_app
from flask import render_template

env = os.environ.get("FLASK_ENV", "dev")

config = configs[env]

# main entry point of the app
app = create_app(config=config)  # pylint:6 disable=invalid-name

host = app.config["FLASK_HOST"]
port = app.config["FLASK_PORT"]
debug = app.config["FLASK_DEBUG"]
loglevel = app.config["LOGLEVEL"]
logfile = app.config["LOGFILENAME"]

logging.basicConfig(
    filename=logfile,
    level=loglevel,
    format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)


@app.route("/")
def get_index():
    return render_template("index.html")

@app.route('/api/docs')
def get_docs():    
    return render_template('swaggerui.html')

if __name__ == "__main__":
    logging.info(f"Flask configuration {config=}")
    logging.info(f"Starting Server {host=}, {port=}, {debug=}")

    app.run(host=host, port=port, debug=debug)

    logging.info(f"Stopping Server.")
