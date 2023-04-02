from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterApi.as_view(), name='register user'),
    path('login/', views.LoginApi.as_view(), name='login user'),
]