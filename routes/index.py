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
from models.answer import Answer

main = Blueprint('index', __name__)

@main.route("/")
def index():
    user = current_user()
    answer = Answer.find_all()
    return render_template("index.html", user=user, answer=answer)