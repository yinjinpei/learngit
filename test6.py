# -*- coding:utf-8 -*-
import win32com.client as win32
import warnings
import sys

reload(sys)
sys.setdefaultencoding('utf8')
warnings.filterwarnings('ignore')

import requests

from pyecharts import Bar

str = ["中国","美国","日本","意大利","英国","韩国"]

value1 = [1123,241,312,453,511,633]


value2 = [1000,200,300,400,500,600]

bar = Bar("各国数据顶尖人才统计")
bar.add("百度统计", str, value1, is_stack=True)
bar.add("谷歌统计", str, value2, is_stack=True)
bar.render()

#
#·   ····
# def main():
#     bar = Bar("我的第一个图表", "这里是副标题")
#     bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])
#     # bar.print_echarts_options() # 该行只为了打印配置项，方便调试时使用
#     bar.render()  # 生成本地 HTML 文件/
#
#
# if __name__ == "__main__":
#     main()

