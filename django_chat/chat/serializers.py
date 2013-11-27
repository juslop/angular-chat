#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.fields import Field
from chat.models import Room, Message
from django.contrib.auth.models import User

class UserHandler(object):
    def full_name(self, obj):
        return obj.get_full_name() or obj.username
    
    def get_img_url(self, obj):
        try:
            ue = obj.userextra
            if ue.thumbnail:
                return obj.userextra.thumbnail.url
        except:
            pass
        #move to settings
        return '/chat/img/anonymous.png'

    def short_name(self, obj):
        try:
            n = obj.get_short_name()
        except:
            n = None
        return n or obj.username


class LobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('name',)


class MsgUserSerializer(UserHandler, serializers.Serializer):
    name = serializers.SerializerMethodField('full_name')
    img = serializers.SerializerMethodField('get_img_url')
    class Meta:
        model = User
        fields = ('name', 'img')


class UserSerializer(UserHandler, serializers.ModelSerializer):
    name = serializers.SerializerMethodField('full_name')
    short_name = serializers.SerializerMethodField('short_name')
    img = serializers.SerializerMethodField('get_img_url')

    class Meta:
        model = User
        fields = ('username', 'name', 'short_name', 'img')

class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name')

class RoomSerializer(serializers.ModelSerializer):
    writer = MsgUserSerializer()
    class Meta:
        model = Message
        fields = ('id', 'content', 'writer')

class MessageSerializer(serializers.ModelSerializer):
    writer = MsgUserSerializer()
    class Meta:
        model = Message
        fields = ('id', 'content', 'responseTo', 'room', 'writer')
