import os
import mysql.connector as mysqlCon
from config.dbConfig import *
import time


# 创建数据库
def createDB():
    print("开始创建数据库")
    mydb = mysqlCon.connect(
        host=hostname,
        user=username,
        passwd=password,
        auth_plugin='mysql_native_password',
        charset="utf8"
    )
    myCursor = mydb.cursor()
    try:
        myCursor.execute("CREATE DATABASE {}".format(database))
        myCursor.close()
        initDB()
    except mysqlCon.errors.DatabaseError:
        print("已有数据库")
        updateDB()


def updateDB():
    print("开始更新数据库")
    os.system('chcp 65001')
    path = os.getcwd()
    with open("config/dbInit.bat", "w") as f:
        f.write("cd {}\n".format(path))
        f.write("flask db migrate\n")
        f.write("flask db upgrade\n")
        f.write("start cmd /c del /q/s dbInit.bat & exit\n")
        f.write("exit")
        f.close()
    os.chdir("config")
    os.system(r"start dbInit.bat")


def initDB():
    print("开始初始化数据库")
    os.system('chcp 65001')
    path = os.getcwd()
    os.system("rmdir /q/s {}".format("migrations"))
    with open("config/dbInit.bat", "w") as f:
        f.write("cd {}\n".format(path))
        f.write("flask db init\n")
        f.write("flask db migrate\n")
        f.write("flask db upgrade\n")
        f.write("start cmd /c del /q/s dbInit.bat & exit\n")
        f.write("exit")
        f.close()
    os.chdir("config")
    os.system(r"start dbInit.bat")


def dbInitMain():
    createDB()
    time.sleep(10)


if __name__ == "__main__":
    os.chdir("../")
    dbInitMain()
