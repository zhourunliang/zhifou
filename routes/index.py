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

main = Blueprint('index', __name__)

@main.route("/")
def index():
    user = current_user()
    return render_template("index.html", user=user)