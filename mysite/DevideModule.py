#coding:utf-8
'''
Name: DevideModule
Description: 使用贪心(线性规划)算法排布画布上的按钮
Author: SamJi
Blog: http://blog.csdn.net/cava15
Date：2013/11/15
'''
# def DevideModule(L,n):
	# """ input//
	# L:list
	# n:length of L
	# output//
	# L: sorted L of input
	# """
	# #print "from 0 to "+ str(n-1)+" :"
	# recMergeSort(L,0,n-1)
import math


posInit = 0    #原值65：起始位置（y轴）
rate_index = 0.33   #比率系数，影响显示的形状

def washData(L):
	'''
	Function:将都是零的列表平均分配大小，将有零有整的列表去除零
	Input: ls with 0
	Output: ls
	Date: 2018/9/16'''
	#pass
	for i in L:
		if isinstance(i["pos"][0],float):
			i["pos"][0] = round(i["pos"][0])
		if isinstance(i["pos"][1],float):
			i["pos"][1] = round(i["pos"][1])
		if isinstance(i["w"],float):
			i["w"] = round(i["w"])
		if isinstance(i["h"],float):
			i["h"] = round(i["h"])
	return L
	
def devide(L,w,h):
	""" wrap function.对具有size的按钮序列在画布容积中排列。
	input//
	L:list that length is n
	w:the rectangle area's width
	h:the rectangle area's height
	s:the first element's index of L
	t:the last element's index of L
	//
	Output: 排布好的按钮数据序列，size,w,h,pos都具有值。
	//L[s...t],mean sorted L[s]...L[t]
	lsRec, the output rectangles' list data structure//
	Author： SamJi
	Blog： http://blog.csdn.net/cava15
	Date:  2014/3/1
	"""
	#global lsRec
	#lsRec = []
	
	pos = [0,posInit]
	for j in range(len(L)):
		L[j]["w"]=0
		L[j]["h"]=0
		L[j]["pos"]=pos
	#print "Initial L with zero value:" + str(L)
	#print "Now Start :::::::::::::::"
	#print "-----In devide-----"
	recurseDevide(L,w,h,pos)
	#print "\n The output L is : " + str(L)
	#L = washData(L)
	return L
	
def recurseDevide(L,w,h,pos):
	"""L的组成：
	   pos:元组，新锚点的坐标
	   w:每次迭代的宽度范围
	   h:每次迭代的高度范围
	   L:每次待迭代的部分列表数据"""
	#global lsRec
	#print "-----In recurseDevide-----\n"
	i = 0     #初始化i值为零，否则递归起来i值永远不会在递归中间初始化。
	i = len(L)
	#print "in recurse, len(L) == "+str(i)
	if i>=2 :
		#print "from "+str(s) + "  "+str(t)
		#devided = [0,0]                 #初始化一个元组（不好，待改进）
		devided = [None]
		#print "in iteration ,devided = [] : "+ str(devided)
		devided = devideLto2(L,w,h,pos)  # 将L分成两个devide，用于进一步递归。
		
		# rec1 = [0,0,[0,0]]    #w1,h1,pos1,初始化，待改进   
		# rec2 = [0,0,[0,0]]    #w2,h2,pos2 初始化，待改进
		# rec = [rec1,rec2]     #初始化，待改进 
		# rec = getDevidedWHP(L,w,h,pos)  #觉得这个函数和devideLto2最好合并起来比较好。
		#print "m=" + str(m)
		if devided[0] != []:  #递归的数列不为空数列   注意处理空值
			#print "devided[0] != [] len()="+str(len(devided[0]))
			recurseDevide(devided[0],devided[0][0]['w'],devided[0][0]['h'],devided[0][0]['pos'])  #因为devided[0][0]和devided[0][1]以及接下来的[0][2]等数据相同，所以取[0][0]的数据
		else:
			#print "devided[0] == []!"
			recurseDevide(devided[0],0,0,[0,posInit])
		if devided[1] != []:  #递归的数列不为空数列   注意处理空值
			#print "devided[1] != [] len()="+str(len(devided[1]))
			recurseDevide(devided[1],devided[1][0]['w'],devided[1][0]['h'],devided[1][0]['pos'])
		else:
			#print "devided[1] == []!"
			recurseDevide(devided[1],0,0,[0,posInit])
	elif i==1:
		# entityRec = {'pos'=[0,0],'w'=0,'h'=0}  #初始化嵌套元素，待改进
		# entityRec['pos']=pos
		# entityRec['w']=w
		# entityRec['h']=h
		L[0]['pos'] = pos   #这里要用L[0]因为只有一个项目，那么就是第一个项目
		L[0]['w'] = w
		L[0]['h'] = h
		#SlsRec.append(entityRec)
		return
	elif i==0:
		return 
def devideLto2(L,w,h,pos):
	""" //input
	L: list with data  each element is {'isDir':true,'size':num,'name':string}
	return: List: List with data each element is {'list':L,'w':width of devided rec,'h':height of devided rectangle,'pos':position of devided rectangle}.
	"""
	#print "-----In devideLto2-----"
	allSize = 0
	for m in range(len(L)):
		allSize += L[m]['size']
	part = 0
	i=0
	rate = 0.0
	part = L[0]['size']        #初始化part and rate
	rate = part*1.0/allSize if(allSize != 0) else 0.0
	for i in range(1,len(L)):  #i=1  len(L)=2
		#print "--add part and rate:in range(1,"+str(len(L))+")"
		#print "part1="+str(part)
		#print "rate1="+str(rate)
		if i==len(L)-1:  #i=1  len(L)=2
			#print " In devideLto2,never > 0.25,so in i==len(L)-1: and is "+str(i)
			L1 = L[:i]   #L1=L[0]
			L2 = L[i:]   #L2=L[1]
			break
		if rate > rate_index:  #i=1 Len(L)=3
			L1 = L[:i]   #L1=L[0,1]
			L2 = L[i:]   #L2=L[2]
			break
		part += L[i]['size']        #之前初始化了，这里再重复运算
		rate = part*1.0/allSize if (allSize !=0) else 0.0    #同上
		#print "part2="+str(part)
		#print "rate2="+str(rate)

	# pos = [0,0]
	# rec1 = {'list':L1,'w':0L,'h':0L,'pos':pos}  # 产生的两个元素之一（列表devided的元素1）
	# rec2 = {'list':L2,'w':0L,'h':0L,'pos':pos}  # 产生的两个元素之二（列表devided的元素2）
	List = []
	List.append(L1)
	List.append(L2)
	#print "List= "+str(List)
	
	#以下是使用所有的规则得出的结果
	#print "i="+str(i)+"; rate="+str(rate)
	for i in range(len(List[0])):    #或取消迭代仅将数据写入List[0][0]，可提高速度
		if w>h:
			List[0][i]['w'] = math.floor(w*rate)
			List[0][i]['h'] = h
			List[0][i]['pos'] = pos
		else:
			List[0][i]['h'] = math.floor(h*rate)
			List[0][i]['w'] = w
			List[0][i]['pos'] = pos
	for i in range(len(List[1])):
		if w>h:
			List[1][i]['w'] = math.floor(w-w*rate)
			List[1][i]['h'] = h
			List[1][i]['pos'] = [pos[0]+math.floor(w*rate),pos[1]]
		else:
			List[1][i]['h'] = math.floor(h-h*rate)
			List[1][i]['w'] = w
			List[1][i]['pos'] = [pos[0],pos[1]+math.floor(h*rate)]
	#print "Devided List[0] = " + str(List[0]) 
	#print "Devided List[1] = " + str(List[1]) 
	return List

	
		
	