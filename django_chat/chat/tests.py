from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from chat.models import Room, Message
import json
import os
import unittest
import time
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CreateData(object):
    def createData(self):
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


class ChatTestCase(CreateData, APITestCase):
    def setUp(self):
        super(ChatTestCase, self).setUp()
        self.createData()
        ret = self.client.login(username='aaa', password='ccc')
        self.assertTrue(ret)


class SeleniumBase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(SeleniumBase, cls).setUpClass()
        CreateData().createData()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumBase, cls).tearDownClass()

class LoginMixin(object):
    def login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.selenium.find_element_by_name("username").send_keys('aaa')
        self.selenium.find_element_by_name("password").send_keys('ccc')
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
        WebDriverWait(self.selenium, 10).until(lambda driver: driver.find_elements_by_id('mblogger-container'))


####################
# Rest API unit tests
####################


class TestReadMain(ChatTestCase):
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


class TestPostMessage(ChatTestCase):
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


####################
# E2e tests
####################


class AngularBasicsTest(SeleniumBase, LoginMixin):
    def test_basics(self):
        self.login()
        #lobby view selected as active
	self.assertEqual(self.selenium.find_element_by_class_name('active').find_element_by_tag_name('a').text, 'lobby');
        #3 nav links set up
	self.assertEqual(len(self.selenium.find_element_by_class_name('nav').find_elements_by_tag_name('li')), 3);
        #2 room new msg tables
        self.assertEqual(len(self.selenium.find_elements_by_tag_name('tbody')), 2);
        #five newest messages
        self.assertEqual(len(self.selenium.find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')), 5);

        #move to a room
        self.selenium.find_element_by_class_name('nav').find_elements_by_tag_name('a')[1].click()
        WebDriverWait(self.selenium, 10).until(lambda driver: driver.find_elements_by_id('message-container'))
        time.sleep(0.5)
        #room a view selected as active
	self.assertEqual(self.selenium.find_element_by_class_name('active').find_element_by_tag_name('a').text, 'a');
        #right amount of messages visible
	self.assertEqual(len(self.selenium.find_elements_by_class_name('message-box')), 5);
        text = self.selenium.find_elements_by_class_name('message-box')[0].find_elements_by_tag_name('span')[1].text
        #correct text
	self.assertEqual(text, 'content 4');


class AngularChatTest(SeleniumBase, LoginMixin):
    def test_chatting(self):
        #test posting a comment to a message
        self.login()
        self.selenium.find_element_by_class_name('nav').find_elements_by_tag_name('a')[1].click()
        WebDriverWait(self.selenium, 10).until(lambda driver: driver.find_elements_by_id('message-container'))
        time.sleep(0.5)
        msg = self.selenium.find_element_by_id('message-container').find_elements_by_tag_name('li')[0]
        self.assertEqual(len(msg.find_elements_by_tag_name('input')), 0)
        msg.find_element_by_tag_name('button').click()
        time.sleep(0.5)
        self.assertEqual(len(msg.find_elements_by_tag_name('input')), 1)
        msg.find_element_by_tag_name('input').send_keys('zyx')
        msg.find_elements_by_tag_name('button')[1].click()
        time.sleep(0.5)
        #comment input removed
        self.assertEqual(len(msg.find_elements_by_tag_name('input')), 0)
        #new comment has been added to DOM
        self.assertEqual(len(msg.find_elements_by_tag_name('li')), 1)
        new_msg = msg.find_elements_by_class_name('message-box')[1]
        text = new_msg.find_elements_by_tag_name('span')[1].text
        #correct text shown
	self.assertEqual(text, 'zyx');
        #correct amount of messages visible
	self.assertEqual(len(self.selenium.find_elements_by_class_name('message-box')), 6);

