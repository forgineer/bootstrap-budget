from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, Response, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

# Bootstrap Budget Imports
from .auth import login_required, user_only
from .entities import Account

# Define as a Flask blueprint: User
bp = Blueprint('account', __name__, url_prefix='/accounts')


@bp.route("/")
@login_required
@user_only
def index() -> Response | str:
    # Query account records
    accounts = Account.select(user_id=g.user, is_active=True).order_by(Account.name)

    return render_template('account.html', user=g.user, accounts=accounts)
