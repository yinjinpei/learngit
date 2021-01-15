# coding:utf-8
# author:YJ沛

def test():
    import json
    info = [{'a':'1','b':'2','c':'3','d':'4','f':'5'}]
    data = json.dumps(info, sort_keys=True, indent=4)
    print(data)


test()