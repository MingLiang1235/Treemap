from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators import csrf
from django.contrib.auth.models import User
from . import models, forms, DevideModule,PassGenerator,business_rules

from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import json
import _thread
import hashlib
import datetime

from .models import Profile,Use_record
from django.core.mail import EmailMessage
from django.db import connection, connections


@login_required(login_url='/')
def contact(request):
	login_common(request)
	login_form = forms.LoginForm()
	#context = {}
	if request.user.is_authenticated:
		username = request.user.username
		useremail = request.user.email
	if request.method == "POST":
		form = forms.ContactForm(request.POST)
		if form.is_valid():
			message = "感谢你的来信，我们会尽速处理你的宝贵意见。"
			user_name = form.cleaned_data['user_name']
			user_id = username
			user_city = form.cleaned_data['user_city']
			user_email = form.cleaned_data['user_email']
			user_message = form.cleaned_data['user_message']

			mail_body = u'''
				网友用户名：{}
				网友姓名：{}
				居住城市：{}
				反馈意见：如下
				{}'''.format(user_id,user_name,user_city,user_message)

			email = EmailMessage(  '来自Treemap网站的网友意见',
				mail_body,
				user_email,
				['unicoder@sohu.com'])
			email.send()
		else:
			message = "请检查您的输入信息是否正确。"
	else:
		form = forms.ContactForm()
	return render(request,'contact.html',locals())

def hello(request):
	context = {}
	context['hello'] = 'Good Morning Sir.What a nice day!'
	return render(request,'hello.html',context)

def index1(request):
	context = {}
	if request.POST:
		context['user_name'] = request.POST['user_id']
	return render(request,'index.html',context)
def login_common(request):
	if 'username' in request.session:  #会话中存有该用户名
		user_name = request.session['username']
		user_email = request.session['useremail']
		print("user_name in session")
		#messages.add_message(request, messages.SUCCESS, '在会话中存有该用户名.')
		return redirect('.')
	elif request.POST:        #通过登录取得用户名
		login_form = forms.LoginForm(request.POST)
		if login_form.is_valid():
			login_name = request.POST['username'].strip()
			login_password = request.POST['password']
			user = authenticate(username=login_name,password=login_password)

			if user is not None:
				if user.is_active:
					auth.login(request,user)
					print("success")
					messages.add_message(request, messages.SUCCESS, '成功登录了')
					user_name = login_name

					request.session['username'] = user.username
					request.session['useremail']= user.email

					return render(request,'index.html',locals())
				
				else:
					#message = u'帐号尚未启用.'
					messages.add_message(request, messages.WARNING, '账号尚未启用')
			else:
				#message = u'登录失败'
				messages.add_message(request, messages.WARNING, '登录失败,没有这个用户/密码组合')
		else:
			#message = u'请检查输入的字段内容'
			messages.add_message(request, messages.INFO,'请检查输入的字段内容')

	else:
		login_form = forms.LoginForm()
	
def index(request):
	login_common(request)
	login_form = forms.LoginForm()
	#context = {}
	if request.user.is_authenticated:
		username = request.user.username
		useremail = request.user.email
		user = User.objects.get(username=username)
		try:
			profile = Profile.objects.get(user_id=user.id)
			app_id = profile.app_id
			secret_key = profile.secret_key
		except Profile.DoesNotExist:
			pass
	# if 'username' in request.session:
	# 	user_name = request.session['username']
	# 	user_email = request.session['useremail']
	# 	print("user_name in session")
	#	messages.add_message(request, messages.SUCCESS, '在会话中存有该用户名.')
	#	return render(request,'index.html',locals())
	# elif request.POST:
	# 	login_form = forms.LoginForm(request.POST)
	# 	if login_form.is_valid():
	# 		login_name = request.POST['username'].strip()
	# 		login_password = request.POST['password']
	# 		user = authenticate(username=login_name,password=login_password)

	# 		if user is not None:
	# 			if user.is_active:
	# 				auth.login(request,user)
	# 				print("success")
	# 				messages.add_message(request, messages.SUCCESS, '成功登录了')
	# 				user_name = login_name

	# 				request.session['username'] = user.username
	# 				request.session['useremail']= user.email

	# 				return render(request,'index.html',locals())
				
	# 			else:
	# 				#message = u'帐号尚未启用.'
	# 				messages.add_message(request, messages.WARNING, '账号尚未启用')
	# 		else:
	# 			#message = u'登录失败'
	# 			messages.add_message(request, messages.WARNING, '登录失败,没有这个用户/密码组合')
	# 	else:
	# 		#message = u'请检查输入的字段内容'
	# 		messages.add_message(request, messages.INFO,'请检查输入的字段内容')

	# else:
	# 	login_form = forms.LoginForm()
	# 	#context['user_name'] = request.POST['user_id']
		#return render(request,'dvlp_info.html',locals())
	return render(request,'index.html',locals())
