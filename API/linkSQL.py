import pymysql
import config.dbConfig as dbConfig
from module.getTime import getTime


class linkData:
    def __init__(self):
        self.db = pymysql.connect(host=dbConfig.hostname, user=dbConfig.username, password=dbConfig.password,
                                  database=dbConfig.database, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.db.cursor()

    def getCondition(self):
        getData = "select * from conditions"
        try:
            self.cursor.execute(getData)
            datas = self.cursor.fetchall()
            return datas
        except Exception as e:
            raise e

    def conditionIn(self, cid, profession):
        insertInfo = "insert into conditions (conditionId,profession) values(%s,%s)"
        par = (cid, profession)
        try:
            self.cursor.execute(insertInfo, par)
            self.db.commit()
        except Exception as e:
            raise e

    def getFractions(self, profession):
        getData = "select * from conditions where profession='{}'".format(profession)
        try:
            self.cursor.execute(getData)
            datas = self.cursor.fetchall()
            return datas
        except Exception as e:
            raise e

    def fractionsIn(self, profession, fractions, nums):
        updateInfo = "UPDATE conditions SET fractions=\"{}\",nums='{}' WHERE profession='{}'".format(fractions, nums,
                                                                                                     profession)
        try:
            self.cursor.execute(updateInfo)
            self.db.commit()
        except Exception as e:
            raise e

    def person(self, studentId, table="students"):
        getData = "select * from {1} where studentId='{0}'".format(studentId, table)
        try:
            self.cursor.execute(getData)
            datas = self.cursor.fetchall()
            return datas
        except Exception as e:
            raise e

    def personUpdate(self, studentId, name, sex, number, profession, province, education, numberP):
        # print(studentId, name, sex, number, profession, province, education, numberP)
        updater = "UPDATE students SET name='{}',sex='{}',number='{}',profession='{}',province='{}',education='{}',numberP='{}' WHERE studentId='{}'".format(
            name, sex, number, profession, province, education, numberP, studentId)
        try:
            self.cursor.execute(updater)
            self.db.commit()
        except Exception as e:
            raise e

    def student(self):
        getData = "select * from students order by sumScore desc"
        try:
            self.cursor.execute(getData)
            datas = self.cursor.fetchall()
            return datas
        except Exception as e:
            raise e

    def studentAllow(self, studentId):
        updateInfo = "update students set allow=1 WHERE studentId='{}'".format(studentId)
        try:
            self.cursor.execute(updateInfo)
            self.db.commit()
        except Exception as e:
            raise e

    def studentSignUp(self, studentId, name, sex, profession, number, birthday, province, education, numberP):
        insertInfo = "insert into students " \
                     "(studentId,name,sex,profession,number,date,birthday,province,education,numberP) " \
                     "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        par = (
            studentId, name, sex, profession, number, getTime().returnStrDate(), birthday, province, education, numberP)
        try:
            self.cursor.execute(insertInfo, par)
            self.db.commit()
        except Exception as e:
            raise e

    def studentAccount(self, studentId, numberP, password):
        insertInfo = "insert into account_s (studentId,numberP,password) values(%s,%s,%s)"
        par = (studentId, numberP, password)
        try:
            self.cursor.execute(insertInfo, par)
            self.db.commit()
        except Exception as e:
            raise e

    def scoreSignIn(self, studentId, score, sumScore, allow):
        if allow is None:
            raise 202
        updateInfo = "UPDATE students SET score=\"{}\",sumScore='{}' WHERE studentId='{}'".format(score, sumScore,
                                                                                                  studentId)
        try:
            self.cursor.execute(updateInfo)
            self.db.commit()
        except Exception as e:
            raise e

    def matriculateIn(self, studentId, name, profession, sumScore, conditionId):
        insertInfo = "insert into matriculate (studentId,name,profession,sumScore,conditionId) values(%s,%s,%s,%s,%s)"
        par = (studentId, name, profession, sumScore, conditionId)
        try:
            self.cursor.execute(insertInfo, par)
            self.db.commit()
        except Exception as e:
            raise e

    def getMatriculateStudent(self):
        getInfo = "select * from matriculate"
        try:
            self.cursor.execute(getInfo)
            datas = self.cursor.fetchall()
            return datas
        except Exception as e:
            raise e

    def getMatriculateSum(self, profession):
        getCount = "select count(*) from matriculate where profession='{}'".format(profession)
        try:
            self.cursor.execute(getCount)
            datas = self.cursor.fetchall()
            return datas
        except Exception as e:
            raise e

    def getUnmatriculate(self):
        getInfo = "select * from unmatriculate"
        try:
            self.cursor.execute(getInfo)
            datas = self.cursor.fetchall()
            return datas
        except Exception as e:
            raise e

    def unmatriculateIn(self, studentId, name, profession, sumScore, fractions):
        insertInfo = "insert into unmatriculate (studentId,name,profession,sumScore,fractions) values(%s,%s,%s,%s,%s)"
        par = (studentId, name, profession, sumScore, fractions)
        try:
            self.cursor.execute(insertInfo, par)
            self.db.commit()
        except Exception as e:
            raise e

    def getAdmin(self, account):
        getter = "select * from admin where account='{}'".format(account)
        try:
            self.cursor.execute(getter)
            datas = self.cursor.fetchall()
            return datas
        except Exception as e:
            raise e

    def getStudentP(self, numberP):
        getter = "select * from account_s where numberP='{}'".format(numberP)
        try:
            self.cursor.execute(getter)
            datas = self.cursor.fetchall()
            return datas
        except Exception as e:
            raise e

    def deleteStudent(self, studentId):
        deleter = "delete from students where studentId='{}'".format(studentId)
        try:
            self.cursor.execute(deleter)
            self.db.commit()
        except Exception as e:
            raise e

    def registerDate(self):
        getter = "select * from registerdate"
        try:
            self.cursor.execute(getter)
            datas = self.cursor.fetchall()[-1]
            dateStart = str(datas["dateStart"])
            dateEnd = str(datas["dateEnd"])
            endTime = str(datas["time"])
            return dateStart, dateEnd, endTime
        except Exception as e:
            raise e

    def byPhoneGetPerson(self, name, number):
        getter = "select * from students where name='{}' and number='{}'".format(name, number)
        try:
            self.cursor.execute(getter)
            datas = self.cursor.fetchall()
            return datas
        except Exception as e:
            raise e

    def __del__(self):
        self.cursor.close()
        self.db.close()
