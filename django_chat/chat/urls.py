from django.conf.urls import patterns, include, url
from django.conf import settings
from views import RoomView, UserView, LobbyView, MessageView, MainView

urlpatterns = patterns('',
    url(r'^room/(?P<id>\d+)/$', RoomView.as_view()),
    url(r'^room/(?P<id>\d+)/(?P<page>\d+)/$', RoomView.as_view()),
    url(r'^user$', UserView.as_view()),
    url(r'^lobby$', LobbyView.as_view()),
    url(r'^main$', MainView.as_view()),
    url(r'^message$', MessageView.as_view()),
)
