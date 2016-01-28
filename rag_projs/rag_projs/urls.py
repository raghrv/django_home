from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url('^admin/', include(admin.site.urls)),
    url('^app1/', include('app1.urls')),
    url('^app1$/|^rag$', include('app1.urls')),
]
