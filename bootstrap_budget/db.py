import sqlite3

from flask import Flask, g


def get_db() -> sqlite3.Connection:
    """
    Create and/or retrieve the SQLite DB connection as a Flask global (g) property

    :return: A SQLite connection
    """
    if 'db' not in g:
        g.db = sqlite3.connect(database='boostrap_budget.db',
                               detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db() -> None:
    """

    :return:
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app: Flask) -> None:
    """
    Used to register all database functions with the Flask app as teardown instructions.

    :param app: The current Flask app
    :return: None
    """

    """
    """
    app.teardown_appcontext(close_db)


if __name__ == '__main__':
    pass
