from flask import session,redirect
import functools

#自定义装饰器，封装用户的登录信息，登录验证装饰器
def login_required(func):
    #让被装饰器的函数数名的属性不会被改变
    @functools.wraps(func)
    def inner(*args,**kwargs):
        user = session.get('user')
        if not user:
            return redirect('/admin/user/login')
        return func(*args,**kwargs)

    return inner
