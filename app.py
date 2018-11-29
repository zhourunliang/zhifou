from flask import Flask

import config

app = Flask(__name__)
# 设置 secret_key 来使用 flask 自带的 session
# 这个字符串随便你设置什么内容都可以
app.secret_key = config.secret_key

from utils import (
    log,
    current_user,
    time_format,
)

from routes.index import main as index_routes
from routes.test import main as test_routes
from routes.user import main as user_routes
from routes.question import main as question_routes
from routes.answer import main as answer_routes

app.register_blueprint(index_routes)
app.register_blueprint(test_routes, url_prefix='/test')
app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(question_routes, url_prefix='/question')
app.register_blueprint(answer_routes, url_prefix='/answer')


@app.context_processor
def get_current_user():
    return dict(current_user=current_user)

@app.context_processor
def get_time_format():
    return dict(time_format=time_format)

# 运行代码
if __name__ == '__main__':
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    config = dict(
        debug=True,
        host='127.0.0.1',
        port=2000,
    )
    app.run(**config)

