# coding:utf-8
# author:YJ沛



P = input()

for i in range(0, len(P)):
    if P[i] == "":
        print("", end="")
    elif P[i] in ["x", "y", "z"]:
        print(chr(ord(P[i]) - 23), end="")
