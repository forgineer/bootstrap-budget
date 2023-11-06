import bcrypt
import datetime
import sqlite3

from importlib.resources import files


def hash_password(password: bytes) -> tuple:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt), salt


def validate_password(password: bytes, password_hash: bytes):
    return bcrypt.checkpw(password, password_hash)


class Users:
    # USERS table fields
    last_name: str
    first_name: str
    middle_name: str
    username: str
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    zipcode: str
    email: str
    phone_number: str
    hash: str
    salt: str
    is_admin: bool
    created_dt_tm: datetime
    updated_dt_tm: datetime
    is_active: bool

    # Constants
    EMPTY_STRING: str = ''

    def __init__(self, username: str, **fields) -> None:
        self.last_name = fields.get('last_name', self.EMPTY_STRING)
        self.first_name = fields.get('first_name', self.EMPTY_STRING)
        self.middle_name = fields.get('middle_name', self.EMPTY_STRING)
        self.username = username
        self.address_line_1 = fields.get('address_line_1', self.EMPTY_STRING)
        self.address_line_2 = fields.get('address_line_2', self.EMPTY_STRING)
        self.city = fields.get('city', self.EMPTY_STRING)
        self.state = fields.get('state', self.EMPTY_STRING)
        self.zipcode = fields.get('zipcode', self.EMPTY_STRING)
        self.email = fields.get('email', self.EMPTY_STRING)
        self.phone_number = fields.get('phone_number', self.EMPTY_STRING)
        self.is_admin = fields.get('is_admin', False)
        self.is_active = fields.get('is_active', True)

    def create(self, user_password: bytes) -> None:
        insert_user: str = files('bootstrap_budget').joinpath('db/sqlite/create_user.sql').read_text()
        db_connection: sqlite3.Connection = sqlite3.connect(f'bootstrap_budget.db')
        sql_cursor: sqlite3.Cursor = db_connection.cursor()

        # Generate password hash and salt
        hashed_password, password_salt = hash_password(user_password)

        # Capture current datetime for creation and update timestamps
        current_datetime = datetime.datetime.now()
        current_datetime_iso = current_datetime.isoformat()

        try:
            response = sql_cursor.execute(insert_user, [
                self.last_name,
                self.first_name,
                self.middle_name,
                self.username,
                self.address_line_1,
                self.address_line_2,
                self.city,
                self.state,
                self.zipcode,
                self.email,
                self.phone_number,
                hashed_password,  # hash
                password_salt,  # salt
                self.is_admin,
                current_datetime_iso,  # created_dt_tm
                current_datetime_iso,  # updated_dt_tm
                self.is_active
            ])

            db_connection.commit()
        except Exception as e:
            print(e)

        db_connection.close()
