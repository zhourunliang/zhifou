from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from routes import *

from models.question import Question


main = Blueprint('question', __name__)


@main.route("/")
def index():
    ts = Question.all()
    return render_template("test/index.html", ts=ts)


@main.route("/add")
def add():
    form = {'title':'test123'}
    m = Question.new(form)
    return redirect(url_for('.index'))

