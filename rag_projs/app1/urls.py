from django.conf.urls import url
from . import views

urlpatterns = [
   url(r'ctime/$', views.get_time, name='dtime'),
   url(r'req/$', views.display, name='display'),
   url(r'^$', views.display, name='display'),
]
