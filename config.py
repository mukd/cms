from redis import StrictRedis
class Config:
    DEBUG = None

    SECRET_KEY = 'clwy'  # 设置密钥

    # 配置数据库
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost:3306/cms'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 配置redis连接信息，实现状态保持，存储用户的session信息
    REDIS_HOST = '127.0.0.1'  # 配置 Redis 主机地址
    REDIS_PORT = 6379  # 配置 Redis 本地端口
    SESSION_TYPE = 'redis'  # 连接类型
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 实例化传入参数
    SESSION_USE_SIGNER = True  # 签名
    PERMANENT_SESSION_LIFETIME = 86400  # 设置session过期时间



# 定义开发模式的配置
class developmentConfig(Config):
    DEBUG = True


# 定义生产模式的配置
class productionConfig(Config):
    DEBUG = False


# 定义字典，方便取值
config = {
    'development': developmentConfig,
    'production': productionConfig
}