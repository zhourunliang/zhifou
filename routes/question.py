from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)
import uuid
from routes import *

from models.question import Question
from models.answer import Answer
from utils import log

main = Blueprint('question', __name__)

# 防csrf
csrf_tokens = dict()

@main.route("/")
def index():
    token = str(uuid.uuid4())
    u = current_user()
    if u is None:
        return redirect(url_for('user.login'))
    csrf_tokens[token] = u.id
    qu = Question.all()
    return render_template("question/index.html", qu=qu,  token=token)


@main.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('question/add.html')
    else:   
        form = request.form
        m = Question.new(form)
        return redirect(url_for('.index'))

@main.route("/delete")
def delete():
    id = int(request.args.get('id'))
    token = request.args.get('token')
    u = current_user()
    # 判断 token 是否是我们给的
    if token in csrf_tokens and csrf_tokens[token] == u.id:
        csrf_tokens.pop(token)
        if u is not None:
            print('删除 question 用户是', u, id)
            Question.delete(id)
            return redirect(url_for('.index'))
        else:
            abort(404)
    else:
        abort(403)

@main.route('/detail/<int:id>')
def detail(id):
    qu = Question.get(id)
    an = Answer.find_all(qid=id)
    return render_template("question/detail.html", question=qu, answer=an)