# Create your views here.
def logout(request):
	auth.logout(request)
	messages.add_message(request,messages.INFO,"成功注销了")
	return redirect('/')

def prodinfo(request):
	login_common(request)
	login_form = forms.LoginForm()
	if request.user.is_authenticated:
		username = request.user.username
		useremail = request.user.email
	# if 'username' in request.session:
	# 	user_name = request.session['username']
	# 	user_email = request.session['useremail']
	return render(request,'prodinfo.html',locals())

def prod_agreement(request):
	login_common(request)
	login_form = forms.LoginForm()
	if request.user.is_authenticated:
		username = request.user.username
		useremail = request.user.email
	# if 'username' in request.session:
	# 	user_name = request.session['username']
	# 	user_email = request.session['useremail']
	return render(request,'prod_agreement.html',locals())

def document(request):
	login_common(request)
	login_form = forms.LoginForm()
	if request.user.is_authenticated:
		username = request.user.username
		useremail = request.user.email
	# if 'username' in request.session:
	# 	user_name = request.session['username']
	# 	user_email = request.session['useremail']
	return render(request,'document.html',locals())

@login_required(login_url='/')
def dvlp_overall(request):
	gap = 10
	login_common(request)
	if request.user.is_authenticated:
		username = request.user.username
		useremail = request.user.email
	prof = None
	app_id = None
	user = User.objects.get(username=username)

	try:
		profile = Profile.objects.get(user_id=user.id)
		prof = profile
	except Profile.DoesNotExist:
		pass
	try:
		app_id = prof.app_id
		secret_key = prof.secret_key
		if app_id == None:
			print("Have not app_id")
		else:              #app_id有数据，有可能存在使用记录
			print("Have app_id")
			#####################################################
			#使用原生SQL：
			cursor = connection.cursor()  # cursor = connections['default'].cursor()
			#cursor.execute("""SELECT * from auth_user where id = %s""", [1])
			cursor.execute(
				'''select * from mysite_use_record as a where a.user_id = %s order by a.used_date desc limit 0,10''',[user.id])
			ls = cursor.fetchall()
			#Use_record = Use_record.objects.raw(
			#	'''select * from mysite_use_record as a where a.user_id = %s order by a.used_date desc limit 0,5''',[user.id])
			print("ls:"+ str(ls))
			Use_record = []
			i=1
			for ur in ls:
				cell = []
				cell.append(i)
				cell.append(str(ur[1]))  ###从datetime.date(2019, 10, 20)转变到 2019-10-20
				cell.append(ur[3])
				Use_record.append(cell)
				i+=1
			print("Use_record:"+str(Use_record))
			cursor.execute("select sum(a.used) from mysite_use_record as a where a.user_id = %s",[user.id])
			Use_record_sum = if_have_value(cursor.fetchone())  #fetchone() like (11,) or (None,) or None
			#print("Use_record_sum fetch:{}".format(Use_record_sum)) # like (11,) or 0
			if Use_record_sum != 0:
				Use_record_sum = Use_record_sum[0]  #like ( 6 , ) to 6 , (None,) to 0
			print("Use_record_sum:{}".format(Use_record_sum))

			today = datetime.date.today()
			oneday = datetime.timedelta(days=1)
			yesterday = today-oneday
			#print(yesterday) #like 2019-10-22
			cursor.execute("select a.used from mysite_use_record as a where a.user_id = %s and a.used_date = %s",
				[user.id,yesterday])
			Yday_record_used = if_have_value(cursor.fetchone())
			#print("Yesterday used fetch:{}".format(Yday_record_used)) #like (2,)
			if Yday_record_used != 0:
				Yday_record_used = Yday_record_used[0] 
			#print("Yesterday used:{}".format(Yday_record_used))

			first = datetime.date(day=1, month=today.month, year=today.year)
			lastMonth = first-datetime.timedelta(days=1)
			#print(lastMonth) #like 2019-9-30
			cursor.execute("select sum(a.used) from mysite_use_record as a where a.user_id = %s and a.used_date > %s",
				[user.id,lastMonth])
			Lmonth_record_sum = if_have_value(cursor.fetchone())
			if Lmonth_record_sum != 0:
				Lmonth_record_sum = Lmonth_record_sum[0]
			print("LastMonth used:{}".format(Lmonth_record_sum))

			#today = datetime.date.today()   前面已经定义过
			print("Month:{}".format(today.month))
			The_month = str(today.year)+'-'+str(today.month)
			The_yesterday = yesterday.strftime("%Y-%m-%d")

			Remain_credit = profile.credit_point

	except:
		pass
	if request.method == "GET":
		req = request.GET.get('req')
		if req == 'detail':  #从overall直接点进来，req=='detail'
			date_form = forms.DateForm()
			# try:
			# 	from_date = request.GET['from_date']
			# 	to_date = request.GET['to_date']
				
			cursor = connection.cursor()
			cursor.execute(
			 	'''select a.used_date,a.used from mysite_use_record as a where a.user_id = %s order by a.used_date desc limit 0,%s''',[user.id,gap])
			#Detail_list = cursor.fetchall()
			ls = cursor.fetchall()
			Detail_list = []
			i=1
			for dl in ls:
				cell = []
				cell.append(i)
				cell.append(str(dl[0]))
				cell.append(dl[1])
				Detail_list.append(cell)
				i+=1
			print("Detail_list:{}".format(Detail_list))
			# 	print("Detail_list:{}".format(Detail_list))
			# except:
			# 	pass
			return render(request,'dvlp_detail.html',locals())
	return render(request,'dvlp_overall.html',locals())

