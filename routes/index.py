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

main = Blueprint('index', __name__)

@main.route("/")
def index():
    u = {'name':'test'}
    return render_template("index.html", user=u)