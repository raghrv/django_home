from django.conf.urls import url
from . import views

urlpatterns = [
   url(r'^$', views.get_time, name='dtime'),
   url(r'^$', views.display, name='display'),
]
