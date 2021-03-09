

#pandas有两个主要数据结构：Series和DataFrame。


import numpy as np
import pandas as pd


# Series的创建
# pd.Series(list,index=[ ])，第二个参数是Series中数据的索引，可以省略。

# arr1 = [i for i in range(10)]
arr1 = np.arange(10)    # 生成数组
print(arr1)

s1 = pd.Series(arr1)
print(s1)

print('---------------------------------------------')

# DataFrame的创建
# pd.DataFrame(data,columns = [ ],index = [ ])：columns和index为指定的列、行索引，并按照顺序排列。

data = {'姓名': ['张三', '李四', '老五', '老六', '八哥', '九尾'],
        '性别': ['男', '女', '男', '女', '男', '女'],
        '年龄': [19, 16, 23, 22, 30, 102]}

df= pd.DataFrame(data)
print(df)

print('---------------------------------------------')


df2 = pd.DataFrame(data, columns=['姓名','别名','性别','年龄'], index=['第一行','第二行','第三行','第四行','第五行','第六行'])
print(df2)

# 另一种常见的创建DataFrame方式是使用嵌套字典，如果嵌套字典传给DataFrame，pandas就会被解释为外层字典的键作为列，内层字典键则作为行索引：
print('---------------------------------------------')

pop = {'姓名':{'第一行':'张三','第二行':'李四','第三行':'老五'},
       '性别':{'第一行':'男','第二行':'女','第三行':'男'},
       '年龄':{'第一行':'19','第二行':'16','第三行':'23'}
       }
df3 = pd.DataFrame(pop)
print(df3)