@login_required(login_url='/')
def dvlp_detail(request):
	gap = 10   # 每页显示多少条数据
	#index = 1  #分页的每一页
	login_common(request)
	if request.user.is_authenticated:
		username = request.user.username
		useremail = request.user.email
	prof = None
	app_id = None
	user = User.objects.get(username=username)

	try:
		profile = Profile.objects.get(user_id=user.id)
		prof = profile
	except Profile.DoesNotExist:
		pass
	try:
		app_id = prof.app_id
		secret_key = prof.secret_key
		if app_id == None:
			print("Have not app_id")
		else:              #app_id有数据，有可能存在使用记录
			print("Have app_id")
			#####################################################
			#使用原生SQL：
			cursor = connection.cursor()  # cursor = connections['default'].cursor()
			#cursor.execute("""SELECT * from auth_user where id = %s""", [1])
			cursor.execute(
				'''select * from mysite_use_record as a where a.user_id = %s order by a.used_date desc limit 0, %s''',[user.id, gap-1])
			ls = cursor.fetchall()
			#Use_record = Use_record.objects.raw(
			#	'''select * from mysite_use_record as a where a.user_id = %s order by a.used_date desc limit 0,5''',[user.id])
			print("ls:"+ str(ls))
			Use_record = []
			i=1
			for ur in ls:
				cell = []
				cell.append(i)
				cell.append(str(ur[1]))  ###从datetime.date(2019, 10, 20)转变到 2019-10-20
				cell.append(ur[3])
				Use_record.append(cell)
				i+=1
			print("Use_record_from_ls:"+str(Use_record))
			cursor.execute("select sum(a.used) from mysite_use_record as a where a.user_id = %s",[user.id])
			Use_record_sum = if_have_value(cursor.fetchone())  #fetchone() like (11,) or (None,) or None
			#print("Use_record_sum fetch:{}".format(Use_record_sum)) # like (11,) or 0
			if Use_record_sum != 0:
				Use_record_sum = Use_record_sum[0]  #like ( 6 , ) to 6 , (None,) to 0
			print("Use_record_sum:{}".format(Use_record_sum))

			today = datetime.date.today()
			oneday = datetime.timedelta(days=1)
			yesterday = today-oneday
			#print(yesterday) #like 2019-10-22
			cursor.execute("select a.used from mysite_use_record as a where a.user_id = %s and a.used_date = %s",
				[user.id,yesterday])
			Yday_record_used = if_have_value(cursor.fetchone())
			#print("Yesterday used fetch:{}".format(Yday_record_used)) #like (2,)
			if Yday_record_used != 0:
				Yday_record_used = Yday_record_used[0] 
			#print("Yesterday used:{}".format(Yday_record_used))

			first = datetime.date(day=1, month=today.month, year=today.year)
			lastMonth = first-datetime.timedelta(days=1)
			#print(lastMonth) #like 2019-9-30
			cursor.execute("select sum(a.used) from mysite_use_record as a where a.user_id = %s and a.used_date > %s",
				[user.id,lastMonth])
			Lmonth_record_sum = if_have_value(cursor.fetchone())
			if Lmonth_record_sum != 0:
				Lmonth_record_sum = Lmonth_record_sum[0]
			print("LastMonth used:{}".format(Lmonth_record_sum))

			#today = datetime.date.today()   前面已经定义过
			print("Month:{}".format(today.month))
			The_month = str(today.year)+'-'+str(today.month)
			The_yesterday = yesterday.strftime("%Y-%m-%d")

			Remain_credit = profile.credit_point

	except:
		pass
	if request.method == "GET":
		date_form = forms.DateForm()
		from_date='2019-10-1'
		to_date='2019-10-31'
		Page_num = []
		
		try:
			from_date = request.GET['from_date']     #点击查询，查询fromdate和todate。
			to_date = request.GET['to_date']
			request.session['from_date'] = from_date
			request.session['to_date'] = to_date
			print("from_date:{},to_date:{}".format(from_date,to_date))

			Detail_list = all_detail_list(user.id,from_date,to_date)
			

			Page_num = get_page_num(len(Detail_list),gap) # len(Detail_list): 6
			request.session['page_num'] = Page_num
			Detail_list = Detail_list[0:gap]  #在取得总的条目数后，取得分页页数（page_num)，然后再削减总条目数得到当前页显示的条目数
		except:
			pass

		try:
			index = request.GET['index']  #  index从1开始起算
			print("In request.GET[index]:{}".format(index))
			intent = (int(index)-1)*gap
			print("Intent:{}".format(intent))
			try:
				from_date = request.session['from_date']
				to_date = request.session['to_date']
				Detail_list = all_detail_list(user.id,from_date,to_date)
			except:
				Detail_list = all_detail_list(user.id,from_date,to_date)
			print("Before cut:{}".format(Detail_list))
			Detail_list = Detail_list[intent:intent+gap]
			print("After cut:{}".format(Detail_list))
			try:
				Page_num = request.session['page_num']
			except:
				Page_num = []
			(from_num,to_num)=get_from_to(Page_num,index,gap)
			Detail_list = cut(Detail_list,from_num,to_num)
		except:
			pass
	return render(request,'dvlp_detail.html',locals())

