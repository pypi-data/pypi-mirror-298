#coding=gbk
from distutils.core import setup
setup(
    name="1_super_test",#对外模块的名字
    version="1.0",#版本号
    decription="这是一个对外发布的模块",#描述
    author="胡琳",#作者
    author_email="lily345543@126.com",
    py_modules=["super.module_B1","super.module_B2"])#要发布的模块