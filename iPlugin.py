#! usr/bin/env python3

class Plugin(object):
    #定义插件接口，所有插件必须实现该接口
    name = ''
    description = ''
    version = ''

    def __init__(self):
        pass

    def getResult(self,jsonData):
        pass

    def executeFun(self):
        pass