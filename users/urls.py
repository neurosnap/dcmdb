from django.conf.urls import patterns, url

from users import views

urlpatterns = patterns('',
    url(r'^$', views.portal, name='portal'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^checkLogin', views.checkLogin, name='checkLogin'),
    url(r'^checkUniqueUser', views.checkUniqueUser, name='checkUniqueUser'),
    url(r'^checkUniqueEmail', views.checkUniqueEmail, name='checkUniqueEmail'),
    url(r'^register', views.register, name='register'),
    url(r'^createUser', views.createUser, name='createUser'),
    url(r'^removeUser', views.removeUser, name='removeUser'),
)