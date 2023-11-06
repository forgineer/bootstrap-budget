from flask import Flask, render_template
from logging.config import dictConfig

# Import bootstrap-budget modules/classes/functions
from .users import Users


dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def start(test_config=None):
    # Create and configure the app
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template('index.html')

    return app
