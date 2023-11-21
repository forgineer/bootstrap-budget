import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

# Import bootstrap-budget blueprints/modules/classes/functions
from .auth import login_required


# Define as a Flask blueprint: Admin
bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route("/")
@login_required
def index():
    return render_template('admin.html')


@bp.route("/users")
@login_required
def users():
    return render_template('users.html')


@bp.route("/stop")
@login_required
def stop():
    return '<p>STOP!</p>'