def cut(ls,from_num,to_num):
	return ls[from_num-1,to_num+1]

def get_from_to(page_num,index,gap):
	index = int(index)
	if index == int(page_num[-1]/gap):  #最后一页
		from_num = gap*(index-1)+1
		to_num = page_num[-1]
	else:
		from_num = gap*(index-1)+1
		to_num = gap*index
	return (from_num,to_num)
def get_page_num(i,gap): #i:总数，gap：每页条数
	print("In get_page_num.i = {}".format(i))
	Page_num = []
	if (i%gap) > 0:  # 6%5 == 1
		k = int(i/gap) + 1  #k=2  分成两页
	else:   #5%5 ==1
		k = int(i/gap)   #k=1  分成一页
	for j in range(k):
		Page_num.append(j+1)

	print("Page_num:{}".format(Page_num))
	return Page_num

def all_detail_list(user_id,from_date,to_date):
	print("In all_detail_list.")
	cursor = connection.cursor()
	cursor.execute(
	'''select a.used_date,a.used from mysite_use_record as a where a.user_id = %s and a.used_date>= %s and a.used_date<= %s order by a.used_date desc''',[user_id,from_date,to_date])
	ls = cursor.fetchall()
	Detail_list = []
	i=1
	for dl in ls:
		cell = []
		cell.append(i)
		cell.append(str(dl[0]))
		cell.append(dl[1])
		Detail_list.append(cell)
		i+=1
	#print("Detail_list:{}".format(Detail_list))
	return Detail_list

