#!/usr/bin/env python
# -*- coding: utf-8 -*-
from chat.models import Message, Room, UserExtra
from chat.forms import AccountForm
from chat.serializers import RoomSerializer, LobbySerializer, UserSerializer, MessageSerializer, RoomsSerializer
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as contrib_login
from django.conf import settings


def login(request, **kwargs):
    if request.user.is_authenticated():
	print 'kusipaska'
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return contrib_login(request, **kwargs)

class LoginRequired(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequired, self).dispatch(*args,**kwargs)


class AuthView(object):
    permission_classes = (IsAuthenticated, )


class RoomView(AuthView, views.APIView):
    def message_tree(self, qs):
        for msg in qs:
            ser = RoomSerializer(msg)
            data = ser.data
            data['children'] = self.message_tree(msg.responses.all())
            yield data

    def get(self, request, format=None, id=1, page="1"):
        room = get_object_or_404(Room, pk=int(id))
        page = int(page)
        queryset = Message.objects.filter(room=room, responseTo=None).order_by('-id')
        paginator = Paginator(queryset, 10, allow_empty_first_page=True)
        try:
            roots = paginator.page(page)
        except EmptyPage:
            roots = []
        data = self.message_tree(roots)
        return Response(data)


class UserView(AuthView, views.APIView):
    def get(self, request, format=None):
        data = UserSerializer(request.user).data
        return Response(data)


class LobbyView(AuthView, views.APIView):
    def populate(self, qs):
        for room in qs:
            ser = LobbySerializer(room)
            data = ser.data
            newest = MessageSerializer(room.message_set.order_by('-created')[0:5], many=True)
            data['newest'] = newest.data
            yield data

    def get(self, request, format=None):
        result = []
        data = self.populate(Room.objects.all())
        return Response(data)


class MessageView(AuthView, views.APIView):
    def post(self, request, format=None):
        data = request.DATA
        if data.get('id'):
            #no modification of posts allowed
            return HttpResponseForbidden()
        ser = MessageSerializer(data=data, partial=True)
        if ser.is_valid():
            ser.object.writer = request.user
            ser.save()
            ser.data['children'] = []
        return Response(ser.data)


class MainView(AuthView, views.APIView):
    def get(self, request, format=None):
        ser = RoomsSerializer(Room.objects.all(), many=True)
        return Response(ser.data)


class AccountView(LoginRequired, FormView):
    template_name="user-settings.html"
    form_class = AccountForm
    success_url = '/chat/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(AccountView, self).get_context_data(**kwargs)
        try:
            context['img'] = self.request.user.userextra.img
        except:
            pass
        return context

    def form_valid(self, form):
        ret = super(AccountView, self).form_valid(form)
        if ret.status_code == 302:
            if not form.instance.pk:
                form.instance.user = self.request.user
            form.save()
        return ret
