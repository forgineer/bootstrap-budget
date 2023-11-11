import unittest

from bootstrap_budget import config
from sqlite3 import Connection


class TestConfig(unittest.TestCase):
    def test_get_config(self) -> None:
        """
        A test of 'boostrap -setup' cli command. An admin account is created with a default password of 'admin'.

        :return: None
        """
        ADMIN_ID: int = 1

        secret_key: config.CONFIG = config.CONFIG(name='SECRET_KEY', user_id=ADMIN_ID)

        print(secret_key)

        secret_key.get()

        print(secret_key)


if __name__ == '__main__':
    unittest.main()