def if_have_value(value):
	if value:
		if value[0]:
			return value
		else:
			return 0
	else:
		return 0

@login_required(login_url='/')
def dvlp_billing(request):
	login_common(request)
	if request.user.is_authenticated:
		username = request.user.username
		useremail = request.user.email
	prof = None
	user = User.objects.get(username=username)

	return render(request,'dvlp_billing.html',locals())

@login_required(login_url='/')
def dvlp_info(request):
	# if 'username' in request.session:
	# 	user_name = request.session['username']
	# 	user_email = request.session['useremail']
	# if login_common(request):
	# 	messages.add_message(request,messages.INFO,"html head load 成功。")
	# else:
	# 	messages.add_message(request,messages.INFO,"html head load fails.")
	login_common(request)
	if request.user.is_authenticated:
		username = request.user.username
		useremail = request.user.email
	prof = None
	user = User.objects.get(username=username)
	try:
		profile = Profile.objects.get(user_id=user.id)
		prof = profile
	except Profile.DoesNotExist:
		#messages.add_message(request, messages.WARNING, '无法找到该用户信息，请联系系统管理员。')
		pass
	try:
		app_id = prof.app_id
		secret_key = prof.secret_key
		if app_id != None:
			#print(app_id)
			pass
		else:
			print("Have not app_id") 
	except:
		pass
	# if 'username' in request.session:
	#  	user_name = request.session['username']
	#  	user_email = request.session['useremail']
	return render(request,'dvlp_info.html',locals())

@login_required(login_url='/')
def generate_app_id(request):
	#login_common(request)
	d = {}
	if request.user.is_authenticated:
		username = request.user.username
		useremail = request.user.email
		print("In gen_app_id: user is authenticated")
		if (request.method == 'POST'):
			con_data = request.POST
			post_body = request.body
			print("1:")
			print(post_body)
			# json_result = json.loads(post_body)
			# print("2:")
			# print (json_result)
			# d = json.loads(json_result)

			g = PassGenerator.Appid_generator()
			app_id = g.gen_appid()
			if is_new(username):
				#d["app_id"] = app_id
				#d["secret_key"] = PassGenerator.getSecretKey()
				user = User.objects.get(username=username)
				try:
					profile = Profile.objects.get(user_id=user.id)
					profile.app_id = app_id
					profile.secret_key = PassGenerator.getSecretKey()
					profile.credit_point = 1000
					profile.save()
				except Profile.DoesNotExist:
					prof = Profile(user_id=user.id)
					prof.app_id = app_id
					prof.secret_key = PassGenerator.getSecretKey()
					prof.credit_point = 1000
					prof.save()
			else:
				#d={}
				error = "Cant gen new app_id cause already has one."
		else:
			error = "Can't offer service."
	else:
		error = "You are not authenticated."
	#return HttpResponse(json.dumps(d,ensure_ascii=False),content_type="application/json,charset=utf-8")
	return render(request,'dvlp_info.html',locals())

