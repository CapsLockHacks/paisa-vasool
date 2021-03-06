"""upicollect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include

from upi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/groups/', views.GroupList.as_view()),
    path('api/groups/<int:pk>/', views.GroupDetail.as_view()),
    path('api/contacts/', views.ContactList.as_view()),
    path('api/contacts/<int:pk>/', views.ContactDetail.as_view()),
    path('api/subscriptions/', views.SubscriptionList.as_view()),
    path('api/subscriptions/<int:pk>/', views.SubscriptionDetail.as_view()),
    path('api/splits/create/', views.Splits.as_view()),
    path('api/splits/fetch/', views.Splits.as_view()),
    path('api/payments/', views.PaymentList.as_view()),
    path('api/payments/<int:pk>/', views.PaymentDetail.as_view()),
    path('api/sync/', views.SyncSMS.as_view()),
    path('api/health/', views.Health.as_view()),
    path('django-rq/', include('django_rq.urls'))
]
