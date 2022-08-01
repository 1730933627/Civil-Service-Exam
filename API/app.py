from flask_migrate import Migrate
from flask_cors import CORS
from config.dbInit import dbInitMain
import config.dbConfig as dbConfig
from module.route import server
from module.model import *

CORS(app, resources={r'/*': {"origins": "*"}}, supports_credentials=True)
app.config.from_object(dbConfig)
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(server, url_prefix='/')


if __name__ == '__main__':
    # 数据库初始化
    # dbInitMain()
    # 插入数据
    # insert()
    # 正式模式 debug=False,  调试模式 debug=True
    app.run(debug=False, port=8860, threaded=True, host='127.0.0.1')
