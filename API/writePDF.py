import os
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont, TTFError

from linkSQL import linkData

# 增加的字体，支持中文显示,需要自行下载支持中文的字体
try:
    pdfmetrics.registerFont(TTFont('SimSun', 'data/SimSun.TTF'))
    pdfmetrics.registerFont(TTFont('SimSunBd', 'data/SimSunBold.ttf'))
except FileNotFoundError:
    pdfmetrics.registerFont(TTFont('SimSun', '../data/SimSun.TTF'))
    pdfmetrics.registerFont(TTFont('SimSunBd', '../data/SimSunBold.ttf'))
except TTFError:
    pdfmetrics.registerFont(TTFont('SimSun', '../data/SimSun.TTF'))
    pdfmetrics.registerFont(TTFont('SimSunBd', '../data/SimSunBold.ttf'))
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(fontName='SimSun', name='SimSun', leading=20, fontSize=18))
stylesheet = getSampleStyleSheet()

Title = stylesheet['Title']
Title.fontName = 'SimSunBd'


def table_model(studentId, name, profession, sumScore, condition, fractions):
    base = [
        ["考生考号", studentId],
        ["考生姓名", name],
        ["考生专业", profession],
        ["考生总分", sumScore],
    ]
    style = [
        # (列 行)(列 行)
        # 设置字体
        ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
        ('FONTSIZE', (0, 0), (-1, -1), 30),
        ('LEADING', (0, 0), (-1, -1), 40),
        # 合并单元格 (列,行)
        ('SPAN', (0, 0), (0, 0)),
        ('SPAN', (1, 1), (1, 1)),
        ('SPAN', (2, 2), (2, 2)),
        ('SPAN', (3, 3), (3, 3)),
        ('SPAN', (4, 4), (4, 4)),
        ('SPAN', (5, 5), (5, 5)),

        # 单元格背景
        ('BACKGROUND', (0, 0), (1, 0), HexColor('#548DD4')),
        ('BACKGROUND', (0, 1), (1, 1), HexColor('#DCDCDC')),
        ('BACKGROUND', (0, 2), (1, 2), HexColor('#FFFAFA')),
        ('BACKGROUND', (0, 3), (1, 3), HexColor('#DCDCDC')),
        ('BACKGROUND', (0, 4), (1, 4), HexColor('#FFFAFA')),
        ('BACKGROUND', (0, 5), (1, 5), HexColor('#DCDCDC')),

        # 字体颜色
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),

        # 对齐设置
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  

        # 单元格框线
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
    ]
    if condition is None:
        base.append(["分数线", fractions])
        base.append(["是否录取", "未录取"])
        style.append(('TEXTCOLOR', (1, 5), (1, 5), colors.red))
    else:
        base.append(["录取公司ID", condition])
        base.append(["是否录取", "已录取"])
        style.append(('TEXTCOLOR', (1, 5), (1, 5), colors.green))

    component_table = Table(base, style=style, colWidths=[200, 200], rowHeights=[75,75,75,75,75,75])
    return component_table


