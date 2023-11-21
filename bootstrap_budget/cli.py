import click
import datetime
import os
import secrets
import sqlite3

from importlib.resources import files
from werkzeug.security import generate_password_hash


def get_db() -> sqlite3.Connection | None:
    """
    Gets a connection to the Bootstrap Budget database (if exists).

    :return: A SQLite connection to the Bootstrap Database. If the database does not exist, None is returned.
    """
    if os.path.exists('bootstrap_budget.db'):
        return sqlite3.connect('bootstrap_budget.db')
    else:
        return None


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
    db_connection: sqlite3.Connection = get_db()
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


def create_admin_config() -> None:
    """
    Creates the admin related configurations on the CONFIG table.
    Configurations created:
        - SECRET_KEY

    :return: None
    """
    create_config_statement: str = files('bootstrap_budget').joinpath('db/sqlite/create_config.sql').read_text()
    db_connection: sqlite3.Connection = get_db()
    sql_cursor: sqlite3.Cursor = db_connection.cursor()

    EMPTY_STRING: str = ''
    TYPE_AFFINITY_TEXT: int = 2
    ADMIN_ID: int = 1

    # Generate SECRET_KEY for Flask config
    secret_key = secrets.token_urlsafe(32)
    secret_key_description = ('A secret key that will be used for securely signing the session cookie and can be used '
                              'for any other security related needs by extensions or your application. '
                              'It should be a long random bytes or str.')

    # Capture current datetime for creation and update timestamps
    current_datetime = datetime.datetime.now()
    current_datetime_iso = current_datetime.isoformat()

    try:
        response = sql_cursor.execute(create_config_statement, [
            'SECRET_KEY',           # name
            secret_key_description, # description
            secret_key,             # config_value
            TYPE_AFFINITY_TEXT,     # config_value_type
            ADMIN_ID,               # user_id
            current_datetime_iso,   # created_dt_tm
            current_datetime_iso,   # updated_dt_tm
            True                    # is_active
        ])

        db_connection.commit()
        db_connection.close()

        click.echo('The Bootstrap Budget SECRET_KEY has been configured.')
    except Exception as e:
        # TODO: Find a better solution for handling this exception
        click.echo(e)


def reset_admin_password() -> None:
    """
    Resets the admin account password.

    :return: None
    """
    update_admin_statement: str = 'UPDATE USERS SET hash = ?, updated_dt_tm = ? WHERE username = "admin"'
    db_connection: sqlite3.Connection = get_db()
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


def create_basic_user() -> None:
    """
    Creates a basic user (meets required fields) for the purposes of testing.

    :return: None
    """
    create_user_statement: str = files('bootstrap_budget').joinpath('db/sqlite/create_user.sql').read_text()
    db_connection: sqlite3.Connection = get_db()
    sql_cursor: sqlite3.Cursor = db_connection.cursor()

    EMPTY_STRING: str = ''
    username: str | None = None

    while username is None:
        username = click.prompt(text='Enter new username', type=str, show_default=True)

        user_id = sql_cursor.execute('SELECT id FROM USERS WHERE username = ?', [username]).fetchone()

        if user_id is not None:
            click.echo(f'The username "{username}" has already been taken. Please use a different username.')
            username = None
            continue

    user_password = click.prompt(text=f'Enter password for {username}', type=str, default=f'{username}',
                                 show_default=True, hide_input=True)

    # Generate password hash and salt
    hashed_password = generate_password_hash(user_password)

    # Capture current datetime for creation and update timestamps
    current_datetime = datetime.datetime.now()
    current_datetime_iso = current_datetime.isoformat()

    try:
        response = sql_cursor.execute(create_user_statement, [
            EMPTY_STRING,           # last_name
            EMPTY_STRING,           # first_name
            EMPTY_STRING,           # middle_name
            username,               # username
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

        click.echo(f'The user {username} has been created.')
    except Exception as e:
        # TODO: Find a better solution for handling this exception
        click.echo(e)


@click.command()
@click.option('--setup', is_flag=True, help='Creates the database schema, admin user, and base config.')
@click.option('--reset-admin', is_flag=True, help='Reset admin password.')
@click.option('--reset-bootstrap', is_flag=True, help='Reset your Bootstrap-Budget install (start over).')
@click.option('--create-user', is_flag=True, help='Creates a basic user for testing purposes.')
@click.option('--backup', is_flag=True, help='Backup all tables to CSV (password-protected zip file).')
def bootstrap(setup: bool, reset_admin: bool, reset_bootstrap: bool, create_user: bool, backup: bool) -> None:
    """
    The Bootstrap Budget command-line interface utility. Used for initial setup, reset, and backing up data.

    :param setup: Creates the database schema, admin user, and base config.
    :param reset_admin: Reset admin password.
    :param reset_bootstrap: Reset your Bootstrap-Budget install (start over).
    :param create_user: Creates a basic user for testing purposes.
    :param backup: Backup all tables to CSV (password-protected zip file).
    :return: None
    """
    if setup or reset_bootstrap:
        if get_db() is not None:
            if reset_bootstrap:
                if click.confirm('Resetting Bootstrap Budget means deleting all of your data and starting over. '
                                 'Are you sure you want to do this?'):
                    create_schema()
                    create_admin_account()
                    create_admin_config()
                    click.echo('Your Boostrap Budget install has been completely reset.')
            else:
                click.echo('Bootstrap Budget has already sbeen etup. No action is needed.')
        else:
            create_schema()
            create_admin_account()
            create_admin_config()
            click.echo('Your Boostrap Budget setup is complete!')
    elif reset_admin:
        if get_db() is not None:
            if click.confirm('You are about to reset your admin account. Are you sure you want to do this?'):
                reset_admin_password()
        else:
            click.echo('The Bootstrap Budget database has not been created. Run --setup first.')
    elif backup:
        # TODO: Complete the backup feature
        click.echo('This does nothing right now, sorry :(')
    elif create_user:
        if get_db() is not None:
            create_basic_user()
        else:
            click.echo('The Bootstrap Budget database has not been created. Run --setup first.')


if __name__ == '__main__':
    pass
