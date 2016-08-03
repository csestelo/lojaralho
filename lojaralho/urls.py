from django.conf.urls import url
from django.contrib import admin
from webapp import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^welcome/$', views.welcome, name='welcome'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^admin/', admin.site.urls),
]
