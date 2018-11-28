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
from utils import log
import json

from models.question import Question
from models.answer import Answer

main = Blueprint('answer', __name__)

# 防csrf
csrf_tokens = dict()

@main.route("/")
def index():
    qid = int(request.args.get('qid'))
    # log('index qid=', qid)
    u = current_user()
    if u is None:
        return redirect(url_for('user.login'))
    qu = Question.get(qid)
    an = Answer.find_all(qid=qid)
    return render_template("answer/index.html", qu=qu, an=an)

@main.route("/add", methods=["POST"])
def add():   
    form = request.form
    qid = form['qid']
    # log('add qid=', qid)
    u = current_user()
    if u is None:
        return redirect(url_for('user.login'))
    r = Answer.new(form, user=u.__dict__)
    return redirect(url_for('question.detail', id=qid))

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

@main.route("/like")
def like():
    id = int(request.args.get('id'))
    an = Answer.find(id)
    an.like = an.like + 1
    an.save()
    return redirect(url_for('question.detail', id=an.qid))

@main.route("/unlike")
def unlike():
    id = int(request.args.get('id'))
    an = Answer.find(id)
    an.unlike = an.unlike + 1
    an.save()
    return redirect(url_for('question.detail', id=an.qid))
