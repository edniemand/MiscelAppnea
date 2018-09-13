"""MiscelAppnea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url,include
from django.urls import path
from . import views
from django.contrib.auth import views as AuthViews

urlpatterns = [
    url(r"^index/$", views.Index.as_view(), name="index"),
    url(r"^home/$", views.Home.as_view(), name="home"),
    url(r"^charts/$", views.Charts.as_view(), name="charts"),
    url(r'^$', AuthViews.login, name='login'),
    url(r'^logout/$', AuthViews.logout, name='logout', kwargs={'next_page': 'login'}),
    url(r'^registration/$',views.registration,name='registration'),
    url(r'^reciente/$',views.Reciente.as_view(),name='reciente'),
    url("",include('nominas_app.urls')),
    url("",include('comedor_app.urls')),
    url("",include('usuarios_app.urls')),
    url('admin/', admin.site.urls),
]
