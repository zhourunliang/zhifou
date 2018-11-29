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
    user = current_user()
    if user is None:
        return redirect(url_for('user.login'))
    csrf_tokens[token] = user.id
    qu = Question.all()
    return render_template("question/index.html", qu=qu,  token=token, user=user)


@main.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('question/add.html')
    else:   
        form = request.form
        u = current_user()
        if u is None:
            return redirect(url_for('user.login'))
        m = Question.new(form, user=u.__dict__)
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
    u = current_user()
    follows = qu.follows
    log('detail follows', follows)
    log('detail u', u)
    if str(u.id) in follows:
        is_follow = True
    else:
        is_follow = False

    return render_template("question/detail.html", question=qu, answer=an, is_follow=is_follow)


@main.route("/follow")
def follow():
    id = int(request.args.get('id'))
    user = current_user()
    if user is None:
        return redirect(url_for('user.login'))
    qu = Question.find(id)
    follows = qu.follows
    log('follow1', follows)
    if not follows:
        follows = {}
    follows[str(user.id)] = user.__dict__
    log('follow2', follows)
    qu.follows = follows
    log('follow3',qu.follows)
    qu.save()
    return redirect(url_for('question.detail', id=id))

@main.route("/unfollow")
def unfollow():
    id = int(request.args.get('id'))
    user = current_user()
    if user is None:
        return redirect(url_for('user.login'))
    qu = Question.find(id)
    follows = qu.follows
    log('unfollow1', follows)
    del follows[str(user.id)]
    # follows = follows.pop(str(user.id))
    log('unfollow2', follows)
    qu.follows = follows
    log('unfollow3',qu.follows)
    qu.save()
    return redirect(url_for('question.detail', id=id))


