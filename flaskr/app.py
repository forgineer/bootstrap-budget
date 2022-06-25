from flask import Flask, render_template
import os
import psycopg2

app = Flask(__name__)

insert_config = open("sql/insert/INSERT_USERS.sql", "r")
insert_stmt = insert_config.read()
insert_config.close()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/test_postgres")
def test_postgres():
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute(insert_stmt)
    conn.commit()
    cur.close()
    conn.close()

    return render_template('index.html')




