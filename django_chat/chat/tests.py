from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from chat.models import Room, Message
import json
import os


class ChatTestCase(APITestCase):
    def setUp(self):
        super(ChatTestCase, self).setUp()
        u = User.objects.create_user(username='aaa', first_name='aa',
                                 last_name='bb', password='ccc')
        u2 = User.objects.create_user(username='bbb', first_name='bb',
                                 last_name='bb', password='ccc')
        r = Room(name='a', createdBy=u)
        r.save()
        Room(name='b', createdBy=u).save()
        for i in range(5):
            Message(content='content ' + str(i), writer = u if i%2 else u2,
                    room = r).save()
        ret = self.client.login(username='aaa', password='ccc')
        self.assertTrue(ret)



class ReadMain(ChatTestCase):
    def test_room_view(self):
        response = self.client.get('/chat-api/room/1/1/', format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0]['content'], 'content 4')
        self.assertEqual(data[4]['content'], 'content 0')
        self.assertEqual(data[1]['writer']['name'], u'aa bb')
        self.assertEqual(data[1]['writer']['img'], '/chat/img/anonymous.png')
        response = self.client.get('/chat-api/room/2/', format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data, [])
        response = self.client.get('/chat-api/room/1/2/', format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data, [])

    def test_user_view(self):
        response = self.client.get('/chat-api/user', format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['short_name'], 'aa')

    def test_main(self):
        response = self.client.get('/chat-api/main', format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)


class PostMessage(ChatTestCase):
    def test_comment(self):
        response = self.client.get('/chat-api/room/1/1/', format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        response = self.client.post('/chat-api/message', {'content': 'abcdef', 'responseTo': '1', 'room': '1'})
        data = json.loads(response.content)
        self.assertEqual(data['content'], u'abcdef')
        self.assertEqual(data['responseTo'], 1)
        response = self.client.get('/chat-api/room/1/1/', format='json')
        self.assertEqual(response.status_code, 200)
        data2 = json.loads(response.content)
        self.assertEqual(len(data2[4]['children']), 1)
        child = data2[4]['children'][0]
        for key in child.keys():
            self.assertEqual(child[key], data[key])


class TestUserExtra(ChatTestCase):
    def test_user_extra(self):
        path = os.path.dirname(os.path.realpath(__file__)) + '/../../angular-chat/chat/'
        with open(path + 'img/anonymous.png') as fp:
            response = self.client.post('/account/', {'name': 'empty.img', 'attachment': fp})
        self.assertEqual(response.status_code, 302)
