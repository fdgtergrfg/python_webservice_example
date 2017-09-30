# !/usr/bin/python
# -*- coding: utf-8 -*-

import soaplib
from soaplib.core.service import rpc, DefinitionBase, soap
from soaplib.core.model.primitive import String, Integer
from soaplib.core.server import wsgi
from soaplib.core.model.clazz import Array
import time
import hashlib
import xmltodict,json
import os
import urlparse

# 根据文本内容和当前时间生成唯一的MD5,用于生成临时文件
def generateMD5(code):
    now = time.time()
    m = hashlib.md5()
    m.update(str(now) + code)
    return m.hexdigest() # 生成唯一的MD5码


# 返回临时创建的文件名
def createTmpFile(code):
    try:
        md5_string = generateMD5(code)
        filePath = md5_string
        outFile = open(filePath,"w")
        outFile.write(code)
        outFile.close()
        return filePath
    except Exception,e:
        print e


class HelloWorldService(DefinitionBase):
    @soap(String,_returns=String)
    def say_hello(self,code):
        code = dict(urlparse.parse_qsl(code)) # 因为传入的时候会对字符串编码,所以服务端需要解码
        # 下面根据code创建临时文件
        file_path = createTmpFile(code["code"])
        # 下面执行你们的代码分析操作(这里用一个简单的赋值语句代替了)
        result = "test.xml" # 生成的xml文件
        # 下面是将xml文件转换为json文件的代码
        result_xml = open(result, 'r').read() # 读取xml文件内容
        result_tmp = xmltodict.parse(result_xml)
        json_result = json.dumps(result_tmp)
        # 删除临时创建的文件
        os.remove(file_path)
        return str(json_result)

if __name__=='__main__':

    try:
        from wsgiref.simple_server import make_server
        soap_application = soaplib.core.Application([HelloWorldService], 'tns', 'webservice')
        wsgi_application = wsgi.Application(soap_application)

        server = make_server('localhost', 7789, wsgi_application)
        server.serve_forever()

    except ImportError:
        print "Error: example server code requires Python >= 2.5"