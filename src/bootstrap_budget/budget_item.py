from datetime import datetime
from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, Response
)

# Bootstrap Budget Imports
from .auth import login_required, user_only
from .entities import BudgetItem


bp = Blueprint('budget_item', __name__, url_prefix='/budget-items')


@bp.route("/")
@login_required
@user_only
def index() -> Response | str:
    # Query budget item records
    budget_items = BudgetItem.select(user_id=g.user, is_active=True).order_by(BudgetItem.sequence_order, BudgetItem.name)

    return render_template('budget-item.html', user=g.user, budget_items=budget_items)


@bp.route("/create", methods=["POST"])
@login_required
def create() -> Response | str:
    """
    Create a new Budget Item from the 'Create Budget Item' modal.

    :return: Back to current view after creation.
    """
    try:
        BudgetItem(name=request.form['name'],
                   description=request.form['description'],
                   budget_amount=float(request.form['budget_amount']),
                   sequence_order=int(request.form['sequence_order']),
                   created_dt_tm=datetime.now(),
                   updated_dt_tm=datetime.now(),
                   user_id=g.user.id)

        flash('The budget item was successfully created.', 'info')
    except Exception as e:
        flash(f'The budget item failed to be created: {e}', 'error')

    return redirect(request.referrer)


@bp.route("/update", methods=["POST"])
@login_required
def update() -> Response | str:
    """
    Update the current account from the 'Edit Account' modal.

    :return: Back to current view after update.
    """
    try:
        current_app.logger.info(request.form)
        #g.user.first_name = request.form['first_name']

        flash('The budget was successfully saved.', 'info')
    except Exception as e:
        flash(f'The budget failed to save: {e}', 'error')

    return redirect(request.referrer)


@bp.route("/delete", methods=["POST"])
@login_required
def delete() -> Response | str:
    """
    Delete an account.

    :return: Back to current view after deletion.
    """
    try:
        current_app.logger.info(request.form)
        #g.user.first_name = request.form['first_name']

        flash('The budget was successfully saved.', 'info')
    except Exception as e:
        flash(f'The budget failed to save: {e}', 'error')

    return redirect(request.referrer)
