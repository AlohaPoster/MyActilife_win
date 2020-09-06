
# import os
# import docx



# def getdoc(docpath):
#     report = docx.Document()
#     report.add_heading('CPAT运动记录仪数据报告',level = 0)

#     report.add_heading('1. 个人信息',level = 1)
#     table = report.add_table(rows=5,cols=2)
#     table.cell(0,0).text = "使用者姓名"
#     table.cell(0,1).text = "zhangrl"
#     table.cell(1,0).text = "使用者编号"
#     table.cell(1,1).text = "12"
#     table.cell(2,0).text = "使用设备编号"
#     table.cell(2,1).text = "24"
#     table.cell(3,0).text = "数据传输日期"
#     table.cell(3,1).text = "2020-03-05"
#     table.cell(4,0).text = "数据是否上传到云"
#     table.cell(4,1).text = "yes"

#     report.add_heading('2. 数据概况',level = 1)

#     report.add_heading('3. 原始数据图表',level = 1)

#     report.add_heading('4. 数据处理分析结果',level = 1)

#     p = report.add_paragraph('This is paragraph')
#     p.add_run('bold').bold = True
#     p.add_run(' and some ')
#     p.add_run('italic.').italic = True
#     report.add_paragraph('first item in unordered list', style='List Bullet')
#     report.add_paragraph('first item in ordered list', style='List Number')
#     report.add_paragraph('Intese quote',style="Intense Quote")
#     report.add_picture(r"/Users/zhangruilin/Desktop/test.png",Inches(2.25))

#     report.save(docpath)
#     return 

import data_pre
from keras import models
import numpy as np

def predictdata(info):
    x,ab_time,time = data_pre.getdata(info['csvpath'], info['csvfilename'])
    model = models.load_model('./resources/predictmodel.h5')  
    y_p = model.predict_classes(x,verbose = 0)
    return y_p,ab_time,time

if __name__ == "__main__":
    info = {
        "csvpath" : "/Users/zhangruilin/Desktop/",
        "csvfilename" : "test1"
    }
    y_p, at, t = predictdata(info)
    print(y_p)
    print(at)
