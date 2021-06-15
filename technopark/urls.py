"""technopark URL Configuration

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
from django.urls import path
from app import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index, name='index'),
    path('ask/',views.ask, name='ask'),
    path('answer/', views.answer, name='answer'),
    path('login/', views.login, name='login'),
    path('hot/', views.hot, name='hot'),
    path('register/', views.register, name='register'),
    path('settings/', views.settings, name='settings'),
    path('question/<int:pk>/', views.one_question, name='question'),
    path('tag/<str>/', views.tag_question, name='tag_question'),
    path('logout/', views.logout, name='logout'),
    path('qvote/', views.qvote, name='qvote'),
    path('avote/', views.avote, name='avote'),
    path('check/', views.check, name='check'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
