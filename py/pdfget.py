# -*- coding: utf-8 -*-  

import predict
from reportlab.pdfgen.canvas import Canvas  
from reportlab.pdfbase import pdfmetrics  
from reportlab.pdfbase.cidfonts import UnicodeCIDFont  
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
from reportlab.pdfbase.ttfonts import TTFont 
pdfmetrics.registerFont(TTFont('msyh', 'SimSun.ttf'))  
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,TableStyle
from reportlab.platypus import SimpleDocTemplate
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.colors import HexColor

def second2time(second):
    hours = int(second/3600)
    mins = int((second - hours*3600)/60)
    second = int(second - 60*mins -3600*hours)
    return hours,mins,second

def time2second(hours,mins,second):
    return (hours*3600+mins*60+second)

def autoLegender( chart,title=''):
    width = 448
    height = 230
    d = Drawing(width,height)
    lab = Label()
    lab.x = 220  #x和y是文字的位置坐标
    lab.y = 210
    lab.setText(title)
    lab.fontName = 'msyh' #增加对中文字体的支持
    lab.fontSize = 20
    d.add(lab)
    d.background = Rect(0,0,width,height,strokeWidth=1.5,strokeColor="#000000",fillColor=None) #边框颜色
    d.add(chart)

    return d


def draw_pie(data=[], labels=[], use_colors=[], width=360,):
    '''更多属性请查询reportlab.graphics.charts.piecharts.WedgeProperties'''

    pie = Pie()
    pie.x = 40 
    pie.y = 20
    pie.slices.label_boxStrokeColor = colors.white  

    pie.data = data      # 饼图上的数据
    pie.labels = labels  # 数据的标签
    pie.simpleLabels = 0 # 0 标签在标注线的右侧；1 在线上边
    pie.sameRadii = 1    # 0 饼图是椭圆；1 饼图是圆形

    pie.slices.strokeColor = colors.blue       # 圆饼的边界颜色
    pie.strokeWidth=1                         # 圆饼周围空白区域的宽度
    pie.strokeColor= colors.white             # 整体饼图边界的颜色
    pie.slices.label_pointer_piePad = 10       # 圆饼和标签的距离
    pie.slices.label_pointer_edgePad = 25    # 标签和外边框的距离
    pie.width = width
    pie.direction = 'clockwise'
    pie.pointerLabelMode  = 'LeftRight'

    for i in range(len(labels)):
        pie.slices[i].fontName = 'msyh' #设置中文
    for i, col in enumerate(use_colors):
        pie.slices[i].fillColor  = col
    return pie


