import os
import click
from flask import current_app, g
from flask.cli import with_appcontext
import psycopg2 as psql


def get_db():
    if 'db' not in g:
        # Get DB environment var
        DATABASE_URL = os.environ['DATABASE_URL']
        #DATABASE_URL = 'postgres://fmclgrvutqfihl:91985637a4936ec8f11fbb18455bd4d1ac9308725409f5323c32745db00d383a\
        # @ec2-52-72-56-59.compute-1.amazonaws.com:5432/d8g771gs0trs2h'

        g.db = psql.connect(DATABASE_URL)

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


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
