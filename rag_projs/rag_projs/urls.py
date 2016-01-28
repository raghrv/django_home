from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url('^admin/$', admin.site.urls),
    url('^app1/', include('app1.urls')),
    url('^app1$/|^rag$', include('app1.urls')),
]
