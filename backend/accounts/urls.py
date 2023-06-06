from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterApi.as_view(), name='register user'),
    path('login/', views.LoginApi.as_view(), name='login user'),
    path('logout/', views.LogoutApi.as_view(), name='logout user'),
    path('ProfessorDetails/', views.ProfessorDetailsLC.as_view(), name='prof profile list'),
    path('ProfessorDetails/<str:pk>/', views.ProfessorDetailsU.as_view(), name='prof profile update'),
    path('UserDetails/', views.UserDetailsL.as_view(), name='user profile'),
    path('UserDetails/<str:pk>/', views.UserDetailsU.as_view(), name='user profile update'),
]