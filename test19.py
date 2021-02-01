

class Solution():
    def maxArea(self,height):
        if isinstance(height, list):
            c_list = []
            for i in range(len(height)):
                for k in range(len(height)):
                    try:
                        c=height[i]*height[k]
                        c_list.append(c)
                    except TypeError:
                        return TypeError
            return c_list
        else:
            return TypeError

a=[1,8,6,2,5,4,8,3,7]
soult = Solution()
print(soult.maxArea(a))





# class Solution():
#     def maxArea(self,height):
#         if isinstance(height, list):
#             c_max = 0
#             for i in range(len(height)):
#                 for k in range(len(height)):
#                     try:
#                         c=height[i]*height[k]
#                         if i == 0 and k==0:
#                             c_max = c
#                         else:
#                             if c > c_max:
#                                 c_max = c
#
#                     except TypeError:
#                         return TypeError
#             return c_max
#         else:
#             return TypeError
#
# a=[1,8,6,2,5,4,8,3,7]
# soult = Solution()
# print(soult.maxArea(a))