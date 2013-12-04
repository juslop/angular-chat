from django.conf.urls import patterns, include, url
from django.conf import settings
from chat.views import AccountView, login
import os

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', login, {'template_name':'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^account/$', AccountView.as_view(), name='account_view'),

    #rest API
    url(r'^chat-api/', include('chat.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    static = os.path.dirname(os.path.realpath(__file__)) + '/static/'
    media = os.path.dirname(os.path.realpath(__file__)) + '/../media/'
    chat = os.path.dirname(os.path.realpath(__file__)) + '/../../angular-chat/chat/'
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root' : static, 'show_indexes':True }),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root' : media, 'show_indexes':True }),
        (r'^chat/(?P<path>.*)$', 'django.views.static.serve', { 'document_root' : chat, 'show_indexes':True }),
    )
