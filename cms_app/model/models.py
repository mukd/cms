from datetime import datetime
from werkzeug.security import check_password_hash
from cms_app import db

class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime,default=datetime.now) #记录创建时间
    update_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now) #记录更新时间


class User(BaseModel,db.Model):
    """管理员"""
    __tablename__ = 'user'

    id = db.Column(db.Integer,primary_key=True) #用户编号
    username = db.Column(db.String(32),unique=True,nullable=False) #用户昵称
    password = db.Column(db.String(128),nullable=False) #加密密码
    mobile  = db.Column(db.String(11),unique=True,nullable=False) #手机号
    last_login = db.Column(db.DateTime,default=datetime.now) #最后一次登录时间

    def check_password(self,password):
        return check_password_hash(self.password,password)

    def to_dick(self):
        resp_dict = {
            'id':self.id,
            'username':self.username,
            'password':self.password,
            'mobile':self.mobile,
            "register": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": self.last_login.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return resp_dict

