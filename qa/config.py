SECRET_KEY = '你的密码加密密钥'


# 数据库配置
HOSTNAME = '127.0.0.1'
PORT = 3306
USERNAME = '数据库用户'
PASSWORD = '密码'
DATABASE = '数据库名'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# 邮箱配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = '服务器邮箱'
MAIL_PASSWORD = '邮箱授权码'
MAIL_DEFAULT_SENDER = '服务器邮箱'
