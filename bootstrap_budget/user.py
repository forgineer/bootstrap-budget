import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, Response, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from bootstrap_budget.db import get_db
from .auth import login_required


# Define as a Flask blueprint: User
bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route("/")
@login_required
def index() -> str:
    return render_template('dashboard.html')


@bp.route("/budget")
@login_required
def budget() -> str:
    return render_template('budget.html')


@bp.route("/budget-items")
@login_required
def budget_items() -> str:
    return render_template('budget-items.html')


@bp.route("/accounts")
@login_required
def accounts() -> str:
    return render_template('accounts.html')


@bp.route("/accounts/transactions")
@login_required
def account_transactions() -> str:
    return render_template('transactions.html')


@bp.route('/logout')
def logout() -> Response:
    session.clear()
    return redirect(url_for('auth.login'))
