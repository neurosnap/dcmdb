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
    url(r'^validateEmail', views.validateEmail, name='validateEmail'),
    url(r'^rm', views.rm, name='remove'),
    url(r'^removeUser', views.removeUser, name='removeUser'),
    url(r'^changePass', views.changePass, name='changePass'),
    url(r'^sendValidation', views.sendValidation, name='sendValidation'),
    url(r'^chngPassConfirm', views.chngPassConfirm, name='chngPassConfirm'),
    url(r'^sendPass', views.sendPass, name='sendPass'),
    url(r'^reqPass', views.reqPass, name='reqPass'),
    url(r'^updateInfo', views.updateInfo, name='updateInfo'),
    url(r'^saveInfo', views.saveInfo, name='saveInfo'),
)