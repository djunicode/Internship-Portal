from django.urls import path
from . import views

urlpatterns = [
    path('internship/', views.InternshipList.as_view()),
    path('internshipDetails/<str:pk>/', views.InternshipDetail.as_view()),
    path('Research_ProjectLC/', views.Research_ProjectLC.as_view()),
    path('Research_ProjectRUD/<str:pk>/', views.Research_ProjectRUD.as_view()),
]