# coding:utf-8
# author:YJ沛


def quick_sort(alist, first, last):
    '''快速排序'''

    if first >= last:
        return

    mid_value = alist[first]
    low = first
    high = last

    while low < high:
        # low    向左移
        # hight  向右移
        while low < high and alist[high] >= mid_value:
            high -= 1
        alist[low] = alist[high]

        while low < high and alist[low] < mid_value:
            low += 1
        alist[high] = alist[low]

    # 从循环体退出，low == high
    alist[low] = mid_value

    # 对low左边的列表执行快速排序
    quick_sort(alist, first, low - 1)

    # 对low右边的列表执行快速排序
    quick_sort(alist, low + 1, last)


if __name__ == "__main__":
    a = [1, 3, 4, 6, 7, 23, 45, 67, 33, 2, 6, 7, 8, 98, 56, 1, 2]
    print(a)
    quick_sort(a, 0, len(a) - 1)
    print(a)
