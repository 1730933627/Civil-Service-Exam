hostname = '127.0.0.1'
database = 'servant'
username = 'username'
password = 'password'
port = '3306'
db_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(username, password, hostname, port, database)

SQLALCHEMY_DATABASE_URI = db_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
