from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings
from main import views as main_views
admin.autodiscover()

if settings.UNDER_CONSTRUCTION:

    urlpatterns = patterns('',
        url(r'^$', main_views.uc, name = "uc"),
        url(r'^main/about/', main_views.about_uc, name = "about_uc"),
        url(r'^main/dicom/', main_views.dicom_uc, name="dicom_uc"),
        url(r'^main/tos/', main_views.tos_uc, name="tos_uc"),
        url(r'^main/privacy/', main_views.privacy_uc, name="privacy_uc"),
    )

else:

    urlpatterns = patterns('',
	    url(r'^$', include('main.urls')),
        url(r'^main/', include('main.urls')),
        url(r'^users/', include('users.urls')),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^viewer/', include('viewer.urls')),
        url(r'^uploader/', include('uploader.urls')),
        url(r'^down/', include('down.urls')),
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, }),
    )

urlpatterns += staticfiles_urlpatterns()