def is_new(username):
	user = User.objects.get(username=username)
	try: 
		profile = Profile.objects.get(user_id=user.id)
		try:
			old_app_id = profile.app_id
			print("profile.old_app_id:" + old_app_id)
			return False
		except:
			print("Has profile,but has not app_id.")
			return True
	except Profile.DoesNotExist:
		return True


def treat_data(request):
	if (request.method == 'POST'):
		con_data = request.POST
		post_body = request.body
		json_result = json.loads(post_body.decode('utf-8'))
		d = json.loads(json_result)
		print(str(d))
		# myObj = { "width":100,
		# 		"height":200,
		# 		"sites":[
		# 			{"name":"Google","value":100,"pos":[0,1]},
		# 			{"name":"Runoob","value":1000,"pos":[100,150]},
		# 			{"name":"jd","value":2000,"pos":[150,150]}
		# 			]
		# 	}
		App_id = d["app_id"]
		Sign = d["sign"]
		Salt = d["salt"]
		if valid(App_id,Sign,Salt):
			try:
				if not business_rules.minus_one_credit(App_id):
					D["error"] = "52002"   # credit has used off,remain zero.
					return HttpResponse(json.dumps(D,ensure_ascii=False),content_type="application/json,charset=utf-8")
				_thread.start_new_thread( business_rules.set_use_record, (App_id,) )
			except:
				print("Error: unable to start thread")

			L = d["sites"]
			W = d["width"]
			H = d["height"]
			L = DevideModule.devide(L,W,H)
			D = {}
			D["width"] = W
			D["height"] = H
			D["sites"] = L
		else:
			D = {}
			D["error"] = "52001"  #"Invalid app_id/secret_key,please try again."
	return HttpResponse(json.dumps(D,ensure_ascii=False),content_type="application/json,charset=utf-8")



def valid(app_id,sign,salt):
	print(app_id+","+sign+","+salt)
	try:
		profile = Profile.objects.get(app_id=app_id)
		mySign = app_id+salt+profile.secret_key
		m1 = hashlib.md5()
		m1.update(mySign.encode(encoding='UTF-8'))
		mySign = m1.hexdigest()
		if sign == mySign:
			return True
		else:
			return False
	except Profile.DoesNotExist:
		return False
	
def test_treat_data(request):
	if (request.method == 'POST'):
		con_data = request.POST
		print("con_data"+str(con_data))
		post_body = request.body
		print("request_body:"+ str(post_body))
		json_result = json.loads(post_body)
		print(json_result)
		#print(json_result['key1']+";"+json_result['key2'])
		print(type(json_result))
		if type(json_result) == type({}):
			#if json_result.has_key('key1'):  #python3不能使用这个语法。
			if 'key1'in json_result:          #python3使用该语法。
				a = json_result['key1']
				print("json_result is a dict and has key1 :" + str(a))
		else:
			a = json.loads(json_result)['key1']
			print("json result is a str and his value of 'key1' is :" + a)
			b = json.loads(json_result)['key2']
			print("json result is a str and his value of 'key2' is :" + b)
		myObj = { "width":100,
					"height":200,
					"sites":[
						{"name":"Google","value":100,"pos":[0,1]},
						{"name":"Runoob","value":1000,"pos":[100,150]},
						{"name":"jd","value":2000,"pos":[150,150]}
						]
				}
	return HttpResponse(json.dumps(myObj,ensure_ascii=False),content_type="application/json,charset=utf-8")