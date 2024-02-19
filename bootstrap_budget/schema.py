from datetime import datetime
from pony.orm import Database, composite_key, Optional, PrimaryKey, Required, Set


def define_entities(db_entity: Database().Entity) -> None:
    """

    :param db_entity:
    :return: None
    """
    class User(db_entity):
        _table_ = 'USER'

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
        accounts = Set('Account')
        configs = Set('Config')
        budgets = Set('Budget')
        budget_items = Set('BudgetItem')
        transactions = Set('Transaction')
        user_budgets = Set('UserBudget')

    class Config(db_entity):
        _table_ = 'CONFIG'

        id = PrimaryKey(int, auto=True)
        name = Required(str, unique=True)
        description = Optional(str, nullable=True)
        config_value = Optional(str, nullable=True)
        config_value_type = Required(int, default=0)
        created_dt_tm = Required(datetime)
        updated_dt_tm = Required(datetime)
        is_active = Required(bool, default=True)
        user_id = Required('User')
        composite_key(name, user_id)

    class Budget(db_entity):
        _table_ = 'BUDGET'

        id = PrimaryKey(int, auto=True)
        name = Required(str)
        description = Optional(str, nullable=True)
        budget_year = Required(int)
        created_dt_tm = Required(datetime)
        updated_dt_tm = Required(datetime)
        is_active = Required(bool, default=True)
        user_id = Required('User')
        user_budgets = Set('UserBudget')
        composite_key(name, user_id)

    class UserBudget(db_entity):
        _table_ = 'USER_BUDGET'

        id = PrimaryKey(int, auto=True)
        permissions = Required(int)
        created_dt_tm = Required(datetime)
        updated_dt_tm = Required(datetime)
        is_active = Required(bool, default=True)
        user_id = Required('User')
        budget_id = Required('Budget')

    class BudgetItem(db_entity):
        _table_ = 'BUDGET_ITEM'

        id = PrimaryKey(int, auto=True)
        name = Required(str)
        description = Optional(str, nullable=True)
        budget_amount = Required(float, default=0)
        sequence = Required(int, default=99)
        created_dt_tm = Required(datetime)
        updated_dt_tm = Required(datetime)
        is_active = Required(bool, default=True)
        user_id = Required('User')
        transactions = Set('Transaction')
        composite_key(name, user_id)

    class Account(db_entity):
        _table_ = 'ACCOUNT'

        id = PrimaryKey(int, auto=True)
        name = Required(str)
        description = Optional(str, nullable=True)
        account_number = Optional(str, nullable=True)
        account_route_nbr = Optional(str, nullable=True)
        opening_amount = Required(float, default=0)
        created_dt_tm = Required(datetime)
        updated_dt_tm = Required(datetime)
        is_active = Required(bool, default=True)
        user_id = Required('User')
        transactions = Set('Transaction')
        composite_key(name, user_id)

    class Transaction(db_entity):
        _table_ = 'TRANSACTION'

        id = PrimaryKey(int, auto=True)
        description = Optional(str, nullable=True)
        amount = Required(float, default=0)
        transaction_dt_tm = Required(datetime)
        note = Optional(str, nullable=True)
        created_dt_tm = Required(datetime)
        updated_dt_tm = Required(datetime, nullable=True)
        is_active = Required(bool, default=True)
        user_id = Required('User')
        account_id = Required('Account')
        budget_item_id = Required('BudgetItem')
