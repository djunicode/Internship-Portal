"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('internship/', views.InternshipList.as_view()),
    path('internshipDetails/<str:pk>/', views.InternshipDetail.as_view()),
]
"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from users import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),
	path('', views.apiOverview, name="api-overview"),
	path('internship-list/', views.internshipList, name="internship-list"),
	path('internship-detail/<str:pk>/', views.internshipDetail, name="internship-detail"),
	path('internship-create/', views.internshipCreate, name="internship-create"),
	path('internship-update/<str:pk>/', views.internshipUpdate, name="internship-update"),
	path('internship-delete/<str:pk>/', views.internshipDelete, name="internship-delete"),
    
    #user accounts
    path('accounts/', include('accounts.urls')),
    path('users/' , include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)