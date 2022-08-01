from linkSQL import linkData

# 根据分数录取学生
def matriculate():
    studentList = linkData().student()
    matriculateStudent = {}
    unmatriculateStudent = {}
    for item in linkData().getCondition():
        count = 0
        profession = item["profession"]
        fraction = item["fractions"]
        nums = item["nums"]
        for person in studentList:
            try:
                if person["profession"] == profession and person["sumScore"] >= fraction and count <= nums:
                    if not matriculateStudent.get(item["profession"], 0):
                        matriculateStudent[item["profession"]] = []
                    person["conditionId"] = item["conditionId"]
                    matriculateStudent[item["profession"]].append(person)
                elif person["profession"] == profession and (person["sumScore"] < fraction or count > nums):
                    if not unmatriculateStudent.get(item["profession"], 0):
                        unmatriculateStudent[item["profession"]] = []
                    person["fractions"] = item["fractions"]
                    unmatriculateStudent[item["profession"]].append(person)
            except TypeError:
                pass
    for item in matriculateStudent.values():
        for person in item:
            try:
                linkData().matriculateIn(person["studentId"], person["name"], person["profession"], person["sumScore"], person["conditionId"])
            except:
                pass
    for item in unmatriculateStudent.values():
        for person in item:
            try:
                linkData().unmatriculateIn(person["studentId"], person["name"], person["profession"], person["sumScore"], person["fractions"])
            except:
                pass


