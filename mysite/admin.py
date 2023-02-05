from django.contrib import admin
from mysite import models
# Register your models here.
admin.site.register(models.Profile)
admin.site.register(models.Billing)
admin.site.register(models.Use_record)