import re
from flask import render_template, url_for, flash, redirect, session, request, jsonify, json
from werkzeug.security import generate_password_hash, check_password_hash
from cms_app import db
from cms_app.model.models import User
from . import admin_bule  # 导入蓝图对象
from ..utils.captcha import  imgCode
from ..utils.common import login_limt

#后台首页
@admin_bule.route('/')
def hello():
    return render_template('admin/index/index.html')

#后台注册
@admin_bule.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        if not data['username']:
            return jsonify(status=0, msg='请填写用户名')
        if not data['password']:
            return jsonify(status=0, msg='请填写密码')
        if data['check_password'] != data['password']:
            return jsonify(status=0, msg='两次密码不一致')
        if not re.match(r'1[3456789]\d{9}$', data['mobile']):
            return jsonify(status=0, msg='手机号格式错误')
        # 根据手机号进行查询，确认用户是否注册
        user_mobile = User.query.filter_by(mobile=data['mobile']).first()
        username = User.query.filter_by(username=data['username']).first()
        if user_mobile:
            return jsonify(status=0, msg='手机号码已被注册')
        elif username:
            return jsonify(status=0,msg='用户名已注册')
        # 构造模型类型对象，准备存储数据到user表
        user = User()
        user.mobile = data['mobile']
        user.username = data['username']
        user.password = generate_password_hash(data['password'])
        # 把用户数据提交到数据库中
        db.session.add(user)
        db.session.commit()
        return jsonify(status=1, msg='注册成功')
    else:
        return render_template('admin/user/register.html')

#后台登录
@admin_bule.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        captcha = request.form.get('captcha').lower()
        user = User.query.filter(User.username==username).first()
        if captcha != session['imageCode'].lower():
            flash('图片验证码错误')
            return redirect(request.referrer)
        if user is None or not user.check_password(password):
            flash('用户名者或密码错误！')
            return redirect(request.referrer)
        #登录成功后,存储用户信息到session
        session['username'] = user.username

        session.permanent = True
        return redirect(url_for('admin_bule.hello'))
    return render_template('admin/user/login.html')

#验证码
@admin_bule.route('/imgCode')
def generate_image_code():
    return imgCode()

#修改密码
@admin_bule.route('/updatePwd',methods=['POST','GET'])
@login_limt
def update():
    if request.method == 'GET':
        return render_template('admin/index/updatePwd.html')
    if request.method == 'POST':
        lodPwd = request.form.get('lodPwd')
        newPwd1 = request.form.get('newPwd1')
        newPwd2 = request.form.get('newPwd2')
        username = session.get('username')
        user = User.query.filter(User.username==username).first()
        if check_password_hash(user.password,lodPwd):
            if newPwd1 != newPwd2:
                flash('两次密码不一致！')
                return render_template('admin/index/updatePwd.html')
            else:
                user.password = generate_password_hash(newPwd2)
                db.session.commit()
                flash('修改成功！')
                return render_template('admin/index/updatePwd.html')
        else:
            flash('原密码错误！')
            return render_template('admin/index/updatePwd.html')

#关于页面
@admin_bule.route('/about')
def about():
    return render_template('admin/about.html')

#后台退出
@admin_bule.route('/logout')
def logout():
    #退出的本质就是清除session
    #session.pop('user')
    session.clear()
    #return redirect('/admin/user/login') #退出后跳转到登录界面
    return redirect(url_for('admin_bule.hello'))
