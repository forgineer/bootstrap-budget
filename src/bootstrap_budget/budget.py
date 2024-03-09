from flask import (
    Blueprint, flash, g, redirect, render_template, request, Response, session, url_for
)

# Bootstrap Budget Imports
from .auth import login_required, user_only
from .entities import Budget


# Define as a Flask blueprint: User
bp = Blueprint('budget', __name__, url_prefix='/budgets')


@bp.route("/")
@login_required
@user_only
def index() -> Response | str:
    # Query budget records
    budgets = Budget.select(user_id=g.user, is_active=True).order_by(Budget.budget_year, Budget.name)

    return render_template('budget.html', user=g.user, budgets=budgets)