def rpt(info):
    y_p, abs_time, time = predict.predictdata(info)
    story = []
    stylesheet = getSampleStyleSheet()

    titileStyle = stylesheet['Normal']
    titileStyle.wordWrap = 'CJK'
    titileStyle.leading = 25
    
    normalStyle = stylesheet['Normal']
    normalStyle.wordWrap = 'CJK'
    normalStyle.leading = 21
    normalStyle.firstLineIndent = 32
    normalStyle.fontSize = 14
    normalStyle.alignment = 0

    rpt_title = '<para autoLeading="off" fontSize=24 align=center><b><font face="msyh">CPAT数据导出报告</font></b><br/><br/><br/></para>' 
    story.append(Paragraph(rpt_title,titileStyle)) 

    text = '<para autoLeading="off" fontSize=18><br/><br/><br/><b><font face="msyh">- 用户基本信息：</font></b><br/><br/></para>'
    story.append(Paragraph(text,titileStyle))

    text = '<font face="msyh" color=grey>用户姓名： %s</font><br/>' % info['username']
    story.append(Paragraph(text,normalStyle))
    text = '<font face="msyh" color=grey>数据导出日期： %s</font><br/>' % info['date']
    story.append(Paragraph(text,normalStyle))
    text = '<font face="msyh" color=grey>是否存储到MyActilifeCloud： %s</font><br/>' % info['ifupload']
    story.append(Paragraph(text,normalStyle))

    text = '<para autoLeading="off" fontSize=18><br/><br/><br/><b><font face="msyh">- 数据概况：</font></b><br/><br/></para>'
    story.append(Paragraph(text,titileStyle))

    with open(info['csvpath'] + info['csvfilename'] + ".txt", "r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            if "测试持续时间" in line:
                temp = line.split(" ")
                hours = int(temp[1])
                mins = int(temp[3])
                seconds = int(temp[5])
            text = '<font face="msyh" color=grey>%s</font><br/>' % line
            story.append(Paragraph(text,normalStyle))
            

    text = '<para autoLeading="off" fontSize=18><br/><br/><br/><b><font face="msyh">- 原始数据图表：</font></b><br/><br/></para>'
    story.append(Paragraph(text,titileStyle))

    hei = 300
    wid = 600
    img = Image(info['csvpath'] + info['csvfilename'] + "_" + "X-axis"+'.png')
    img.drawHeight = hei
    img.drawWidth = wid
    story.append(img)

    img = Image(info['csvpath'] + info['csvfilename'] + "_" + "Y-axis"+'.png')
    img.drawHeight = hei
    img.drawWidth = wid
    story.append(img)

    img = Image(info['csvpath'] + info['csvfilename'] + "_" + "Z-axis"+'.png')
    img.drawHeight = hei
    img.drawWidth = wid
    story.append(img)

    img = Image(info['csvpath'] + info['csvfilename'] + "_" + "combined"+'.png')
    img.drawHeight = hei
    img.drawWidth = wid
    story.append(img)

    text = '<para autoLeading="off" fontSize=18><br/><br/><br/><b><font face="msyh">- 数据分析结果：</font></b><br/><br/></para>'
    story.append(Paragraph(text,titileStyle))

    print(y_p)
    alltime = time2second(hours,mins,seconds)
    text = '<font face="msyh" color=grey>总记录时间：%d 小时 %d 分钟 %d 秒</font><br/>' % (hours,mins,seconds)
    story.append(Paragraph(text,normalStyle))

    p0 = sum(l==0 for l in y_p)*100/len(y_p)
    p1 = sum(l==1 for l in y_p)*100/len(y_p)
    p2 = sum(l==2 for l in y_p)*100/len(y_p)

    hours, mins, seconds = second2time(alltime*p0/100)
    text = '<font face="msyh" color=grey>轻度运动时间时间：%d 小时 %d 分钟 %d 秒</font><br/>' % (hours,mins,seconds)
    story.append(Paragraph(text,normalStyle))

    hours, mins, seconds = second2time(alltime*p1/100)
    text = '<font face="msyh" color=grey>中度运动时间时间：%d 小时 %d 分钟 %d 秒</font><br/>' % (hours,mins,seconds)
    story.append(Paragraph(text,normalStyle))

    hours, mins, seconds = second2time(alltime*p2/100)
    text = '<font face="msyh" color=grey>剧烈运动时间时间：%d 小时 %d 分钟 %d 秒</font><br/>' % (hours,mins,seconds)
    story.append(Paragraph(text,normalStyle))

    t0 = "轻度运动时间 %.2f%%" % p0
    t1 = "中等运动时间 %.2f%%" % p1
    t2 = "剧烈运动时间 %.2f%%" % p2
    data = [p0,p1,p2]
    labs = [t0,t1,t2]
    colorss = [HexColor("#D8BFD8"),HexColor("#778899"),HexColor("#483D8B")]
    z = autoLegender(draw_pie(data,labs,colorss),"各运动强度分布比例图")
    story.append(z)

    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.ticker as ticker
    fig = plt.figure(figsize=(25, 12))
    ax = fig.add_subplot(111)

    y_p = [l+1 for l in y_p]
    ax.plot(abs_time, y_p)
    # ax.set_xticks(xtick)
    ax.grid()
    ax.set_yticks([1,2,3])
    ax.xaxis.set_major_locator(ticker.MultipleLocator(24))
    ax.set_xticklabels(abs_time, rotation=30)
    ax.set_yticklabels(['L','M','V'])
    ax.set_xlabel("abs_time")
    ax.set_ylabel("PA")
    fig.savefig(info['csvpath'] + "detail")

    img = Image(info['csvpath'] + "detail"+'.png')
    img.drawHeight = 400
    img.drawWidth = 600
    story.append(img)

    # lp = LinePlot()
    # lp.height = 150
    # lp.width = 300
    # da = []
    # for i in range(0,len(y_p)):
    #     da.append((i,y_p[i]))
    # lp.data = [da]
    # lp.lines[0].strokeColor = colors.blue
    
    # d = Drawing(448,230)
    # lab = Label()
    # lab.x = 220  
    # lab.y = 210
    # lab.setText('具体运动情况折线图')
    # lab.fontName = 'msyh' 
    # lab.fontSize = 20
    # d.add(lab)
    # d.background = Rect(0,0,448,230,strokeWidth=1.5,strokeColor="#000000",fillColor=None) #边框颜色
    # d.add(lp)
    # story.append(d)

    report = SimpleDocTemplate(info['csvpath'] + info['csvfilename'] + '.pdf')
    report.multiBuild(story)
    return "1"

if __name__ == "__main__":
    info = {
        "csvfilename": 'test2',
        "csvpath": '/Users/zhangruilin/Desktop/test/',
        'username': 'zhangrl',
        'userid': '23',
        'deviceid': '24',
        'ospassword': '102495',
        'ifupload': 'on',
        'date': '2020/3/17'
    }
    rpt(info)
    import time
    time.sleep(10)
   
    