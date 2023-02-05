# -*- coding: utf-8 -*-
import sys
import os
import random
import math
import hashlib
import datetime

class Appid_generator(object):
	app_index = 0
	app_time = ""
	def gen_appid(self):
		app_id = ""
		#gen_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') #str类型
		gen_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S') #str类型
		five = range(2,6)  #five[0~3]=2~5
		if self.app_time == gen_time:
			if self.app_index <= 2:
				app_id = gen_time + str(five[self.app_index])
				self.app_index += 1
			else:
				app_id = gen_time + str(five[3])
		else:
			app_id = gen_time + str(1)
			self.app_index = 0
		self.app_time = gen_time
		return app_id




def getSign():
	#pass
	appid = '20190129000260104' #你的appid
	secretKey = 'kikbWfkfaQYzecQ6joIb' #你的密钥

	salt = random.randint(32768, 65536)
	sign = appid+str(salt)+secretKey
	m1 = hashlib.md5()
	m1.update(sign.encode(encoding='UTF-8'))
	#m1.update(sign)
	sign = m1.hexdigest()
	return (sign,salt)

def getSecretKey():
	#f = open('passwords.txt','a+')
	ls = ['0','1','2','3','4','5','6','7','8','9',
			'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
			'q','r','s','t','u','v','w','x','y','z',
			'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',
			'Q','R','S','T','U','V','W','X','Y','Z']   #26*2+10=62
	x = ''
	index = 0
	for i in range(20):
		#print(random.random())
		#index = int(math.floor(random.random()*62)) #生成0～61之间的数
		index = random.randint(0,61) #生成0～61之间的数
		print(index)
		x += ls[index]
		print(x)
	#f.write(x)
	#f.write('\n')
	#f.close()
	return x

