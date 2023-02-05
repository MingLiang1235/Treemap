# -*- coding: utf-8 -*-
import PassGenerator1
import threading

def main():
	a = PassGenerator1.Appid_generator()  #初始化一个Appid_generator类的实例。
	print(a.gen_appid())
	print(a.gen_appid())
	print(a.gen_appid())
	print(a.gen_appid())
	print(a.gen_appid())
	print(a.gen_appid())
	b = [a]
	timer = threading.Timer(5,func,b)  #运行func函数，把b中的内容作为func的参数！！！
	timer.start()
def func(a):
	print(a.gen_appid())
	print(a.gen_appid())
	print(a.gen_appid())
	print(a.gen_appid())

if __name__=='__main__':
	main()