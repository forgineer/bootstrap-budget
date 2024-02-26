import importlib.metadata
import sqlite3

from datetime import datetime
from flask import Flask
from logging.config import dictConfig
from pony import orm
from pony.flask import Pony

# Set Bootstrap Budget version
__version__: str = importlib.metadata.version('bootstrap_budget')


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


# Define database and entities (Pony ORM)
db = orm.Database()


class User(db.Entity):
    _table_ = 'USER'

    id = orm.PrimaryKey(int, auto=True)
    last_name = orm.Optional(str, nullable=True)
    first_name = orm.Optional(str, nullable=True)
    middle_name = orm.Optional(str, nullable=True)
    username = orm.Required(str, unique=True)
    address_line_1 = orm.Optional(str, nullable=True)
    address_line_2 = orm.Optional(str, nullable=True)
    city = orm.Optional(str, nullable=True)
    state = orm.Optional(str, nullable=True)
    zipcode = orm.Optional(str, nullable=True)
    email = orm.Optional(str, nullable=True)
    phone_number = orm.Optional(str, nullable=True)
    hash = orm.Required(str)
    created_dt_tm = orm.Required(datetime)
    updated_dt_tm = orm.Required(datetime)
    is_active = orm.Required(bool, default=True)
    accounts = orm.Set('Account')
    configs = orm.Set('Config')
    budgets = orm.Set('Budget')
    budget_items = orm.Set('BudgetItem')
    transactions = orm.Set('Transaction')
    user_budgets = orm.Set('UserBudget')
"""
CREATE TABLE "USER" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "last_name" TEXT,
    "first_name" TEXT,
    "middle_name" TEXT,
    "username" TEXT UNIQUE NOT NULL,
    "address_line_1" TEXT,
    "address_line_2" TEXT,
    "city" TEXT,
    "state" TEXT,
    "zipcode" TEXT,
    "email" TEXT,
    "phone_number" TEXT,
    "hash" TEXT NOT NULL,
    "created_dt_tm" DATETIME NOT NULL,
    "updated_dt_tm" DATETIME NOT NULL,
    "is_active" BOOLEAN NOT NULL
);
"""


class Config(db.Entity):
    _table_ = 'CONFIG'

    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str, unique=True)
    description = orm.Optional(str, nullable=True)
    config_value = orm.Optional(str, nullable=True)
    config_value_type = orm.Required(int, default=0)
    created_dt_tm = orm.Required(datetime)
    updated_dt_tm = orm.Required(datetime)
    is_active = orm.Required(bool, default=True)
    user_id = orm.Required(User)
    orm.composite_key(name, user_id)
"""
CREATE TABLE "CONFIG" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT UNIQUE NOT NULL,
    "description" TEXT,
    "config_value" TEXT,
    "config_value_type" INTEGER NOT NULL,
    "created_dt_tm" DATETIME NOT NULL,
    "updated_dt_tm" DATETIME NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "user_id" INTEGER NOT NULL REFERENCES "USER" ("id") ON DELETE CASCADE,
    CONSTRAINT "unq_config__name_user_id" UNIQUE ("name", "user_id")
);

CREATE INDEX "idx_config__user_id" ON "CONFIG" ("user_id");
"""


class Budget(db.Entity):
    _table_ = 'BUDGET'

    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str)
    description = orm.Optional(str, nullable=True)
    budget_year = orm.Required(int)
    created_dt_tm = orm.Required(datetime)
    updated_dt_tm = orm.Required(datetime)
    is_active = orm.Required(bool, default=True)
    user_id = orm.Required(User)
    user_budgets = orm.Set('UserBudget')
    orm.composite_key(name, user_id)
"""
CREATE TABLE "BUDGET" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "description" TEXT,
    "budget_year" INTEGER NOT NULL,
    "created_dt_tm" DATETIME NOT NULL,
    "updated_dt_tm" DATETIME NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "user_id" INTEGER NOT NULL REFERENCES "USER" ("id") ON DELETE CASCADE,
    CONSTRAINT "unq_budget__name_user_id" UNIQUE ("name", "user_id")
);

CREATE INDEX "idx_budget__user_id" ON "BUDGET" ("user_id");
"""


class UserBudget(db.Entity):
    _table_ = 'USER_BUDGET'

    id = orm.PrimaryKey(int, auto=True)
    permissions = orm.Required(int)
    created_dt_tm = orm.Required(datetime)
    updated_dt_tm = orm.Required(datetime)
    is_active = orm.Required(bool, default=True)
    user_id = orm.Required(User)
    budget_id = orm.Required(Budget)
"""
CREATE TABLE "USER_BUDGET" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "permissions" INTEGER NOT NULL,
    "created_dt_tm" DATETIME NOT NULL,
    "updated_dt_tm" DATETIME NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "user_id" INTEGER NOT NULL REFERENCES "USER" ("id") ON DELETE CASCADE,
    "budget_id" INTEGER NOT NULL REFERENCES "BUDGET" ("id") ON DELETE CASCADE
);

CREATE INDEX "idx_user_budget__budget_id" ON "USER_BUDGET" ("budget_id");
CREATE INDEX "idx_user_budget__user_id" ON "USER_BUDGET" ("user_id");
"""

