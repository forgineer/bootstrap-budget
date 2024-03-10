from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, Response, session, url_for
)

# Bootstrap Budget Imports
from .auth import login_required, user_only
from .entities import User


# Define as a Flask blueprint: User
bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route("/")
@login_required
@user_only
def index() -> Response | str:
    return render_template('dashboard.html', user=g.user)


@bp.route("/update", methods=["POST"])
@login_required
def update() -> Response | str:
    """
    Update the current user from 'Edit Profile' modal.

    :return: Back to current view after update.
    """
    user: User = g.user

    try:
        user.first_name = request.form['first_name']
        user.middle_name = request.form['middle_name']
        user.last_name = request.form['last_name']
        user.address_line_1 = request.form['address_line_1']
        user.address_line_2 = request.form['address_line_2']
        user.city = request.form['city']
        user.state = request.form['state']
        user.zipcode = request.form['zipcode']
        user.email = request.form['email']
        user.phone_number = request.form['phone_number']

        flash('User profile was successfully saved.', 'info')
    except Exception as e:
        flash(f'User profile failed to save: {e}', 'error')

    g.user = user

    return redirect(request.referrer)


@bp.route("/reset-password", methods=["POST"])
@login_required
def reset_password() -> Response | str:
    """
    Reset the password for a given user (by username) from 'Reset Password' modal.

    :return: Back to current view after update.
    """
    flash('This does not do anything yet, Sorry :-/', 'warning')

    return redirect(request.referrer)