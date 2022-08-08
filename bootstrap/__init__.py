import os
from flask import Flask, render_template
from logging.config import dictConfig


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def budget(test_config=None):
    # Create and configure the app
    app = Flask(__name__)

    from . import db
    db.init_app(app)

    @app.route("/")
    def index():
        return render_template('index.html')

    return app