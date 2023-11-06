import click
import getpass
import os
import sqlite3

from bootstrap_budget import Users
from importlib.resources import files


def create_schema() -> None:
    db_schema_script: str = files('bootstrap_budget').joinpath('db/sqlite/create_sqlite_schema.sql').read_text()
    db_connection: sqlite3.Connection = sqlite3.connect('bootstrap_budget.db')
    sql_cursor: sqlite3.Cursor = db_connection.cursor()

    # Iterate through each SQL statement in the file
    for schema_definition in db_schema_script.split('--'):
        response = sql_cursor.execute(schema_definition)

    db_connection.close()


@click.command('bootstrap-init')
@click.option('-set-admin-passwd', is_flag=True, help='Set admin password.')
@click.option('-refresh-schema', is_flag=True, help='Refresh the database schema (drop and replace).')
def bootstrap_init(set_admin_passwd: bool, refresh_schema: bool) -> None:
    if os.path.exists('bootstrap_budget.db'):
        if refresh_schema:
            create_schema()
            click.echo('Bootstrap-Budget schema has been refreshed.')
        else:
            click.echo('Bootstrap-Budget schema already exists.')
    else:
        create_schema()
        click.echo('Bootstrap-Budget schema has been created.')

    passwd: bytes

    if set_admin_passwd:
        passwd = bytes(getpass.getpass('Enter admin password:'), 'utf-8')
    else:
        passwd = bytes('admin', 'utf-8')

    admin_user = Users(username='admin', is_admin=True)
    admin_user.create(user_password=passwd)
    click.echo('Admin user created.')


if __name__ == '__main__':
    pass
