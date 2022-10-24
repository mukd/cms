from flask import session, redirect
import functools

# 自定义装饰器，封装用户的登录信息，登录验证装饰器
def login_limt(func):
    # 让被装饰的函数名的属性不会被改变，
    @functools.wraps(func)
    def inner(*args, **kwargs):
        user = session.get('username')
        if not user:
            return redirect('/login')
        return func(*args, **kwargs)
    return inner