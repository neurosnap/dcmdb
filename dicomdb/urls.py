from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#import settings
from django.contrib import admin
import socket
from django.conf import settings

admin.autodiscover()

from main import views as main_views

host = socket.gethostname()
#host = "dev"
#host = "dcmdb.org"
#see if it's production
if host == "dcmdb.org":

    #uc = under construction
    urlpatterns = patterns('',
        url(r'^$', main_views.uc, name = "uc"),
        url(r'^main/about/', main_views.about_uc, name = "about_uc"),
        url(r'^main/dicom/', main_views.dicom_uc, name="dicom_uc"),
        url(r'^main/tos/', main_views.tos_uc, name="tos_uc"),
    )

else:

    urlpatterns = patterns('',
	    url(r'^$', include('main.urls')),
        url(r'^main/', include('main.urls')),
        url(r'^users/', include('users.urls')),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^dcmview/', include('dcmview.urls')),
        url(r'^dcmupload/', include('dcmupload.urls')),
        url(r'^down/', include('down.urls')),
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, }),
    )

urlpatterns += staticfiles_urlpatterns()
