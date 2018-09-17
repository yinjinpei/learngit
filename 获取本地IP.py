import socket

# 方法一：
# 通常使用socket.gethostbyname()方法即可获取本机IP地址，但有时候获取不到(比如没有正确设置主机名称)，示例代码如下：

# 获取本机计算机名称
hostname = socket.gethostname()
# 获取本机ip
ip = socket.gethostbyname(hostname)
print(ip)


# 方法二：
# 亲测本方法在windows和Linux系统下均可正确获取IP地址
def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

if __name__ == '__main__':
    print(get_host_ip())