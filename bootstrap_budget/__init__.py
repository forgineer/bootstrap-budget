import importlib.metadata

from flask import Flask, render_template, redirect, request, url_for
from logging.config import dictConfig
from werkzeug.security import check_password_hash


# Set Bootstrap Budget version
__version__: str = importlib.metadata.version("bootstrap_budget")


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


def main() -> Flask:
    """
    The main function for Bootstrap Budget.

    :return: A Flask app (Bootstrap Budget)
    """
    # Create and configure the app
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    # Register Bootstrap Budget blueprints
    from . import auth
    from . import user
    #from . import admin

    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    #app.register_blueprint(admin.bp)

    # Define the index entry point: The Boostrap Budget Dashboard
    app.add_url_rule("/", endpoint="user.index")

    return app
