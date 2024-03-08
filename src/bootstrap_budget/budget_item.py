from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, Response, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

# Bootstrap Budget Imports
from .auth import login_required, user_only
from .entities import BudgetItem


# Define as a Flask blueprint: User
bp = Blueprint('budget_item', __name__, url_prefix='/budget-items')


@bp.route("/")
@login_required
@user_only
def index() -> Response | str:
    # Query budget item records
    budget_items = BudgetItem.select(user_id=g.user, is_active=True).order_by(BudgetItem.sequence_order, BudgetItem.name)

    return render_template('budget-item.html', user=g.user, budget_items=budget_items)
