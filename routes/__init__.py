from flask import (
    session,
    Blueprint,
)

from models.user import User

main = Blueprint('/', __name__)

def current_user():
    uid = session.get('user_id', '')
    if uid:
       u = User.find_by(id=int(uid))
    else:
        u = None
    return u
