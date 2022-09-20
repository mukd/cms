import cms_app
from . import home_blue
from flask import render_template,request
import os
from werkzeug.utils import secure_filename

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