def admit(studentId, name, sex, profession, number, province, numberP):
    base = [
        ["身份信息"],
        ["准考证号：{}\n"
         "姓        名：{}\n"
         "性        别：{}\n"
         "专        业：{}\n"
         "证件类型：中华人民共和国居民身份证\n"
         "身份证号：{}\n"
         "籍        贯：{}\n"
         "电        话：{}".format(studentId, name, sex, profession, number, province, numberP)],

        ["时间安排"],
        ["考试日期:  2022-06-21\n"
         "报道时间:  08:20\n"
         "考试时间:  09:00-11:20"],

        ["考场安排"],
        ["考试地点:  天水师范学院\n"
         "考试教室:  2J211\n"
         "考  场  号:  068\n"
         "座  位  号:  04"],

        ["考生须知"],
        ["1.考试当日考生须携带相应科目准考证、报考时使用身份证件及学校规定其他证件按规定时间到达准考证上指定的考场，配\n"
         "合监考员完成健康检测、身份核对，考场签到表上签字，并按考点要求将与考试无关物品放置在指定位置。证件携带不齐全\n"
         "或不配合监考员完成健康检测、身份核对、签到及拒绝将与考试无关物品放置在指定位置的考生将不得进入考场，情节严重\n"
         "的将按违规处理。2.考生进入考场后须按准考证上的位置入座，否则按违规处理。3.考生须听从监考员指令，在规定时间打开\n"
         "试卷、作答和停止作答，否则按违规处理。4.考生在答题前，请认真完成以下内容:(1)请检查试题册背面条形码粘贴条、答题\n"
         "卡的印刷质量，如有问题及时向监考员反映，确认无误后完成以下两点要求;(2)请将试题册背面条形码粘贴条揭下后粘贴在答\n"
         "题卡1的条形码粘贴框内，并将姓名和准考证号填写在试题册背面相应位置;(3)请在答题卡1和答题卡2指定位置用黑色签字笔\n"
         "填写准考证号、姓名和学校名称，并用HB-2B铅笔将对应准考证号的信息点涂黑。5.在考试过程中出现突发事件导致考试无法\n"
         "正常进行时，考生须听从监考员安排，相关情况未解决之前，不得离开考场."],

        ["考点提示"],
        ["考场提示说明\n"
         "1.考生必须在规定的时间（上午8:45开始，下午14:45开始）入场，上午9:00，下午15:00后禁止入场。入场时必须主动出示本人\n"
         "准考证、有效身份证和学生证(毕业证复印件)，并接受监考人员安检。\n"
         "2.考生须携带2B铅笔（涂答题卡用）、黑色签字笔、橡皮等文具。禁止携带任何书籍、笔记、资料、报刊、草稿纸以及各种\n"
         "无线通讯工具、电子记事本等违规物品。\n"
         "3.考试结束后，考生应立即停止答卷，将试题册扣放在桌面上，经监考人员允许后方可离开考场，不得将答题卡和试题册带\n出考场。\n"
         "4.考生应自觉遵守考试纪律，诚信应考，拒绝作弊行为，凡发现有舞弊行为者，依据《天水师范学院学生违反考试纪律处分\n"
         "规定》给予严肃处理。"],
    ]
    style = [
        # (列 行)(列 行)
        # 设置字体
        ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
        ('FONTSIZE', (0, 1), (0, 1), 14),
        ('LEADING', (0, 1), (0, 1), 14),
        ('FONTSIZE', (0, 3), (0, 3), 14),
        ('LEADING', (0, 3), (0, 3), 14),
        ('FONTSIZE', (0, 5), (0, 5), 14),
        ('LEADING', (0, 5), (0, 5), 14),

        ('FONTNAME', (0, 0), (0, 0), 'SimSunBd'),
        ('FONTSIZE', (0, 0), (0, 0), 14),
        ('LEADING', (0, 0), (0, 0), 14),
        ('FONTNAME', (0, 2), (0, 2), 'SimSunBd'),
        ('FONTSIZE', (0, 2), (0, 2), 14),
        ('LEADING', (0, 2), (0, 2), 14),
        ('FONTNAME', (0, 4), (0, 4), 'SimSunBd'),
        ('FONTSIZE', (0, 4), (0, 4), 14),
        ('LEADING', (0, 4), (0, 4), 14),
        ('FONTNAME', (0, 6), (0, 6), 'SimSunBd'),
        ('FONTSIZE', (0, 6), (0, 6), 14),
        ('LEADING', (0, 6), (0, 6), 14),
        ('FONTNAME', (0, 8), (0, 8), 'SimSunBd'),
        ('FONTSIZE', (0, 8), (0, 8), 14),
        ('LEADING', (0, 8), (0, 8), 14),

        # 对齐设置
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        # ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        # 单元格框线
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
    ]
    component_table = Table(base, style=style, colWidths=[550])      # , rowHeights=[75, 75, 75, 75, 75, 75, 75]
    return component_table


def generate_pdf(studentId, methods, name=None, profession=None, sumScore=None, conditionId=None, fractions=None, filePath="data/studentStatus.pdf"):
    data = list()
    pdf = SimpleDocTemplate(filePath, rightMargin=0, leftMargin=0, topMargin=20, bottomMargin=0)
    if methods == "录取":
        pdf.pagesize = (7 * inch, 7.7 * inch)
        table = table_model(studentId, name, profession, sumScore, conditionId, fractions)
        data.append(table)
    else:
        info = linkData().person(studentId)[0]
        data.append(Paragraph("公务员考试", Title))
        data.append(Paragraph("准考证", Title))
        admits = admit(studentId, info["name"], info["sex"], info["profession"], info["number"], info["province"],
                       info["numberP"])
        data.append(admits)
        pdf.pagesize = (8.5 * inch, 9.4 * inch)
    try:
        pdf.multiBuild(data)
    except FileNotFoundError:
        os.mkdir("data")
        pdf.multiBuild(data)


if __name__ == "__main__":
    generate_pdf(22178222947, methods="准考证")
