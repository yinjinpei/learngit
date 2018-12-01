# coding:utf-8
# author:YJ沛


'''
插入排序法稳定性： 稳定

最优时间复杂度：O(nlogn)
最坏时间复杂度：O(nlogn)

生成一个新的列表，需要消耗空间
'''


def merge_sort(alist):
    '''归并排序'''

    n = len(alist)
    if n <= 1:
        return alist
    mid = n // 2

    # left 采用归并排序后形成的新的列表
    left_list = merge_sort(alist[:mid])

    # right 采用归并排序后形成的新的列表
    right_list = merge_sort(alist[mid:])

    # 左边的指针，右边的指针
    left_pointer, right_pointer = 0, 0
    result = []

    while left_pointer < len(left_list) and right_pointer < len(right_list):
        if left_list[left_pointer] <= right_list[right_pointer]:
            result.append(left_list[left_pointer])
            left_pointer += 1
        else:
            result.append(right_list[right_pointer])
            right_pointer += 1

    # 将有序的子列表合并成一个列表
    result += left_list[left_pointer:]
    result += right_list[right_pointer:]

    return result


if __name__ == "__main__":
    a = [1, 3, 4, 6, 7, 23, 45, 67, 33, 2, 6, 7, 8, 98, 56, 1, 2]
    print(a)
    b = merge_sort(a)
    print(a)
    print(b)

