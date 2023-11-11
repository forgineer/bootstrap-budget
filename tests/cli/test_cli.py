import os
import sqlite3
import unittest

from bootstrap_budget import cli
from click.testing import CliRunner
from time import sleep
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

    def test_validate_admin(self, admin_password: str = 'admin') -> None:
        """
        Validates that the admin user account was created and the password can be checked.

        :return: None
        """
        db = sqlite3.connect(database='bootstrap_budget.db', detect_types=sqlite3.PARSE_DECLTYPES)

        password_hash, created_dt_tm, updated_dt_tm = db.execute('SELECT hash, created_dt_tm, updated_dt_tm '
                                                                 'FROM USERS where username = "admin"').fetchone()
        db.close()

        self.assertTrue(check_password_hash(password_hash, admin_password))
        self.assertEqual(created_dt_tm, updated_dt_tm)

    def test_reset_admin(self) -> None:
        """
        A test of 'bootstrap --reset-admin' cli command. This will reset the admin password by updating the user row.
        The updated_dt_tm should also be changes as a result to reflect when the update took place.

        :return: None
        """
        runner = CliRunner()
        sleep(1)  # Sleep for one seconds to ensure created and updated date/time do not match
        result = runner.invoke(cli=cli.bootstrap, args=['--reset-admin'], input='\n'.join(['y', 'p@ssw0rd']))

        print(result.output)

        db = sqlite3.connect(database='bootstrap_budget.db', detect_types=sqlite3.PARSE_DECLTYPES)

        password_hash, created_dt_tm, updated_dt_tm = db.execute('SELECT hash, created_dt_tm, updated_dt_tm '
                                                                 'FROM USERS where username = "admin"').fetchone()
        db.close()

        assert result.exit_code == 0
        self.assertTrue(check_password_hash(password_hash, 'p@ssw0rd'))
        self.assertNotEqual(created_dt_tm, updated_dt_tm)

    def test_reset_bootstrap(self) -> None:
        """
        A test of 'bootstrap --reset-bootstrap' cli command. This will completely reset the Bootstrap Budget schema
        and admin user

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(cli=cli.bootstrap, args=['--reset-bootstrap'], input='y')

        print(result.output)

        assert result.exit_code == 0
        assert os.path.exists('bootstrap_budget.db')

        # Validate the default admin password, created_dt_tm, and updated_dt_tm
        self.test_validate_admin(admin_password='admin')

    def test_backup(self) -> None:
        """
        A test of 'bootstrap --backup' cli command. This will back up all tables as CSV files into a single Zip file.

        :return: None
        """
        # TODO: Complete this test once the functionality has been baked in
        runner = CliRunner()
        result = runner.invoke(cli=cli.bootstrap, args=['--backup'])

        print(result.output)

        assert result.exit_code == 0

        # Remove database after successful assert
        #os.remove('bootstrap_budget.db')


if __name__ == '__main__':
    unittest.main()
