import cms_app
from . import home_blue
from flask import render_template,request
import os
from werkzeug.utils import secure_filename
#from flask_paginate import Pagination
##from sqlalchemy.orm import sessionmaker
#from cms_app.model import *
@home_blue.route('/')  #使用当前蓝图对象注册路由
def index():
    return render_template('admin/index/index.html')

#@home_blue.route('/student/')
#def login():
    #return render_template('home/student.html')

#@home_blue.route('/result',methods=['POST','GET'])
#def result():
    #if request.method == 'POST':
        ##return render_template('home/result.html',result=result)

#上传文件
cms_app.config['UPLOAD_FOLDER'] = 'upload/'
@home_blue.route('/upload')
def upload_file():
    return render_template('home/upload.html')

@home_blue.route('/uploader',methods = ['GET','POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(cms_app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

        return 'file uplaod successfully!'
    else:
        return render_template('home/upload.html')
