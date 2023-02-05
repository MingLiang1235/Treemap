#_*_ encoding: utf-8 *_*
from django import forms
from django.contrib.auth.models import User
from . import models
import datetime
from datetime import timedelta


class LoginForm(forms.Form):
	username = forms.CharField(label='姓名',max_length=10)
	password = forms.CharField(label='密码',widget=forms.PasswordInput())

class ContactForm(forms.Form):
	CITY = [
        ['SH', 'Shanghai'],
        ['GZ', 'Guangzhou'],
        ['NJ', 'Nanjing'],
        ['HZ', 'Hangzhou'],
        ['WH', 'Wuhan'],
        ['NA', 'Others'],
	]
	user_name = forms.CharField(label='您的姓名', max_length=50, initial='李大仁')
	user_city = forms.ChoiceField(label='居住城市', choices=CITY)
	#user_school = forms.BooleanField(label='是否在学', required=False)
	user_email = forms.EmailField(label='电子邮件')
	user_message = forms.CharField(label='您的意见', widget=forms.Textarea)
class DateForm(forms.Form):
	now = datetime.datetime.now()
	this_month_start = datetime.date(now.year, now.month, 1)
	today = datetime.date.today()
	from_date = forms.DateField(label='开始时间', widget=forms.DateInput(attrs={'type':'date'}), initial=str(this_month_start))
	to_date = forms.DateField(label='结束时间', widget=forms.DateInput(attrs={'type':'date'}), initial=str(today))
