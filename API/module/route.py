import json
from flask import request, render_template, send_file, Blueprint
from linkSQL import *  # 数据库连接模块
from personnel import matriculate as matriculateConduct
from writePDF import generate_pdf
from module.getTime import getTime

server = Blueprint("server", __name__)


@server.route('/', methods=['get', "post"])
def index():
    res = {'status': 200, 'err': 0, 'msg': "success"}
    return json.dumps(res, ensure_ascii=False)
    # return render_template('index.html')


# ==================================================
#                       查询
# ==================================================


@server.route('/getStudent', methods=["GET"])
def getStudent():
    data = linkData().student()
    res = {'status': 200, 'err': 0, "data": data}
    return json.dumps(res, ensure_ascii=False)


@server.route('/byPhone', methods=["POST"])
def byPhone():
    numberP = request.values.get("numberP")
    if numberP is None:
        name = request.values.get("name")
        number = request.values.get("number")
        person = linkData().byPhoneGetPerson(name, number)
    else:
        person = linkData().getStudentP(numberP)
    if len(person) == 0:
        return json.dumps({'status': 201, 'err': 0, "msg": "查不到该学生"}, ensure_ascii=False)
    res = {'status': 200, 'err': 0, "data": person}
    return json.dumps({'status': 200, 'err': 0, "data": res}, ensure_ascii=False)


@server.route('/getPerson', methods=["POST"])
def getPerson():
    studentId = request.values.get("studentId")
    data = linkData().person(studentId)
    res = {'status': 200, 'err': 0, "data": data}
    return json.dumps(res, ensure_ascii=False)


@server.route('/login', methods=['POST'])
def login():
    account = request.values.get("account")
    numberP = request.values.get("numberP")
    password = request.values.get("password")
    if numberP is None:
        try:
            info = linkData().getAdmin(account)[0]
            if password == info['password']:
                return json.dumps({'status': 200, 'err': 0, 'msg': info['permission']}, ensure_ascii=False)
            else:
                return json.dumps({'status': 201, 'err': 0, 'msg': "password error"}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'status': 202, 'msg': "account error"}, ensure_ascii=False)
    else:
        try:
            info = linkData().getStudentP(numberP)[0]
            if password == info['password']:
                return json.dumps({'status': 200, 'err': 0, 'msg': info["studentId"]}, ensure_ascii=False)
            else:
                return json.dumps({'status': 201, 'err': 0, 'msg': "password error"}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'status': 202, 'msg': "account error"}, ensure_ascii=False)


@server.route('/getMatriculate', methods=["POST"])
def getMatriculate():
    matriculate = linkData().getMatriculateStudent()
    unmatriculate = linkData().getUnmatriculate()
    matriculateConduct()
    res = {'status': 200, 'err': 0, "matriculate": matriculate, "unmatriculate": unmatriculate}
    return json.dumps({'status': 200, 'err': 0, "data": res}, ensure_ascii=False)


@server.route('/downloadPDF', methods=["GET"])
def downloadPDF(file="data\\studentStatus.pdf"):
    studentId = request.values.get("studentId")
    name = request.values.get("name")
    profession = request.values.get("profession")
    sumScore = request.values.get("sumScore")
    conditionId = request.values.get("conditionId")
    fractions = request.values.get("fractions")
    methods = request.values.get("method")
    try:
        if methods is None:
            generate_pdf(studentId, methods='录取', name=name, profession=profession, sumScore=sumScore,
                         conditionId=conditionId, fractions=fractions)
        else:
            generate_pdf(studentId, methods="准考证")
    except Exception as e:
        print(e)
    return send_file("..\\" + file, attachment_filename='{}-{}.pdf'.format(studentId, name))


# ==================================================
#                       插入
# ==================================================

@server.route('/insertStudent', methods=['post'])
def insertStudent():
    try:
        dates = linkData().registerDate()
        if getTime().timeRange(dates[0], dates[1], dates[2]):
            del dates
        else:
            return json.dumps({'status': 203, 'msg': '注册时间已过'}, ensure_ascii=False)
    except IndexError:
        return json.dumps({'status': 204, 'msg': '注册还未开始'}, ensure_ascii=False)
    studentId = request.values.get("studentId")
    name = request.values.get("name")
    sex = request.values.get("sex")
    profession = request.values.get("profession")
    birthday = request.values.get("birthday")
    province = request.values.get("province")
    education = request.values.get("education")
    password = request.values.get("password")
    numberP = request.values.get("numberP")
    number = request.values.get("number")
    try:
        linkData().studentSignUp(studentId, name, sex, profession, number, birthday, province, education, numberP)
        linkData().studentAccount(studentId, numberP, password)
        return json.dumps({'status': 200, 'err': 0, 'msg': "success", "studentId": studentId}, ensure_ascii=False)
    except Exception as e:
        print(e)
        if int(str(e)[1:5]) == 1062:
            if str(e)[5:].split(" ")[-1][1:-3] == "numberP":
                return json.dumps({'status': 205, 'msg': '电话号已存在'}, ensure_ascii=False)
            else:
                return json.dumps({'status': 201, 'msg': '身份证已存在'}, ensure_ascii=False)
        else:
            return json.dumps({'status': 202, 'msg': '信息不能为空'}, ensure_ascii=False)


