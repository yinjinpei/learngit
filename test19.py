import random
import string


class Solution():
    def maxArea(self, height):
        if isinstance(height, list):
            c_max = 0
            for i in range(len(height)):
                for k in range(i + 1, len(height)):
                    try:
                        if height[i] >= height[k]:
                            c = height[k] * (k - i)
                        else:
                            c = height[i] * (k - i)
                        if c > c_max:
                            c_max = c
                    except TypeError:
                        return TypeError
            return c_max
        else:
            return TypeError

a = []
n = random.randint(0,100)
for i in list(random.SystemRandom().choice(string.digits) for _ in range(n)):
    a.append(int(i))

print('a大小：',len(a))
print(a)

# a=[1,8,6,2,5,4,8,3,7]
# a=[1,2,1]
# a=[1,1]
# a=[4,3,2,1,4]
a=[4,1,1,4]
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


# class Solution():
#     def maxArea(self,height):
#         if isinstance(height, list):
#             c_list = []
#             for i in range(len(height)):
#                 for k in range(i+1,len(height)):
#                     try:
#                         if height[i] >= height[k]:
#                             c = height[k] * (k - i)
#                         else:
#                             c = height[i] * (k - i)
#                         c_list.append(c)
#                     except TypeError:
#                         return TypeError
#             return c_list
#         else:
#             return TypeError
#
# a=[1,8,6,2,5,4,8,3,7]
# # a=[1,2,1]
# soult = Solution()
# print(soult.maxArea(a))
