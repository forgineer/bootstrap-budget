import os
import sqlite3
import unittest

from bootstrap_budget import cli
from click.testing import CliRunner
from werkzeug.security import check_password_hash


class TestCLI(unittest.TestCase):
    def test_setup(self) -> None:
        """
        A test of 'boostrap -setup' cli command. An admin account is created with a default password of 'admin'.

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(cli=cli.bootstrap, args=['--setup'])

        print(result.output)

        assert result.exit_code == 0
        assert os.path.exists('bootstrap_budget.db')

    def test_validate_admin(self) -> None:
        """
        Validates that the admin user account was created and the

        :return:
        """
        db = sqlite3.connect(database='bootstrap_budget.db', detect_types=sqlite3.PARSE_DECLTYPES)

        password_hash = db.execute('SELECT hash FROM USERS where username = "admin"').fetchone()
        db.close()
        self.assertTrue(check_password_hash(password_hash[0], 'admin'))

        # Remove database after successful assert
        os.remove('bootstrap_budget.db')


if __name__ == '__main__':
    unittest.main()
