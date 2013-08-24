from django.conf.urls import patterns, url

from dcmview import views

urlpatterns = patterns('',
	url(r'^(?P<dcm_id>\w+)$', views.dcmview, name='dcmview'),
	url(r'^series/(?P<series_id>\w+)$', views.dcmseries, name='dcmseries'),
)
