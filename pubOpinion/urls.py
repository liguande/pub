"""pubOpinion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from eduOpinion import views as eduOpinion_views


urlpatterns = [
    url(r'^$', eduOpinion_views.home, name='home'),
    url(r'^createUser/$',eduOpinion_views.createUser, name="createUser"),
    url(r'^login/$',eduOpinion_views.login,name="login"),
    url(r'^logOut/$',eduOpinion_views.logOut,name="logOut"),
    url(r'^index/$', eduOpinion_views.index, name='index'),
    url(r'^setting/$',eduOpinion_views.setting,name="setting"),
    url(r'^addObject/$',eduOpinion_views.addObject,name="addObject"),
    url(r'^data/$',eduOpinion_views.data,name="data"),
    url(r'^admin/', admin.site.urls),
]
