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
from config import user_file_director

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
    return redirect(url_for('user.register'))


@main.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('user/register.html')
    else:     
        form = request.form
        # 用类函数来判断
        
        u = User.register(form)
        if u is None:
            log('注册失败')
            
            return redirect(url_for('.index'))
        else:
            return redirect(url_for('.index'))


@main.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')
    else:       
        form = request.form
        u = User.validate_login(form)
        if u is None:
            log('login fail')
            # 转到 topic.index 页面
            return redirect(url_for('topic.index'))
        else:
            log('login success')
            # session 中写入 user_id
            session['user_id'] = u.id
            # 设置 cookie 有效期为 永久
            session.permanent = True
            return redirect(url_for('topic.index'))


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)


def allow_file(filename):
    suffix = filename.split('.')[-1]
    from config import accept_user_file_type
    return suffix in accept_user_file_type


@main.route('/addimg', methods=["POST"])
def add_img():
    u = current_user()

    if u is None:
        return redirect(url_for(".profile"))

    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if allow_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(user_file_director, filename))
        u.user_image = filename
        u.save()

    return redirect(url_for(".profile"))


@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(user_file_director, filename)