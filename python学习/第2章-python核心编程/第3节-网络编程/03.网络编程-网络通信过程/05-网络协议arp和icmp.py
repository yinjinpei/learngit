#-*- coding:utf-8 -*-
#author:YJ沛


'''
1，arp 用来广播，通过IP获取网卡mac地址
2，icmp 用来ping   ping时要先获取mac
3，rarp 用来广播，通过MAC获取IP

判断是两个IP是否在同一网段方法：把IP与其子网掩码 按位与 得到的结果是否相同，相同则是同一网段

电脑命令：
arp -a  获取缓存中的ip和MAC列表
arp -d  清除缓存中的ip和MAC列表

MAC地址，在两个设备之间通信时在变化
而IP地址，在整个通信过程中不会发生任何变化


访问一个网址过程：
1，先要解析出域名（如 baidu.com）对应的IP地址
    1，先知道默认网关的MAC
        1，使用ARP获取默认网关的MAC地址
    2，组织数据发送给默认网关（IP还是dns服务器的IP，但MAC地址是默认网关的MAC）
    3，默认网关拥有转发数据的能力，把数据转发给路由器
    4，路由根据自己的路由协议，选择最优路由进程转发数据
    5，目的网关（DNS服务器所在的网关），把数据转发给DNS服务器
    6，DNS服务器解析出域名对应的IP地址，并原路返回相应的数据给clinet
2，得到域名对应的IP地址之后，会发送TCP的3次握手，进行连接
3，使用http协议发送请求数据给web服务器
4，web服务器收到数据请求之后，通过查询自己的服务器得到的相应结果，原路还回给client浏览器
5，浏览器接收到数据后，通过浏览器自己的渲染功能来显示这个网页
6，浏览器关闭TCP连接，即4次挥手

完成整个访问过程


TCP 3次握手，4次挥手
    长连接，短连接


'''
