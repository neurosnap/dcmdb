from django.conf.urls import patterns, url

from dcmupload import views

urlpatterns = patterns('',
    url(r'^$', views.dcmupload, name='dcmupload'),
    #url(r'^success/', views.success, name='success'),
    #url(r'^upload_dicom/', views.upload_dicom, name='upload_dicom'),
)
