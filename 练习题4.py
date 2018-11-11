
# author:YJ沛



s = '''
<div>

    <p>岗位职贵：</p>
<p>完成推荐*法、数据统计、接口.后台等服务器端相关工作</p> 
<p><br></p>
<p>必备要求：</p>
<p>良好的自我驱动力和职业素界，工作积极主动、结果导向</p>
<p>&nbs p;<b r></p>
<p>技术要求：</p>
<P>1、一年以上Python幵发经验，掌握面向对象分析和设计，了解设计模式 
<p>2、掌握HTTP协议，熟悉MVC、MWM等概念以及泪关WEB开发框架</p> 
<p>3、箪握关系数据庳幵发设计，箪握SQL,熟练使用MySQL/PostgreSQL 
<p>4、莩握NoSOL、MQ,熟练使用对应技术解决方案</p>
<p>5、熟悉 Javascript/CSS/HTML5, JQuery、React、Vue. js</p> 
<p>&nbsp;<br></p>
<p>加分项：</p>
<p>大数据，数理统计，机器学习，sklearn,高性能，大并发。</p>
    
    
    </div>
'''


import xlrd
workbook = xlrd.open_workbook('D:\work\demo.xlsx') #打开excel数据表
SheetList = workbook.sheet_names()#读取电子表到列表
SheetName = SheetList[0]#读取第一个电子表的名称
#Sheet1 = workbook.sheet_by_index(0) #电子表索引从0开始
Sheet2 = workbook.sheet_by_name(SheetList[1]) #实例化电子表对象
print(Sheet2)


print(Sheet2.nrows) # 行数
print(Sheet2.ncols) # 列数
print(Sheet2.row_values)


m=0
f=0

for i in range(1,Sheet2.nrows):

     rows = Sheet2.row_values(i)    # 读取整个表

     # print(rows)
     print(rows[1])
     m +=rows[1]

print("总数：",m)



#
#
# import plotly.offline as pltoff
# import plotly.graph_objs as go
#
# def pie_charts(name='pie_chart.html'):
#     dataset = {
#         'labels':['Windows', 'Linux', 'MacOS'],
#         'values':[280, 100, 30]}
#     data_g = []
#     tr_p = go.Pie(
#     labels = dataset['labels'],
#     values = dataset['values']
#
#     )
#     data_g.append(tr_p)
#     layout = go.Layout(title="pie charts")
#     fig = go.Figure(data=data_g, layout=layout)
#     pltoff.plot(fig, filename=name)
#
# if __name__=='__main__':
#     pie_charts()

class A(object):
     def __init__(self,name,age):
          pass