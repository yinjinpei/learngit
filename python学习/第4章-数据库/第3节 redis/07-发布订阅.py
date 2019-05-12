# coding:utf-8
# author:YJ沛



'''
官网手册：http://redis.cn/commands.html

发布订阅
    发布者不是计划发送消息给特定的接收者（订阅者），而是发布的消息分到不同的频道，不需要知道什么样的订阅者订阅
    订阅者对一个或多个频道感兴趣，只需接收感兴趣的消息，不需要知道什么样的发布者发布的
    发布者和订阅者的解耦合可以带来更大的扩展性和更加动态的网络拓扑
    客户端发到频道的消息，将会被推送到所有订阅此频道的客户端
    客户端不需要主动去获取消息，只需要订阅频道，这个频道的内容就会被推送过来

消息的格式
    推送消息的格式包含三部分
    part1:消息类型，包含三种类型
        subscribe，表示订阅成功
        unsubscribe，表示取消订阅成功
        message，表示其它终端发布消息
    如果第一部分的值为subscribe，则第二部分是频道，第三部分是现在订阅的频道的数量
    如果第一部分的值为unsubscribe，则第二部分是频道，第三部分是现在订阅的频道的数量，如果为0则表示当前没有订阅任何频道，当在Pub/Sub以外状态，客户端可以发出任何redis命令
    如果第一部分的值为message，则第二部分是来源频道的名称，第三部分是消息的内容
命令
    订阅
    SUBSCRIBE 频道名称 [频道名称 ...]

    取消订阅
    如果不写参数，表示取消所有订阅
    UNSUBSCRIBE 频道名称 [频道名称 ...]

    发布
    PUBLISH 频道 消息


'''

