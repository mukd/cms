import time
from . import home_blue
from flask import render_template, request, session
from cms_app.utils.common import login_limt
from cms_app import db
from ..model import User, Blog, Comment

#写博客页面
@home_blue.route('/writeBlog',methods=['POST','GET'])
@login_limt
def writeblog():
    if request.method == 'GET':
        return render_template('home/writeBlog.html')
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        username = session.get('username')
        #获取当前系统时间
        create_time = time.strftime('%Y-%m-%d %H:%M:%S')
        user = User.query.filter(User.username==username).first()
        blog = Blog(title=title,text=text,create_time=create_time,user_id=user.id)
        db.session.add(blog)
        db.session.commit()
        blog = Blog.query.filter(Blog.create_time==create_time).first()
        return render_template('home/blogSuccess.html',title=title,id=blog.id)

#展示全部博客
@home_blue.route('/blogAll', methods=['GET'])
@login_limt
def main():
    return render_template("home/blogAll.html")
@home_blue.route('/get_data',methods=['POST'])
@login_limt
def get_data():
    data = Blog.query.order_by(Blog.id).all()
    limit = int(request.form.get("pageSize"))
    page = int(request.form.get("currentPage"))
    start = (page - 1) * limit
    end = page * limit if len(data) > page * limit else len(data)
    ret = [{"id": data[i].id, "name": data[i].title,'create_time':data[i].create_time} for i in range(start, end)]
    return {"data": ret, "count": len(data)}

''''
#查看个人博客
@home_blue.route('/show_data',methods=['POST'])
@login_limt
def myBlog():
    username = session.get('username')
    user = User.query.filter(User.username == username).first()
    data = Blog.query.filter(Blog.user_id == user.id).order_by(Blog.create_time.desc()).all()
    limit = int(request.form.get("pageSize"))
    page = int(request.form.get("currentPage"))
    start = (page - 1) * limit
    end = page * limit if len(data) > page * limit else len(data)
    ret = [{"id": data[i].id, "name": data[i].title, 'create_time': data[i].create_time} for i in range(start, end)]
    return {"data": ret, "count": len(data)}

@home_blue.route('/myBlog',methods=['GET'])
@login_limt
def main_myblog():
    return render_template('home/myBlog.html')
'''

#查看个人博客
@home_blue.route('/myBlog')
@login_limt
def article():
    # 查看文章列表
    username = session.get('username')
    user = User.query.filter(User.username == username).first()
    page = request.args.get('page', 1, type=int)
    pagination = Blog.query.filter(Blog.user_id == user.id).order_by(Blog.create_time).paginate(page, per_page=10, error_out=False)
    post_list = pagination.items
    return render_template('home/article.html', post_list=post_list, pagination=pagination)

# 博客详情页面
@home_blue.route('/showBlog/<id>')
def showBlog(id):
    blog = Blog.query.filter(Blog.id == id).first()
    comment = Comment.query.filter(Comment.blog_id == blog.id)
    return render_template("home/showBlog.html", blog=blog, comment=comment)

# 博客修改
@home_blue.route("/update/<id>", methods=['POST', 'GET'])
@login_limt
def update(id):
    if request.method == 'GET':
        blog = Blog.query.filter(Blog.id == id).first()
        return render_template('home/updateBlog.html', blog=blog)
    if request.method == 'POST':
        id = request.form.get("id")
        title = request.form.get("title")
        text = request.form.get("text")
        blog = Blog.query.filter(Blog.id == id).first()
        blog.title = title
        blog.text = text
        db.session.commit()
        return render_template('home/blogSuccess.html', title=title, id=id)

# 删除博客
@home_blue.route("/delete/<int:id>",methods=['GET','POST'])
@login_limt
def delete(id):
    blog = Blog.query.filter(Blog.id == id).first()
    if blog:
        db.session.delete(blog)
        db.session.commit()
        return {
            'state': True,
            'msg': "删除成功！"
        }

#评论
@home_blue.route('/comment',methods=['POST'])
@login_limt
def comment():
    text = request.values.get('text')
    blogId = request.values.get('blogId')
    username = session.get('username')
    #获取当前系统时间
    create_time = time.strftime("%Y-%m-%d %H:%M:%S")
    user = User.query.filter(User.username==username).first()
    comment = Comment(text=text,create_time=create_time,blog_id=blogId,user_id=user.id)
    db.session.add(comment)
    db.session.commit()
    return {
        'success':True,
        'message':'评论成功！',
    }
