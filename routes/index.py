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
from models.question import Question

main = Blueprint('index', __name__)


@main.route("/")
def index():
    user = current_user()
    answer = Answer.find_all()
    question = Question.find_all()
    
    # log('answer', answer)
    # log('question', question)   
    list_data = sorted(answer + question, key = lambda i:int(i.created_time), reverse = True)
   
    return render_template("index.html", user=user, list_data=list_data, Answer=Answer)

@main.route("/uploads/img/<filename>")
def uploads(filename):
    return send_from_directory(user_img_director, filename)

@main.route("/search")
def search():
    keyword = request.args.get('keyword')
    qu = Question.find_all(title=keyword)
    # log(keyword)
    # log(qu)
    return render_template("search.html", qu=qu, keyword=keyword)

