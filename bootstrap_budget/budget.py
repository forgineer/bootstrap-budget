import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, Response, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from bootstrap_budget.db import get_db
from .auth import login_required


# Define as a Flask blueprint: User
bp = Blueprint('budget', __name__, url_prefix='/budget')


@bp.route("/")
@login_required
def index() -> str:
    return render_template('budget.html')
