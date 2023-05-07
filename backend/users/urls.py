from django.urls import path
from . import views

urlpatterns = [
	path('', views.apiOverview, name="api-overview"),
	path('internship-create/', views.internshipCreate, name="internship-create"),

	path('internship-update/<str:pk>/', views.internshipUpdate, name="internship-update"),
	path('internship-delete/<str:pk>/', views.internshipDelete, name="internship-delete"),

    path('Research_ProjectLC/', views.Research_ProjectLC.as_view()),
    path('Research_ProjectRUD/<str:pk>/', views.Research_ProjectRUD.as_view()),
    path('HelloInternWS/', views.HelloIntern.as_view()),
    path('InternShala/', views.InternShala),
]