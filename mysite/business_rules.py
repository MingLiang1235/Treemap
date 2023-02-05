#-*- encoding:UTF-8 -*-
###################################################################################
#																				  # 
# Python Treemap Business rules ： business_rules.py     						  #
# Writer: Unicoder.J  2019-09-17												  #
#																				  #
###################################################################################

from .models import Profile,Use_record
import django.utils.timezone as timezone
import datetime


def set_use_record(app_id):
	try:
		profile = Profile.objects.get(app_id=app_id)
		try:
			#user = User.objects.get(user_id=profile.user_id)
			date = datetime.datetime.now().strftime('%Y%m%d')
			print("today:"+date) 
			print("profile.user_id:"+str(profile.user_id))
			records = None
			records = Use_record.objects.filter(user_id=profile.user_id,used_date=datetime.datetime.now().date())
			print("records:"+str(records))
			if records: #有多个天数记录
				print("Has records:"+str(records[0]))
				print(records[0].used_date.strftime('%Y%m%d'))
				if len(records) == 1 :  #数据库里面只有一条数据
					print("len(records) == 1")
					if str(date) == records[0].used_date.strftime('%Y%m%d'): #如果是今天的数据，就在今天的数据上加一
						print ("str(date) work!")
						records[0].used += 1
						records[0].save()
						#has_today = True
					else:  #如果不是今天的数据，添加一个新一天的记录（还是同一个用户id）
						rcd = Use_record(user_id=profile.user_id)
						rcd.used+=1
						rcd.used_date = timezone.now()
						rcd.save()
				else:    #数据库里面同一用户有多天数据
					print("len(records of User_record {}:{}".format(profile.user_id,str(len(records))))
					has_today = False
					for  record in records:
						print("record: "+str(record))
						if str(date) == str(record.used_date.strftime('%Y%m%d')): #今天在天数之中
							print("ok,today has record. "+str(date))
							record.used += 1
							record.save()
							has_today = True
							break
					if not has_today:  #今天不在天数之中,创建同一个用户今天的数据
						record = Use_record(user_id=profile.user_id)
						record.used += 1
						record.used_date = timezone.now()
						record.save()

			else: #本用户一天的记录都没有
				record = Use_record(user_id=profile.user_id)
				record.used += 1
				record.used_date = timezone.now()
				record.save()
		except:
			print("Has not records where user_id = "+ str(profile.user_id))
			
	except Profile.DoesNotExist:
		print("log set use record error.can not find user : "+ app_id)

def minus_one_credit(app_id):
	try:
		profile = Profile.objects.get(app_id=app_id)
		if profile.credit_point > 0:
			profile.credit_point -= 1
			profile.save()
			print("log profile's credit point minus 1:" + str(profile.credit_point))
			return True
		else:
			print("log profile's credit point is empty.")
			return False
	except Profile.DoesNotExist:
		print("log error.")
		return False