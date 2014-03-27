from django.conf.urls import patterns, url
from downloader import views

urlpatterns = patterns('',
	url(r'^zip/dcm/(?P<uid>.*)$', views.zip_dcm, name='dlzipdcm'),
	url(r'^zip/series/(?P<uid>.*)$', views.zip_series, name='dlzipseries'),
	url(r'^zip/study/(?P<uid>.*)$', views.zip_study, name='dlzipstudy'),
	#url(r'^dcm/json/(?P<uid>.*)$', views.json_dcm, name='dljsondcm'),
	#url(r'^series/json/(?P<uid>.*)$', views.json_series, name='dljsonseries'),
	#url(r'^study/json/(?P<uid>.*)$', views.json_study, name='dljsonstudy'),
)