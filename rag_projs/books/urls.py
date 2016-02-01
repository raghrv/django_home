from django.conf.urls import url
import views

urlpatterns = [
   url(r'^$', views.search_form, name='search_form'),
]
