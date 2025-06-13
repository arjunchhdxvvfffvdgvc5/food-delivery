"""
URL configuration for fooddelivery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings 
from django.conf.urls.static import static
from fooddeliveryapp.views import *
from fooddeliveryapp import admin_urls,customer_urls,restaurent_urls,agent_urls
urlpatterns = [
    path('admin/',include(admin_urls)),
    path('customer/',include(customer_urls)),
    path('restaurent/',include(restaurent_urls)),
    path('agent/',include(agent_urls)),


    path('', homeview.as_view(), name='home'),
    path('register/', registerview.as_view(), name='register'),
    path('login/', loginview.as_view(), name='login'),
    path('restaurent_reg/', restaurentview.as_view(), name='restaurent_reg'),
    path('agent_reg/', agentview.as_view(), name='agent_reg'),
    path('forgot-password/', ForgotPassword.as_view(), name='forgot_password'),
    path('password-reset/<uidb64>/<token>/',PasswordReset.as_view(), name='password_reset'),
    path('success/', SuccessView.as_view(), name='success'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
