import json
import re
from werkzeug.security import generate_password_hash
from . import admin_bule #导入蓝图对象
from flask import render_template, url_for, flash, redirect, session, request, jsonify
from cms_app.model.models import User
from cms_app import db
from cms_app.utils.common import login_required #引入装饰器


#后台注册
@admin_bule.route('/admin/user/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        if not data['username']:
            return jsonify(status=0,msg='请填写用户名')
        if not data['password']:
            return jsonify(status=0,msg='请填写密码')
        if data['check_password'] != data['password']:
            return jsonify(status=0,msg='两次密码不一致')
        if not re.match(r'1[3456789]\d{9}$',data['mobile']):
            return jsonify(status=0,msg='手机号格式错误')
        #根据手机号进行查询，确认用户是否注册
        user_mobile = User.query.filter_by(mobile=data['mobile']).first()
        if user_mobile:
            return jsonify(status=0,msg='手机号码已被注册')

        #构造模型类型对象，准备存储数据到user表
        user = User()
        user.mobile = data['mobile']
        user.username = data['username']
        user.password = generate_password_hash(data['password'])

        #把用户数据提交到数据库中
        db.session.add(user)
        db.session.commit()

        return jsonify(status=1,msg='注册成功')
    else:
        return render_template('admin/user/register.html')


#后台登录
@admin_bule.route('/admin/user/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('用户名或者密码输入错误！')
            return redirect(request.referrer)
        #登录成功后,存储用户信息到session
        session['user'] = user
        return redirect('/admin')
    return render_template('/admin/user/login.html')


#后台退出
@admin_bule.route('/admin/logout')
def logout():
    #退出的本质就是清除session
    session.pop('user')
    return redirect('/admin/user/login') #退出后跳转到登录界面

@admin_bule.route('/admin')
@login_required
def index():
    return render_template('/admin/index/index.html')
