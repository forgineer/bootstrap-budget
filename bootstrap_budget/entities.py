from datetime import datetime
from pony.orm import Database, Optional, PrimaryKey, Required, Set


def define_user_entity(db_entity: Database().Entity) -> None:
    """

    :param db_entity:
    :return:
    """
    class User(db_entity):
        id = PrimaryKey(int, auto=True)
        last_name = Optional(str, nullable=True)
        first_name = Optional(str, nullable=True)
        middle_name = Optional(str, nullable=True)
        username = Required(str, unique=True)
        address_line_1 = Optional(str, nullable=True)
        address_line_2 = Optional(str, nullable=True)
        city = Optional(str, nullable=True)
        state = Optional(str, nullable=True)
        zipcode = Optional(str, nullable=True)
        email = Optional(str, nullable=True)
        phone_number = Optional(str, nullable=True)
        hash = Required(str)
        created_dt_tm = Required(datetime)
        updated_dt_tm = Required(datetime)
        is_active = Required(bool, default=True)
        configs = Set('Config')
        budgets = Set('Budget')
        budget_items = Set('BudgetItem')
        accounts = Set('Account')
        transactions = Set('Transaction')


def define_config_entity(db_entity: Database().Entity) -> None:
    """

    :param db_entity:
    :return:
    """
    class Config(db_entity):
        id = PrimaryKey(int, auto=True)
        name = Required(str, unique=True)
        description = Optional(str, nullable=True)
        config_value = Optional(str, nullable=True)
        config_value_type = Required(int, default=0)
        created_dt_tm = Required(datetime)
        updated_dt_tm = Required(datetime)
        is_active = Required(bool, default=True)
        user = Required('User')


def define_budget_entity(db_entity: Database().Entity) -> None:
    """

    :param db_entity:
    :return:
    """
    class Budget(db_entity):
        id = PrimaryKey(int, auto=True)
        name = Required(str)
        description = Optional(str, nullable=True)
        budget_year = Required(int)
        created_dt_tm = Required(datetime)
        updated_dt_tm = Required(datetime)
        is_active = Required(bool, default=True)
        user = Required('User')


def define_budget_item_entity(db_entity: Database().Entity) -> None:
    """

    :param db_entity:
    :return:
    """
    class BudgetItem(db_entity):
        id = PrimaryKey(int, auto=True)
        name = Required(str)
        description = Optional(str, nullable=True)
        budget_amount = Required(float, default=0)
        sequence = Required(int, default=99)
        created_dt_tm = Required(datetime)
        updated_dt_tm = Required(datetime)
        is_active = Required(bool, default=True)
        user = Required('User')
        transactions = Set('Transaction')


def define_account_entity(db_entity: Database().Entity) -> None:
    """

    :param db_entity:
    :return:
    """
    class Account(db_entity):
        id = PrimaryKey(int, auto=True)
        name = Required(str)
        description = Optional(str, nullable=True)
        account_number = Optional(str, nullable=True)
        account_route_nbr = Optional(str, nullable=True)
        opening_amount = Required(float, default=0)
        created_dt_tm = Required(datetime)
        updated_dt_tm = Required(datetime)
        is_active = Required(bool, default=True)
        user = Required('User')
        transactions = Set('Transaction')


def define_transaction_entity(db_entity: Database().Entity) -> None:
    """

    :param db_entity:
    :return:
    """
    class Transaction(db_entity):
        id = PrimaryKey(int, auto=True)
        description = Optional(str, nullable=True)
        amount = Required(float, default=0)
        transaction_dt_tm = Required(datetime)
        note = Optional(str, nullable=True)
        created_dt_tm = Required(datetime)
        updated_dt_tm = Required(datetime, nullable=True)
        is_active = Required(bool, default=True)
        account = Required('Account')
        budget_item = Required('BudgetItem')
        user = Required('User')
