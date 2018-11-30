from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    send_from_directory,
    flash,
)

import os
from werkzeug.utils import secure_filename
from models.user import User
from utils import log
from config import user_img_director
from models.answer import Answer
from models.question import Question

main = Blueprint('user', __name__)

def current_user():
    # 从 session 中找到 user_id 字段, 找不到就 -1
    # 然后 User.find_by 来用 id 找用户
    # 找不到就返回 None
    uid = session.get('user_id', -1)
    u = User.find_by(id=uid)
    return u


@main.route("/")
def index():
    return redirect(url_for('.login'))

@main.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('user/register.html')
    else:     
        form = request.form
        # 用类函数来判断
        u = User.register(form)
        # log('register', u)
        if u['status'] is False:
            msg = u['msg'] 
            return render_template('user/register.html', msg=msg)
        else:
            return redirect(url_for('.login'))

@main.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')
    else:       
        form = request.form
        log('login', form)
        u = User.validate_login(form)
        if u['status'] is False:
            msg = u['msg'] 
            return render_template('user/login.html', msg=msg)
        else:
            user = u['data']
            # session 中写入 user_id
            session['user_id'] = user.id
            # 设置 cookie 有效期为 永久
            session.permanent = True
            return redirect(url_for('index.index'))

@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index.index'))


@main.route('/setting', methods=['GET', 'POST'])
def setting():
    u = current_user()
    if request.method == 'GET':    
        if u is None:
            return redirect(url_for('.login'))
        else:
            return render_template('user/setting.html', user=u)
    else:     
        form = request.form
        name = form.get('username', '')
        pwd = form.get('password', '')
        area = form.get('area', '')
        job = form.get('job', '')
        if len(name) < 2:
            return render_template('user/setting.html', msg='用户名不能少于2位', user=u)
        elif User.find_by(username=name).id != u.id:
            return render_template('user/setting.html', msg='用户名已存在', user=u)
        else:
            if 'file' in request.files:
                file = request.files['file']
                # log('file', file)
                u.avatar = add_img(file)

            u.username = name
            if pwd is not '':
                u.password = User.salted_password(pwd)
            u.area = area
            u.job = job
            u.save()
            return render_template('user/setting.html', msg='修改成功', user=u)

def allow_img(filename):
    suffix = filename.split('.')[-1]
    from config import accept_user_img_type
    return suffix in accept_user_img_type

def add_img(file):
    if file.filename == '':
        return redirect(request.url)

    if allow_img(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(user_img_director, filename))
        return filename
    else:
        return ''

@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(user_img_director, filename)

@main.route("/people")
def people():
    user = current_user()
    if user is None:
        return redirect(url_for('user.login'))
    qu = Question.find_all(uid=user.id)
    an = Answer.find_all(uid=user.id)

    return render_template("user/people.html", user=user, qu=qu, an=an)
