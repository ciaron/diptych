from django.conf.urls import patterns, url
from django.conf import settings

from images import views

urlpatterns = patterns('',
    # e.g. /images/
    url(r'^$', views.index, name='index'),
    # e.g. /images/2010/12/31
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)$', views.detail, name='detail')
)

