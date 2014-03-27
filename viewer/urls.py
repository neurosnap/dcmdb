from django.conf.urls import patterns, url

from viewer import views

urlpatterns = patterns('',
	url(r'^image/(?P<dcm_uid>.*)$', views.image, name='image'),
	url(r'^study/(?P<dcm_uid>.*)$', views.study, name='study'),
	url(r'^series/(?P<dcm_uid>.*)$', views.series, name='series'),
)