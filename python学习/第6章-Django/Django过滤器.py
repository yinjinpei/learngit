#-*- coding:utf-8 -*-
#author:YJ沛



'''
django1.4

html页面从数据库中读出DateTimeField字段时，显示的时间格式和数据库中存放的格式不一致，比如数据库字段内容为2012-08-26 16:00:00，但是页面显示的却是Aug. 26, 2012, 4 p.m.

为了页面和数据库中显示一致，需要在页面格式化时间，需要添加<td>{{ dayrecord.p_time|date:"Y-m-d H:i:s" }}</td> 类似的过滤器。刷新页面，即可正常显示。

过滤器相关：

一、形式：小写
{{ name | lower }}

二、串联：先转义文本到HTML，再转换每行到 <p> 标签
{{ my_text|escape|linebreaks }}

三、过滤器的参数
显示前30个字
{{ bio | truncatewords:"30" }}

格式化
{{ pub_date | date:"F j, Y" }}

过滤器列表
{{ 123|add:"5" }} 给value加上一个数值
{{ "AB'CD"|addslashes }} 单引号加上转义号，一般用于输出到javascript中
{{ "abcd"|capfirst }} 第一个字母大写
{{ "abcd"|center:"50" }} 输出指定长度的字符串，并把值对中
{{ "123spam456spam789"|cut:"spam" }} 查找删除指定字符串
{{ value|date:"F j, Y" }} 格式化日期
{{ value|default:"(N/A)" }} 值不存在，使用指定值
{{ value|default_if_none:"(N/A)" }} 值是None，使用指定值
{{ 列表变量|dictsort:"数字" }} 排序从小到大
{{ 列表变量|dictsortreversed:"数字" }} 排序从大到小
{% if 92|divisibleby:"2" %} 判断是否整除指定数字


{{ string|escape }} 转换为html实体
{{ 21984124|filesizeformat }} 以1024为基数，计算最大值，保留1位小数，增加可读性
{{ list|first }} 返回列表第一个元素
{{ "ik23hr&jqwh"|fix_ampersands }} &转为&amp;
{{ 13.414121241|floatformat }} 保留1位小数，可为负数，几种形式
{{ 13.414121241|floatformat:"2" }} 保留2位小数
{{ 23456 |get_digit:"1" }} 从个位数开始截取指定位置的1个数字


{{ list|join:", " }} 用指定分隔符连接列表
{{ list|length }} 返回列表个数
{% if 列表|length_is:"3" %} 列表个数是否指定数值
{{ "ABCD"|linebreaks }} 用新行用<p> 、 <br /> 标记包裹
{{ "ABCD"|linebreaksbr }} 用新行用<br /> 标记包裹
{{ 变量|linenumbers }} 为变量中每一行加上行号
{{ "abcd"|ljust:"50" }} 把字符串在指定宽度中对左，其它用空格填充


{{ "ABCD"|lower }} 小写
{% for i in "1abc1"|make_list %}ABCDE,{% endfor %} 把字符串或数字的字符个数作为一个列表
{{ "abcdefghijklmnopqrstuvwxyz"|phone2numeric }} 把字符转为可以对应的数字？？
{{ 列表或数字|pluralize }} 单词的复数形式，如列表字符串个数大于1，返回s，否则返回空串


{{ 列表或数字|pluralize:"es" }} 指定es
{{ 列表或数字|pluralize:"y,ies" }} 指定ies替换为y
{{ object|pprint }} 显示一个对象的值
{{ 列表|random }} 返回列表的随机一项
{{ string|removetags:"br p div" }} 删除字符串中指定html标记
{{ string|rjust:"50" }} 把字符串在指定宽度中对右，其它用空格填充


{{ 列表|slice:":2" }} 切片
{{ string|slugify }} 字符串中留下减号和下划线，其它符号删除，空格用减号替换
{{ 3|stringformat:"02i" }} 字符串格式，使用Python的字符串格式语法
{{ "E<A>A</A>B<C>C</C>D"|striptags }} 剥去[X]HTML语法标记
{{ 时间变量|time:"P" }} 日期的时间部分格式
{{ datetime|timesince }} 给定日期到现在过去了多少时间
{{ datetime|timesince:"other_datetime" }} 两日期间过去了多少时间


{{ datetime|timeuntil }} 给定日期到现在过去了多少时间，与上面的区别在于2日期的前后位置。
{{ datetime|timeuntil:"other_datetime" }} 两日期间过去了多少时间
{{ "abdsadf"|title }} 首字母大写
{{ "A B C D E F"|truncatewords:"3" }} 截取指定个数的单词
{{ "<a>1<a>1<a>1</a></a></a>22<a>1</a>"|truncatewords_html:"2" }} 截取指定个数的html标记，并补完整
<ul>{{ list|unordered_list }}</ul> 多重嵌套列表展现为html的无序列表


{{ string|upper }} 全部大写
<a href="{{ link|urlencode }}">linkage</a> url编码
{{ string|urlize }} 将URLs由纯文本变为可点击的链接。（没有实验成功）
{{ string|urlizetrunc:"30" }} 同上，多个截取字符数。（同样没有实验成功）


{{ "B C D E F"|wordcount }} 单词数
{{ "a b c d e f g h i j k"|wordwrap:"5" }} 每指定数量的字符就插入回车符
{{ boolean|yesno:"Yes,No,Perhaps" }} 对三种值的返回字符串，对应是 非空,空,None



日期格式化参数：

a 'a.m.' 或 'p.m.' (注意,它与PHP 的输出略有不同.它包括了句点(django扩展). 'a.m.'
A 'AM' 或 'PM'. 'AM'
B 未实现.
d 每月第几天, 带前导零 '01' to '31'
D 每周第几天,3字母的字符串. 'Fri'
f 时间, 12-小时制的小时和分钟数, 如果分钟数为零,则不显示.(django 扩展). '1', '1:30'
F 月份, 长文本格式. 'January'
g 小时, 12-小时制,没有前导零 '1' to '12'
G 小时, 24-小时制,没有前导零 '0' to '23'
h 小时, 12-小时制,有前导零 '01' to '12'
H 小时, 24-小时制,有前导零 '00' to '23'
i 分钟. '00' to '59'
I 未实现
j 每月第几天, 无前导零 '1' to '31'
l 每周第几天,长文本格式. 'Friday'
L 是否闰年. True or False
m 数字表示的月份,有前导零. '01' to '12'
M 月份,3字母短文本格式. 'Jan'
n 数字表示的月份,无前导零 '1' to '12'
N 出版风格的月份缩写(django 扩展) 'Jan.', 'Feb.', 'March', 'May'
O 与格林威治的时间差(以小时计) '+0200'
P 12小时制的小时分钟及'a.m.'/'p.m.' 分钟数若为零则不显示. 用字符串表示特殊 的时间点, 如 'midnight' 和 'noon' (django扩展) '1 a.m.', '1:30 p.m.', 'midnight','noon', '12:30 p.m.'
r RFC 822 格式的日期 . 'Thu, 21 Dec 2000 16:01:07+0200'
s 秒数, 带有前导零的数字表示 '00' to '59'
S 英语序数后缀,用于一个月的第几天,2个字符 'st', 'nd', 'rd' or 'th'
t 给定月共有多少天. 28 to 31
T 本机时区. 'EST', 'MDT'
U 未实现
w 一周中的第几天,没有前导零的数字 '0' (Sunday) to '6' (Saturday)
W ISO-8601 一年的第多少星期数, 一周从 星期一开始 1, 23
y Year, 2 位数字表示 '99'
Y Year, 4 位数字表示 '1999'
z 一年中的第几天 . 0 to 365
Z 以秒计的时区偏移量. 这个偏移量对UTC西部 时区总是负数,而对UTC东部时区则总是正数 -43200 to 43200



'''