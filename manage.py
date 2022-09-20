from flask import session,render_template#导入flask自带的session
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand   #flask_migrate==2.7
from cms_app import create_app,db #导入工厂函数
from cms_app.model import User

app = create_app('development')# 传入不同模式生产不同app
manage = Manager(app) #实例化管理器
Migrate(app,db) # 注入框架实例和数据实例
manage.add_command('db',MigrateCommand) ## 添加迁移命令

#@app.route('/cms')
#def hei():
    #session['name'] = 'clwy' #设置一个假的session,仅仅用来测试session
    #return session['name']

# 上下文处理器，定义用户当前是否登录状态，全局可访问
@app.context_processor
def login_statue():
    # 获取session中的username
    username = session.get('username')
    # 如果username不为空，则已登录，否则没有登录
    if username:
        try:
            # 登录后，查询用户信息并返回用户信息
            user = User.query.filter(User.username == username).first()
            if user:
                return {"username": username, 'mobile': user.mobile, 'password': user.password}
        except Exception as e:
            return e
    # 如果没有登录，返回空
    return {}

#404页面
app.errorhandler(404)
def page_not_found(e):
    return render_template('admin/404.html'), 404

#505页面
app.errorhandler(500)
def internal_server_error(e):
    return render_template('admin/404.html'), 500



if __name__ == '__main__':
    print(app.url_map)  # 输出路由映射
    manage.run()
