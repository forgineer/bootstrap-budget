import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

# Import bootstrap-budget blueprints/modules/classes/functions
from . import db


# Define as a Flask blueprint: Admin
bp = Blueprint('admin', __name__)


@bp.route("/admin")
def admin_console():
    return render_template('admin.html')


@bp.route("/users")
def users_console():
    return render_template('users.html')


@bp.route("/stop")
def stop():
    return '<p>STOP!</p>'
