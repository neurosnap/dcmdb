from django.conf.urls import patterns, url

from browse import views

urlpatterns = patterns('',
    url(r'^$', views.portal, name='portal'),
    url(r'^view/(.*)$', views.view, name='view'),
)
