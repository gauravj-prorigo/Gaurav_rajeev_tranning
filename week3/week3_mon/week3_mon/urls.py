"""
URL configuration for week3_mon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from home.views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from home.views import RegisterView ,LoginView ,BlogViewSet
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register('blogs',BlogViewSet)
router.register('tasks', TaskViewSet)
urlpatterns = [
    path('' , homepage,name = 'home'),
    # path('blogs/', blog_list, name='blog_list'),
    # path('blogs/new/', create_blog, name='create_blog'),
    # path('edit/<int:id>/', edit_blog, name='edit_blog'),   
    # path('delete/<int:id>/', delete_blog, name='delete_blog'), 
    path('viewcourse/',index),
    path('add&viewperson/',person_api),
    # path('add&viewblog/',Blog_api),
    path('api/',include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
