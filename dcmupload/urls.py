from django.conf.urls import patterns, url

from dcmupload import views

urlpatterns = patterns('',
    url(r'^$', views.dcmupload, name='dcmupload'),
    url(r'^signature', views.handle_s3, name="s3_signee"),
    url(r'^delete', views.handle_s3, name='s3_delete'),
    url(r'^success', views.success_redirect_endpoint, name="s3_succes_endpoint"),
    url(r'^blank', views.blank, name='blank'),
    #url(r'^success/', views.success, name='success'),
    #url(r'^upload_dicom/', views.upload_dicom, name='upload_dicom'),
)
