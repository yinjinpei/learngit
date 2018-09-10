########## 流程程 ############
'''
1,在包的同级目录下创建 setup.py 文件
2,内容为：
from distutils.core import setup
setup(name="peter", version="1.0", description="peter's module", author="peter", py_modules=['moduleDir.sendmsg', 'moduleDir.recvmsg'])

3，构建模块：linux下进行
python3 setup.py build
python3 setup.py sdist  #此时会生成一个包：peter-1.0.tar.gz

4，安装模块包：linux下进行
python3 setup.py install

'''