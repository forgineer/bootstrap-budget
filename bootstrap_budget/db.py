import os
from flask import current_app, g


def get_db():
    if 'db' not in g:
        # Get DB environment var
        DATABASE_URL = os.environ['DATABASE_URL']

        #g.db = psql.connect(DATABASE_URL)

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    cur = db.cursor()

    with current_app.open_resource('postgresql_schema.sql') as sql:
        cur.execute(sql.read().decode('utf8'))
        db.commit()
        cur.close()


def init_app(app):
    app.teardown_appcontext(close_db)