@server.route('/matriculate', methods=['POST'])
def matriculate(studentId=None):
    if studentId is None:
        studentId = request.values.get("studentId")
    else:
        pass
    try:
        person = linkData().person(studentId)[0]
    except Exception as e:
        return json.dumps({'status': 202, 'msg': "未查到该学生"}, ensure_ascii=False)
    if person["sumScore"] is None:
        return json.dumps({'status': 201, 'msg': "该学生没有成绩"}, ensure_ascii=False)
    condition = linkData().getFractions(person["profession"])[0]  # 获得分数线
    count = linkData().getMatriculateSum(person["profession"])[0]["count(*)"]  # 获得已录取人数
    if person["sumScore"] >= condition["fractions"] and count <= condition["nums"]:  # 满足条件
        person["conditionId"] = condition["conditionId"]
        try:
            linkData().matriculateIn(person["studentId"], person["name"], person["profession"], person["sumScore"],
                                     person["conditionId"])
            del person["score"]
            del person["date"]
            return json.dumps({'status': 200, 'msg': person}, ensure_ascii=False)
        except Exception as e:
            if int(str(e)[1:5]) == 1062:
                res = linkData().person(person["studentId"], "matriculate")[0]
                return json.dumps({'status': 200, 'msg': res}, ensure_ascii=False)
            else:
                return json.dumps({'status': 404, 'msg': e}, ensure_ascii=False)
    else:  # 不满足条件
        person["fractions"] = condition["fractions"]
        try:
            linkData().unmatriculateIn(person["studentId"], person["name"], person["profession"], person["sumScore"],
                                       person["fractions"])
            del person["score"]
            del person["date"]
            return json.dumps({'status': 200, 'msg': person}, ensure_ascii=False)
        except Exception as e:
            if int(str(e)[1:5]) == 1062:
                res = linkData().person(person["studentId"], "unmatriculate")[0]
                return json.dumps({'status': 200, 'msg': res}, ensure_ascii=False)
            else:
                return json.dumps({'status': 404, 'msg': e}, ensure_ascii=False)


# ==================================================
#                       更新
# ==================================================

@server.route('/updatePerson', methods=['POST'])
def updatePerson():
    oldStudentId = request.values.get("oldStudentId")
    studentId = request.values.get("studentId")
    if not oldStudentId == studentId:
        return json.dumps({'status': 201, 'err': 0, 'msg': "编号不可更改"}, ensure_ascii=False)
    name = request.values.get("name")
    sex = request.values.get("sex")
    number = request.values.get("number")
    numberP = request.values.get("numberP")
    education = request.values.get("education")
    province = request.values.get("province")
    profession = request.values.get("profession")
    try:
        # print(oldStudentId, name, sex, number, profession, province, education, numberP)
        linkData().personUpdate(oldStudentId, name, sex, number, profession, province, education, numberP)
        return json.dumps({'status': 200, 'err': 0, 'msg': "success"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({'status': 202, 'err': 0, 'msg': str(e)}, ensure_ascii=False)


@server.route('/studentAllow', methods=['POST'])
def studentAllow():
    studentIds = request.values.get("studentIds")
    status = 0
    for item in eval("[" + studentIds + "]"):
        try:
            linkData().studentAllow(item)
        except Exception as e:
            status += 1
    return json.dumps({'status': 200, 'err': 0, 'msg': status}, ensure_ascii=False)


@server.route('/updateScore', methods=['POST'])
def updateScore():
    studentId = request.values.get("studentId")
    score = request.values.get("score")
    sumScore = request.values.get("sumScore")
    try:
        allow = linkData().person(studentId)[0]["allow"]  # 获得数据库allow信息
    except Exception as e:
        allow = None
    if allow == "1" or allow == 1:
        try:
            linkData().scoreSignIn(studentId, score, sumScore, allow)
            matriculate(studentId)
            return json.dumps({'status': 200, 'err': 0, 'msg': "success"}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'status': 201, 'msg': "没有公司"}, ensure_ascii=False)
    else:
        return json.dumps({'status': 202, 'msg': "未经允许的学生id"}, ensure_ascii=False)


# ==================================================
#                       删除
# ==================================================

@server.route('/studentDelete', methods=["POST"])
def studentDelete():
    studentIds = request.values.get("studentIds")
    status = 0
    for item in eval("[" + studentIds + "]"):
        try:
            linkData().deleteStudent(item)
        except Exception as e:
            status += 1
    return json.dumps({'status': 200, 'err': 0, "msg": "成功删除"}, ensure_ascii=False)
