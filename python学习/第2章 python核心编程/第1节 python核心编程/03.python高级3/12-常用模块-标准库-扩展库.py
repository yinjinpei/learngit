#-*- coding:utf-8 -*-
#author:YJ沛

'''
常用标准库：
builtins	内建函数默认加载
os	        操作系统接口
sys	Python  自身的运行环境
functools	常用的工具
json	    编码和解码 JSON 对象
logging	    记录日志，调试
threading	多线程
copy	    拷贝
time	    时间
datetime	日期和时间
calendar	日历
hashlib	    加密算法
random	    生成随机数
re	        字符串正则匹配
socket	    标准的 BSD Sockets API
shutil	    文件和目录管理
glob	    基于文件通配符搜索
multiprocessing	    多进程


常用扩展库：
requests	    使用的是 urllib3，继承了urllib2的所有特性
urllib	        基于http的高层库
scrapy  	    爬虫
beautifulsoup4	HTML/XML的解析器
celery	        分布式任务调度模块
redis	        缓存
Pillow(PIL) 	图像处理
xlsxwriter	    仅写excle功能,支持xlsx
xlwt	        仅写excle功能,支持xls ,2013或更早版office
xlrd	        仅读excle功能
elasticsearch	全文搜索引擎
pymysql	        数据库连接库
matplotlib	    画图
numpy/scipy	    科学计算
xmltodict	    xml 转 dict
gevent	        基于协程的Python网络库
fabric	        系统管理
pandas	        数据处理库
scikit-learn	机器学习库
SimpleHTTPServer	    简单地HTTP Server,不使用Web框架
mongoengine/pymongo	    mongodbpython接口
django/tornado/flask	web框架
'''


#hashlib    哈希，算法,加密
import hashlib

m = hashlib.md5()   #生成一个哈希对象
m.update(b'yinjinpei')  #把明文'yinjinpei'进行Md5加密
print(m.hexdigest())    #返回十六进制数字字符串（16个字节，32个字母）
print(len(m.hexdigest()))

'''
就可以运行起来静态服务。平时用它预览和下载文件太方便了。

在终端中输入命令：

python2中

    python -m SimpleHTTPServer PORT
python3中

    python -m http.server PORT
'''