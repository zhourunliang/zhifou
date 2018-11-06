from flask import Flask

import config

app = Flask(__name__)
from routes.index import main as index_routes
from routes.test import main as test_routes
from routes.user import main as user_routes
app.register_blueprint(index_routes)
app.register_blueprint(test_routes, url_prefix='/test')
app.register_blueprint(user_routes, url_prefix='/user')

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