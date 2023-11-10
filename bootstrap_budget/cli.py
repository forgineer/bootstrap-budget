import click
import datetime
import os
import sqlite3

from importlib.resources import files
from werkzeug.security import generate_password_hash


def create_schema() -> None:
    """
    Creates the Bootstrap Budget database schema. This is also used to reset the database schema as a DROP and REPLACE.

    :return: None
    """
    db_schema_script: str = files('bootstrap_budget').joinpath('db/sqlite/create_sqlite_schema.sql').read_text()
    db_connection: sqlite3.Connection = sqlite3.connect('bootstrap_budget.db')
    sql_cursor: sqlite3.Cursor = db_connection.cursor()

    # Iterate through each SQL statement in the file
    for schema_definition in db_schema_script.split('--'):
        response = sql_cursor.execute(schema_definition)

    db_connection.close()
    click.echo('The Bootstrap Budget schema has been created.')


def create_admin_account() -> None:
    """
    Creates the admin account on the USER table.

    :return: None
    """
    create_user_statement: str = files('bootstrap_budget').joinpath('db/sqlite/create_user.sql').read_text()
    db_connection: sqlite3.Connection = sqlite3.connect(f'bootstrap_budget.db')
    sql_cursor: sqlite3.Cursor = db_connection.cursor()

    EMPTY_STRING: str = ''

    admin_passwd = click.prompt(text='Enter admin password', type=str, default='admin',
                                show_default=True, hide_input=True)

    # Generate password hash and salt
    hashed_password = generate_password_hash(admin_passwd)

    # Capture current datetime for creation and update timestamps
    current_datetime = datetime.datetime.now()
    current_datetime_iso = current_datetime.isoformat()

    try:
        response = sql_cursor.execute(create_user_statement, [
            EMPTY_STRING,           # last_name
            EMPTY_STRING,           # first_name
            EMPTY_STRING,           # middle_name
            'admin',                # username
            EMPTY_STRING,           # address_line_1
            EMPTY_STRING,           # address_line_2
            EMPTY_STRING,           # city
            EMPTY_STRING,           # state
            EMPTY_STRING,           # zipcode
            EMPTY_STRING,           # email
            EMPTY_STRING,           # phone_number
            hashed_password,        # hash
            current_datetime_iso,   # created_dt_tm
            current_datetime_iso,   # updated_dt_tm
            True                    # is_active
        ])

        db_connection.commit()
        db_connection.close()

        click.echo('The Bootstrap Budget admin account has been created.')
    except Exception as e:
        # TODO: Find a better solution for handling this exception
        click.echo(e)


def reset_admin_password() -> None:
    """
    Resets the admin account password.

    :return: None
    """
    update_admin_statement: str = 'UPDATE USERS SET hash = ?, updated_dt_tm = ? WHERE username = "admin"'
    db_connection: sqlite3.Connection = sqlite3.connect(f'bootstrap_budget.db')
    sql_cursor: sqlite3.Cursor = db_connection.cursor()

    admin_passwd = click.prompt(text='Enter admin password', type=str, default='admin',
                                show_default=True, hide_input=True)

    # Generate password hash and salt
    hashed_password = generate_password_hash(admin_passwd)

    # Capture current datetime for creation and update timestamps
    current_datetime = datetime.datetime.now()
    current_datetime_iso = current_datetime.isoformat()

    try:
        response = sql_cursor.execute(update_admin_statement, [
            hashed_password,        # hash
            current_datetime_iso    # updated_dt_tm
        ])

        db_connection.commit()
        db_connection.close()

        click.echo('The Bootstrap Budget admin password has been reset.')
    except Exception as e:
        # TODO: Find a better solution for handling this exception
        click.echo(e)


@click.command()
@click.option('--setup', is_flag=True, help='Creates the database schema, admin user, and base config.')
@click.option('--reset-admin', is_flag=True, help='Reset admin password.')
@click.option('--reset-bootstrap', is_flag=True, help='Reset your Bootstrap-Budget install (start over).')
@click.option('--backup', is_flag=True, help='Backup all tables to CSV (password-protected zip file).')
def bootstrap(setup: bool, reset_admin: bool, reset_bootstrap: bool, backup: bool) -> None:
    """
    The Bootstrap Budegt command-line interface utility. Used for initial setup, reset, and backing up data.

    :param setup: Creates the database schema, admin user, and base config.
    :param reset_admin: Reset admin password.
    :param reset_bootstrap: Reset your Bootstrap-Budget install (start over).
    :param backup: Backup all tables to CSV (password-protected zip file).
    :return: None
    """
    if setup or reset_bootstrap:
        if os.path.exists('bootstrap_budget.db'):
            if reset_bootstrap:
                if click.confirm('Resetting Bootstrap Budget means deleting all of your data and starting over. '
                                 'Are you sure you want to do this?'):
                    create_schema()
                    create_admin_account()
                    click.echo('Your Boostrap Budget install has been completely reset.')
            else:
                click.echo('Bootstrap Budget has already setup. No action is needed.')
        else:
            create_schema()
            create_admin_account()
            click.echo('Your Boostrap Budget setup is complete!')
    elif reset_admin:
        if click.confirm('You are about to reset your admin account. Are you sure you want to do this?'):
            reset_admin_password()
    elif backup:
        # TODO: Complete the backup feature
        click.echo('This does nothing right now, sorry :(')


if __name__ == '__main__':
    pass
