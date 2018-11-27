from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    send_from_directory,
)
from routes import *
from utils import log
from config import user_img_director
from models.answer import Answer

main = Blueprint('index', __name__)

@main.route("/")
def index():
    user = current_user()
    answer = Answer.find_all()
    return render_template("index.html", user=user, answer=answer)

@main.route("/uploads/img/<filename>")
def uploads(filename):
    return send_from_directory(user_img_director, filename)