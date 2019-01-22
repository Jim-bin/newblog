# -*- coding:utf-8 -*_

from functools import wraps
from flask import session, redirect, url_for


# 登录限制装饰器
def log_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper