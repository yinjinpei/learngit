from urllib import request

import xlwt as xlwt
from bs4 import BeautifulSoup
import ssl
import os
import urllib.request
import time


dict_name = {}

# 新建文件夹
curPath = os.getcwd()
tempPath = 'douban'
targetPath = curPath + os.path.sep + tempPath
# if not os.path.exists(targetPath):
#     os.makedirs(targetPath)
# else:
#     print("路径已经存在")


# get_img函数是取数据的
def get_img(url):
    response = request.urlopen(url)
    page = response.read()
    html_doc = page.decode('utf-8')
    soup = BeautifulSoup(html_doc, "html5lib")

    # 取出标题
    div = soup.find('div', id='content')
    for title in div.find_all('h1'):
        # print(title)
        # print(title.text)
        s = title.text
        # 去掉空格
        global xlsName
        xlsName = s.replace(' ', '')
        print(xlsName)

    # 创建一个工作簿并设置编码
    global workbook
    workbook = xlwt.Workbook(encoding='utf-8')

    # 创建一个工作表并命名
    global worksheet
    worksheet = workbook.add_sheet(xlsName)

    # #保存工作簿
    # workbook.save(tempPath+'/'+xlsName+'.xls')

    ol = soup.find('ol', class_='grid_view')
    for name in ol.find_all('li'):
        n2 = name.find("div", attrs={"class": "pic"})

        movieNumber = n2.find("em", attrs={"class": ""})

        print(movieNumber.string)
        n4 = n2.find('a').get('href')
        # 网络上图片的地址
        n5 = n2.find('img').get('src')
        movieName = n2.find('img').get('alt')
        print(movieName)
        print('-------------------------')
        img_path = tempPath + "/" + movieNumber.string + ".jpg"
        # 将远程数据下载到本地，第二个参数就是要保存到本地的文件名
        # request.urlretrieve(n5, img_path)

        # 保存电影名，和存放在表中的列的值
        dict_name[int(movieNumber.string)] = [movieName,"导演名"]
        # worksheet.write(int(movieNumber.string), 0, label=movieName)

        # for test
        # if 20 == int(movieNumber.string):
        #     break

        # for i in range(int(movieNumber.string)):
        #     #写入Excel，注意三个参数分别对应工作表的行、列、值
        #     print('i的值 ：',i)
        #     worksheet.write(i, i, label=movieName)
        #     workbook.save('Excel_Workbook.xls')


# 方法1
# https://movie.douban.com/top250?start=0&filter=
list_url = []
for i in range(2):
    list_url.append("https://movie.douban.com/top250?start=" +
                    str(i * 25) + "&filter=")
    get_img(list_url[i])
    print("当页网址" + list_url[i])
    print("第" + str(i + 1) + "页完成")

# 写到表中
for key in dict_name:
    # 放在电影名
    worksheet.write(key - 1, 0, label=str(dict_name[key][0]))
    # 放在导演名
    worksheet.write(key - 1, 1, label=str(dict_name[key][1]))

# workbook.save(tempPath + '/' + xlsName + '.xls')
workbook.save('电影.xls')

# 方法2
'''
for i in range(10):
    url=['https://movie.douban.com/top250?start={}&filter='.format(i) for i in range(0,226,25)]
    get_img(url[i])
'''
