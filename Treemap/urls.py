"""Treemap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from mysite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    #path('api/index/',views.index),
    path('logout/',views.logout),
    path('api/prodinfo/',views.prodinfo),
    path('api/document/',views.document),
    path('api/dvlp_info/',views.dvlp_info),
    path('api/dvlp_overall/',views.dvlp_overall),
    path('api/dvlp_overall/dvlp_detail/',views.dvlp_detail),
    path('api/billing/',views.dvlp_billing),
    #path('api/test_treat_data',views.test_treat_data),
    path('api/treat_data',views.treat_data),
    path('api/generate_app_id',views.generate_app_id),
    path('contact/',views.contact),
    path('accounts/', include('registration.backends.default.urls')),
    path('api/prod_agreement/',views.prod_agreement),

]
