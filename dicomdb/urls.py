from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#import settings
from django.contrib import admin
import socket

admin.autodiscover()

from main import views as main_views

host = socket.gethostname()

#see if it's production
if host == "dcmdb.org" or host == "72.240.79.150":

    urlpatterns = patterns('',
        url(r'^$', main_views.under_construction, name = "under_construction"),
    )

else:

    urlpatterns = patterns('',
        # Examples:
        # url(r'^$', 'dicomdb.views.home', name='home'),
        # url(r'^blog/', include('blog.urls')),
        #(r'^dicoms/(?P<path>.*)$', 'django.views.static.serve',
    	#    {'document_root': settings.MEDIA_ROOT}),
        url(r'^$', include('main.urls')),
        url(r'^main/', include('main.urls')),
        url(r'^users/', include('users.urls')),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^upload/', include('upload.urls')),
        url(r'^browse/', include('browse.urls')),
        url(r'^dcmview/', include('dcmview.urls')),
    )

urlpatterns += staticfiles_urlpatterns()
