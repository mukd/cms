from flask import session #导入flask自带的session
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand   #flask_migrate==2.7
from cms_app import create_app,db,model #导入工厂函数

app = create_app('development')# 传入不同模式生产不同app
manage = Manager(app) #实例化管理器
Migrate(app,db) # 注入框架实例和数据实例
manage.add_command('db',MigrateCommand) ## 添加迁移命令

#@app.route('/cms')
#def hei():
    #session['name'] = 'clwy' #设置一个假的session,仅仅用来测试session
    #return session['name']

if __name__ == '__main__':
    print(app.url_map)  # 输出路由映射
    manage.run()
