from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from routes import *

from models.test import Test


main = Blueprint('test', __name__)


@main.route("/")
def index():
    ts = Test.all()
    return render_template("test/index.html", ts=ts)


@main.route("/add")
def add():
    form = {'title':'test123'}
    m = Test.new(form)
    return redirect(url_for('.index'))

