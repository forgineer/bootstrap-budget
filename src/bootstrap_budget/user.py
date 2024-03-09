from flask import (
    Blueprint, flash, g, redirect, render_template, request, Response, session, url_for
)

# Bootstrap Budget Imports
from .auth import login_required, user_only


# Define as a Flask blueprint: User
bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route("/")
@login_required
@user_only
def index() -> Response | str:
    return render_template('dashboard.html', user=g.user)
