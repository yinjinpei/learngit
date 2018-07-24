
a=[1,23,4,25,34,56,47,567,23,3,464,523,]
b=["v","cv","a","b"]
##########　列表从小到大排列 #########
a.sort()
b.sort()
print(a)
print(b)

##########　列表从大到小排列 #########
a.sort(reverse=True)
b.sort(reverse=True)
print(a)
print(b)

########  列表嵌套字典排列 ##########
a=[{"name":"peter","age":18},{"name":"alex","age":26},{"name":"xiaoming","age":20}]
a.sort(key=lambda x:x["name"])     #以"name"从小到大排序
print(a)

a.sort(reverse=True,key=lambda a:a["age"])  #以"age“ 从大到小排序
print(a)