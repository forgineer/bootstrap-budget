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

    #TODO: Sanitize form contents
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

    g.user = user

    return redirect(request.referrer)
