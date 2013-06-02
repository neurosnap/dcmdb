from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#import settings
from django.contrib import admin
import socket
from django.conf import settings

admin.autodiscover()

from main import views as main_views

host = socket.gethostname()

#see if it's production
if host == "dcmdb.org":

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
        #url(r'^$', main_views.under_construction, name = "under_construction",
	url(r'^$', include('main.urls')),
        url(r'^main/', include('main.urls')),
        url(r'^users/', include('users.urls')),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^upload/', include('upload.urls')),
        url(r'^browse/', include('browse.urls')),
        url(r'^dcmview/', include('dcmview.urls')),
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, }),
    )

urlpatterns += staticfiles_urlpatterns()
