

import  pandas  as pd
import numpy as np
from pandas import DataFrame



#写
dic1 = {'标题列1': ['张三','李四'],
        '标题列2': [80, 90]
       }

dic2 = {'标题列1': ['老五','老六'],
        '标题列2': [18, 20]
       }

df1 = pd.DataFrame(dic1)
df2 = pd.DataFrame(dic2)

writer = pd.ExcelWriter('1.xlsx')
df1.to_excel(writer, index=False,sheet_name="abc")
df2.to_excel(writer, index=False,sheet_name="def")

writer.close()
