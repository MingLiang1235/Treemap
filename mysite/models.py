from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	app_id = models.CharField(max_length=21,unique=True)
	secret_key = models.CharField(max_length=20)
	credit_point = models.PositiveIntegerField(default=1000)
class Billing(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	charge = models.FloatField(max_length=20)
	charge_date = models.DateTimeField(null=False,default=timezone.now)
class Use_record(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	used = models.PositiveIntegerField(default=0)
	used_date = models.DateField(null=False,default=timezone.now)

	class Meta:
		ordering = ('-used_date',)