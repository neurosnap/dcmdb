from django.conf.urls import patterns, url

from users import views

urlpatterns = patterns('',
    url(r'^$', views.portal, name='portal'),
    url(r'^login', views.login, name='login'),
    url(r'^register', views.register, name='register'),
)