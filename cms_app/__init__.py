from flask import Flask
from config import config  # 导入配置信息
from flask_sqlalchemy import SQLAlchemy #导入数据库扩展
#from flask_session import Session #导入session扩展
app = Flask(__name__)
db = SQLAlchemy() #去掉实例化

#定义工厂函数，生产app
def create_app(config_name): #传入要生产的模式参数
    app.config.from_object(config[config_name]) #读取对应的配置
    db.init_app(app) #通过init_app去实例化db对象
    #Session(app)  #实例化Session

    #注册前台蓝图
    from cms_app.home import home_blue
    app.register_blueprint(home_blue)
    from cms_app.admin import admin_bule
    app.register_blueprint(admin_bule)
    from cms_app.admin.type import type_blue
    app.register_blueprint(type_blue)
    return app #最后返回当前app
