from django.conf.urls import url
from django.contrib import admin
from webapp import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
]
