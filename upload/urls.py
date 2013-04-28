from django.conf.urls import patterns, url

from upload import views

urlpatterns = patterns('',
    url(r'^$', views.upload, name='upload'),
    url(r'^success/', views.success, name='success'),
    url(r'^upload_dicom/', views.upload_dicom, name='upload_dicom'),
)