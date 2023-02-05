#-*- encoding:UTF-8 -*-

###################################################################################
#																				  # 
# Python Treemap Demo 1 (Use Treemap)	： demo1.py     						  #
# Writer: Unicoder.J  2019-09-17												  #
#																				  #
###################################################################################

import requests, json
import random
import hashlib

#jishanshan:
appid = '20190929000000000001' #你的appid
secretKey = 'abcdefghijklmnopqrst' #你的密钥
#test1
appid2 = '201910011157381'
secretKey2 = 'kE8I1yruXRsMyfIBsOsu'
#test2
appid3 = '201910011204131'
secretKey3 = 'BgUHA0Z3kCyqtBrtXz75'
# test92:
appid='201911051847531'
secretKey='8f3RAys3scsYKY2oL4Kz'
# now use:
appid='201910011204131'
secretKey='BgUHA0Z3kCyqtBrtXz75'

salt = random.randint(32768, 65536)
sign = appid+str(salt)+secretKey
m1 = hashlib.md5()
m1.update(sign.encode(encoding='UTF-8'))
sign = m1.hexdigest()

url_json = 'http://treemap.me/api/treat_data'
treemap = {   "width":100,
			"height":200,
			"sites":[
				{"name":"Google","pos":[0,0],"w":0,"h":0,"size":637313880},
				{"name":"Runoob","pos":[0,0],"w":0,"h":0,"size":13953508178},
				{"name":"jd","pos":[0,0],"w":0,"h":0,"size":54790216020},
				{"name":"suning","pos":[0,0],"w":0,"h":0,"size":1582824}
				],
			"app_id":appid,
			"sign":sign,
			"salt":str(salt)
		}
#treemap["app_id"] = appid
#treemap["sign"] = sign
#treemap["salt"] = str(salt)
data_json = json.dumps(treemap)  #dumps:将python对象转换为json数据
r_json = requests.post(url_json,json=data_json)

print(r_json)
print(r_json.text)
print(r_json.content)
print(type(r_json.content))
bytes = r_json.content
print(type(json.loads(bytes)))
dictionary = json.loads(bytes) #将json对象转换为字典对象
if isinstance(dictionary,dict):
	if 'error' in dictionary:   #dictionary.has_key('error') 's python3 syntex.
		print(str(dictionary["error"]))
	else:
		print(str(dictionary["width"])+","+str(dictionary["height"]))
		for i in dictionary["sites"]:
			print(i["name"]+": "+str(i["w"])+","+str(i["h"])+"; ("+str(i["pos"][0])+","+str(i["pos"][1])+")")