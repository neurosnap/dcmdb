from django.conf.urls import patterns, url

from viewer import views

urlpatterns = patterns('',
	url(r'^viewer/(?P<dcm_uid>.*)$', views.view, name='dcmview'),
	url(r'^study/(?P<dcm_uid>.*)$', views.study, name='dcmstudy'),
	url(r'^series/(?P<dcm_uid>.*)$', views.series, name='dcmseries'),
)
#(?P<path>.*)$