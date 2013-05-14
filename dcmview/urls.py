from django.conf.urls import patterns, url

from dcmview import views

urlpatterns = patterns('',
	url(r'^$', views.dcmview, name='dcmview'),
)
