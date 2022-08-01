from module.exts import db, app


# 管理员账户  admin
class admin_s(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    account = db.Column(db.String(20))
    password = db.Column(db.String(20))
    permission = db.Column(db.Integer, default=0, server_default='0')


# conditions
class conditions_s(db.Model):
    __tablename__ = 'conditions'
    conditionId = db.Column(db.Integer, primary_key=True, nullable=False)
    profession = db.Column(db.String(10), nullable=False)
    fractions = db.Column(db.Integer)
    nums = db.Column(db.Integer)


# registerDate
class registerdate_s(db.Model):
    __tablename__ = 'registerdate'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    dateStart = db.Column(db.Date, nullable=False)
    dateEnd = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)


# students
class students_s(db.Model):
    __tablename__ = 'students'
    studentId = db.Column(db.BigInteger, primary_key=True, nullable=False)  # 学生id
    birthday = db.Column(db.String(10))  # 2002/02/10
    province = db.Column(db.String(10))  # 省
    education = db.Column(db.String(6))  # 学历
    name = db.Column(db.String(10), nullable=False)
    sex = db.Column(db.String(4), nullable=False)
    profession = db.Column(db.String(10), nullable=False)
    number = db.Column(db.String(18), unique=True)  # 身份证
    date = db.Column(db.String(11))  # 时间
    score = db.Column(db.String(64))  # 成绩
    sumScore = db.Column(db.BigInteger)  # 总成绩
    allow = db.Column(db.Integer, default=0, server_default='0')  # 审核
    numberP = db.Column(db.String(11), nullable=False, unique=True)  # 电话号


class account_s(db.Model):
    __tablename__ = 'account_s'
    studentId = db.Column(db.BigInteger, db.ForeignKey('students.studentId', ondelete='CASCADE'), primary_key=True,
                          nullable=False)  # 学生id
    numberP = db.Column(db.String(11), nullable=False, unique=True)  # 电话号
    password = db.Column(db.String(30), nullable=False)  # 密码


# matriculate
class matriculate_s(db.Model):
    __tablename__ = 'matriculate'
    studentId = db.Column(db.BigInteger, db.ForeignKey('students.studentId', ondelete='CASCADE'), primary_key=True,
                          nullable=False)
    name = db.Column(db.String(10), nullable=False)
    profession = db.Column(db.String(10))
    sumScore = db.Column(db.BigInteger, nullable=False)
    conditionId = db.Column(db.Integer, nullable=False)


# unMatriculate
class unmatriculate_s(db.Model):
    __tablename__ = 'unmatriculate'
    studentId = db.Column(db.BigInteger, db.ForeignKey('students.studentId', ondelete='CASCADE'), primary_key=True,
                          nullable=False)
    name = db.Column(db.String(10), nullable=False)
    profession = db.Column(db.String(10))
    sumScore = db.Column(db.BigInteger)
    fractions = db.Column(db.BigInteger)


# place
class place_s(db.Model):
    __tablename__ = 'place'
    placeId = db.Column(db.BigInteger, db.ForeignKey('students.studentId', ondelete='CASCADE'), primary_key=True,
                        nullable=False)  # 对应的id
    province = db.Column(db.String(10), nullable=False)  # 省
    school = db.Column(db.String(10), nullable=False)  # 考试学校
    classroom = db.Column(db.String(10), nullable=False)  # 几号楼
    examRoom = db.Column(db.String(10), nullable=False)  # 考场号
    seat = db.Column(db.Integer, nullable=False)  # 座位号


def insert():
    with app.app_context():
        admin = admin_s(account='admin', password='admin')
        root = admin_s(account='root', password='root')
        stu1 = students_s(studentId=22178222947, birthday='2021-03-23', province='甘肃', education='研究生',
                          numberP='15446251450', name='大耗子', sex='男', profession='行政', number='624513200106261005',
                          score='["60","60","60"]', sumScore=180, allow=1, date='2022-06-01')
        stu2 = students_s(studentId=22178222946, birthday='2021-03-23', province='甘肃', education='研究生',
                          numberP='15446251451', name='zds', sex='男', profession='法律', number='622513200206267005',
                          score='["60","60","60"]', sumScore=180, allow=1, date='2022-06-01')
        stu3 = students_s(studentId=22178222945, birthday='2021-03-23', province='甘肃', education='研究生',
                          numberP='15446251452', name='琪亚娜卡斯兰娜', sex='女', profession='法律', number='624513200410216472',
                          score='["60","60","60"]', sumScore=180, allow=1, date='2022-06-01')
        stu4 = students_s(studentId=22178222944, birthday='2021-03-23', province='甘肃', education='研究生',
                          numberP='15446251453', name='刻晴', sex='女', profession='行政', number='624513200206042255',
                          score='["60","60","60"]', sumScore=180, allow=1, date='2022-06-01')
        stu5 = students_s(studentId=22178222943, birthday='2021-03-23', province='甘肃', education='研究生',
                          numberP='15446251454', name='甘雨', sex='女', profession='财经', number='624513200112035573',
                          score='["60","60","60"]', sumScore=180, allow=1, date='2022-06-01')
        stu6 = students_s(studentId=22178222941, birthday='2021-03-23', province='甘肃', education='研究生',
                          numberP='15446251455', name='德莉莎', sex='女', profession='法律', number='62451320030154482',
                          score='["60","60","60"]', sumScore=180, allow=1, date='2022-06-01')
        stu7 = students_s(studentId=22178222940, birthday='2021-03-23', province='甘肃', education='研究生',
                          numberP='15446251456', name='胡桃', sex='女', profession='行政', number='624513200207254437',
                          score='["60","60","60"]', sumScore=180, allow=1, date='2022-06-01')
        cond1 = conditions_s(conditionId=110, profession="法律", fractions=250, nums=64)
        cond2 = conditions_s(conditionId=120, profession="财经", fractions=240, nums=54)
        cond3 = conditions_s(conditionId=130, profession="行政", fractions=260, nums=62)
        reg = registerdate_s(dateStart='2022-06-01', dateEnd='2022-07-10', time='22:00:00')
        db.session.add_all([admin, root])
        db.session.add(reg)
        db.session.add_all([stu1, stu2, stu3, stu4, stu5, stu6, stu7])
        db.session.add_all([cond1, cond2, cond3])
        db.session.commit()
