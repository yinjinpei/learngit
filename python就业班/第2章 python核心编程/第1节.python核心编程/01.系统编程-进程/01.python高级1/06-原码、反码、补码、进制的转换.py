'''

两个字节用二进制表示：
十进制数字1 : 0000 0000 0000 0001
十进制数字2 : 0000 0000 0000 0010

负数表示：第一个位置（符号位）为0时表示正数，为1时表示负数
十进制数字-1 : 1000 0000 0000 0001
十进制数字-2 : 1000 0000 0000 0010


############## 原码，反码，补码 ##############

正数：原码 = 反码 = 补码
负数：反码 = 符号位不变，其它位取反
     补码 = 反码+1

例子：
-1原码：1000 0000 0000 0001
-1反码：1111 1111 1111 1110
-1补码：1111 1111 1111 1111

############## 正负数相加运算： ###############
规则：正数原码+负数补码

例子：1+(-1)
-1:    0000 0000 0000 0001
1 :    1111 1111 1111 1111
结果:  0000 0000 0000 0000

############## 负数补码转换原码 ###############
规则：原码 = 补码的符号位不变 --> 数据位取反  --> 尾+1

例子：-1
-1的补码:1111 1111 1111 1111
取反：   1000 0000 0000 0000
1-的原码:1000 0000 0000 0001

'''