class BudgetItem(db.Entity):
    _table_ = 'BUDGET_ITEM'

    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str)
    description = orm.Optional(str, nullable=True)
    budget_amount = orm.Required(float, default=0)
    sequence_order = orm.Required(int, default=99)
    created_dt_tm = orm.Required(datetime)
    updated_dt_tm = orm.Required(datetime)
    is_active = orm.Required(bool, default=True)
    user_id = orm.Required(User)
    transactions = orm.Set('Transaction')
    orm.composite_key(name, user_id)
"""
CREATE TABLE "BUDGET_ITEM" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "description" TEXT,
    "budget_amount" REAL NOT NULL,
    "sequence_order" INTEGER NOT NULL,
    "created_dt_tm" DATETIME NOT NULL,
    "updated_dt_tm" DATETIME NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "user_id" INTEGER NOT NULL REFERENCES "USER" ("id") ON DELETE CASCADE,
    CONSTRAINT "unq_budget_item__name_user_id" UNIQUE ("name", "user_id")
);

CREATE INDEX "idx_budget_item__user_id" ON "BUDGET_ITEM" ("user_id");
"""


class Account(db.Entity):
    _table_ = 'ACCOUNT'

    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str)
    description = orm.Optional(str, nullable=True)
    account_number = orm.Optional(str, nullable=True)
    account_route_nbr = orm.Optional(str, nullable=True)
    opening_amount = orm.Required(float, default=0)
    created_dt_tm = orm.Required(datetime)
    updated_dt_tm = orm.Required(datetime)
    is_active = orm.Required(bool, default=True)
    user_id = orm.Required(User)
    transactions = orm.Set('Transaction')
    orm.composite_key(name, user_id)
"""
CREATE TABLE "ACCOUNT" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "description" TEXT,
    "account_number" TEXT,
    "account_route_nbr" TEXT,
    "opening_amount" REAL NOT NULL,
    "created_dt_tm" DATETIME NOT NULL,
    "updated_dt_tm" DATETIME NOT NULL,
    "is_active" BOOLEAN NOT NULL,
    "user_id" INTEGER NOT NULL REFERENCES "USER" ("id") ON DELETE CASCADE,
    CONSTRAINT "unq_account__name_user_id" UNIQUE ("name", "user_id")
);

CREATE INDEX "idx_account__user_id" ON "ACCOUNT" ("user_id");
"""


class Transaction(db.Entity):
    _table_ = 'TRANSACTION'

    id = orm.PrimaryKey(int, auto=True)
    description = orm.Optional(str, nullable=True)
    amount = orm.Required(float, default=0)
    transaction_dt_tm = orm.Required(datetime)
    note = orm.Optional(str, nullable=True)
    created_dt_tm = orm.Required(datetime)
    updated_dt_tm = orm.Required(datetime, nullable=True)
    is_active = orm.Required(bool, default=True)
    user_id = orm.Required(User)
    account_id = orm.Required(Account)
    budget_item_id = orm.Required(BudgetItem)
"""
CREATE TABLE "TRANSACTION" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "description" TEXT,
    "amount" REAL NOT NULL,
    "transaction_dt_tm" DATETIME NOT NULL,
    "note" TEXT,
    "created_dt_tm" DATETIME NOT NULL,
    "updated_dt_tm" DATETIME,
    "is_active" BOOLEAN NOT NULL,
    "user_id" INTEGER NOT NULL REFERENCES "USER" ("id") ON DELETE CASCADE,
    "account_id" INTEGER NOT NULL REFERENCES "ACCOUNT" ("id") ON DELETE CASCADE,
    "budget_item_id" INTEGER NOT NULL REFERENCES "BUDGET_ITEM" ("id") ON DELETE CASCADE
);

CREATE INDEX "idx_transaction__account_id" ON "TRANSACTION" ("account_id");
CREATE INDEX "idx_transaction__budget_item_id" ON "TRANSACTION" ("budget_item_id");
CREATE INDEX "idx_transaction__user_id" ON "TRANSACTION" ("user_id");
"""


def create_app() -> Flask:
    """
    The main function for Bootstrap Budget.

    :return: A Flask app (Bootstrap Budget)
    """
    # Create and configure the app
    # The instance folder is set to 'relative' in order to find the config file easily
    app = Flask(__name__, instance_relative_config=True)

    # TODO: Remove this once the database bind is tested
    # Check to see if the database was set up through the CLI utility.
    #with app.app_context():
    #    db_connection: sqlite3.Connection = data.get_db()
    #
    #    if db_connection is None:
    #        raise RuntimeError('The Bootstrap Budget database has not been created. '
    #                           'Use the "bootstrap --setup" CLI command to complete the installation.')

    # Find the configuration file one level up from the instance folder (defined as relative)
    # A configuration file should have been created from the 'boostrap --setup' CLI and contain
    # the SECRET_KEY and any other configurations.
    app.config.from_pyfile('bootstrap_config.py')

    # Bind the database from config
    db.bind(**app.config['PONY'])
    db.generate_mapping()

    # Wrap application requests with Pony's db_session
    Pony(app)

    # Import Bootstrap Budget blueprint modules
    from . import (
        account, admin, auth, budget, budget_item, dashboard, transaction, user
    )

    # Register blueprints
    app.register_blueprint(account.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(budget.bp)
    app.register_blueprint(budget_item.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(transaction.bp)
    app.register_blueprint(user.bp)

    # Define the index entry point: The Boostrap Budget Dashboard
    app.add_url_rule("/", endpoint="dashboard.index")

    return app
