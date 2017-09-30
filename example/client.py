# !/usr/bin/python
# -*- coding: utf-8 -*-

from suds.client import Client
# import logging
import MySQLdb
import urllib

if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    # logging.getLogger('suds.client').setLevel(logging.DEBUG)

    hello_client = Client('http://localhost:7789/?wsdl', cache=None)

    conn = MySQLdb.connect(host="localhost",user="root",passwd="111111",db="CodePedia_test")
    cursor = conn.cursor()

    cursor.execute("select code from blobs where id=1")
    item = cursor.fetchone()
    code = item[0]

    m={"code":code}
    m = urllib.urlencode(m) # 因为字符问题,需要编码,然后服务端解码

    result = hello_client.service.say_hello(m)
    print result