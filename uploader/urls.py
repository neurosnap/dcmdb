from django.conf.urls import patterns, url

from uploader import views

urlpatterns = patterns('',
    url(r'^$', views.uploader, name='uploader'),
    url(r'^blank', views.blank, name='blank'),
    url(r'^handle_upload', views.handle_upload, name='handle_upload'),
)
