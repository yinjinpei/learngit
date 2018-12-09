# coding:utf-8
# author:YJ沛


# 二分查找 (查找的对象是有有序的列表)
def binary_search(alist, item):
    n = len(alist)
    mid = n//2

    if n > 0:
        if alist[mid] == item:
            return True
        # alist[:mid]
        elif alist[mid] > item:
            return binary_search(alist[:mid], item)
        # alist[mid:]
        elif alist[mid] < item:
            return binary_search(alist[mid+1:], item)
    return False


a_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(a_list)


find = binary_search(a_list, item=5)
print(find)
