from django.conf.urls import url
from django.contrib import admin
from webapp import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup')
]
