
#情况一：
#from moduleDir import sendmsg   #如果__init__.py内容为空时，不支持from moduleDir import *
#sendmsg.sendmsg_print()

#情况二：
#from moduleDir import *  #此时__init__.py里有__all__
#sendmsg.sendmsg_print()


#情况三
import moduleDir
moduleDir.sendmsg.sendmsg_print()

moduleDir.recvmsg.recvmsg_print()