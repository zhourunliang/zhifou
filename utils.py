import os.path
import time
import json

import arrow

def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)

def current_user():
    from flask import session
    from models.user import User
    uid = session.get('user_id', '')
    if uid:
       u = User.find_by(id=int(uid))
    else:
        u = None
    return u

def time_format(time):
    format_time = arrow.get(time)
    format_time = format_time.humanize(locale='zh_cn')
    return format_time
