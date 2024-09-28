#coding=utf-8
#import a.aa.module_AA
#a.aa.module_AA.fun_AA()
#from a.aa import module_AA
#module_AA.fun_AA()
#from a.aa.module_AA import fun_AA
#fun_AA()
import math
import a
print(a.math.pi)
print(id(math))
print(id(a.math))

from a import *#实际上是导入__init__里面的__all__方法
module_A.fun_A()