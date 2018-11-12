from flask import session

from models.user import User


def current_user():
    uid = session.get('user_id', '')
    if uid:
       u = User.find_by(id=int(uid))
    else:
        u = None
    return u