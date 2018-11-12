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
    return render_template("question/index.html", ts=ts)


@main.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('question/add.html')
    else:   
        form = request.form
        m = Question.new(form)
        return redirect(url_for('.index'))

