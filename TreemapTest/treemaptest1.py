#-*- encoding:UTF-8 -*-

###################################################################################
#																				  # 
# Python Treemap Test 1 (Use Treemap)											  #
# Writer: Unicoder.J  2019-09-17												  #
#																				  #
###################################################################################

import requests,json

url_json = 'http://127.0.0.1:15000/api/test_treat_data'
data_json = json.dumps({'key1':'value1','key2':'value2'})  #dumps:将python对象解码为json数据
r_json = requests.post(url_json,json=data_json)

print(r_json)
print(r_json.text)
print(r_json.content)
print(type(r_json.content))
bytes = r_json.content
print(type(json.loads(bytes)))
dictionary = json.loads(bytes) #将json对象转换为字典对象
print(str(dictionary["width"])+","+str(dictionary["height"]))
for i in dictionary["sites"]:
	print(i["name"]+" : "+str(i["value"])+"; "+str(i["pos"][0])+":"+str(i["pos"][1]))