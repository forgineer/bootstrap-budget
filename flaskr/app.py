from flask import Flask, render_template
import os
import psycopg2


# Setup Flask app
app = Flask(__name__)


# Get DB environment var
DATABASE_URL = os.environ['DATABASE_URL']


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
