angular-chat
============

I created this single page chatroom app project to learn angular front end framework and django-rest framework.

This is a backend independent angular app. Requires a REST backend. One implemented with django-rest included, but it is easy to set-up backend with any REST capable web server. The required resources can be checked from resources.js and from django urls, models and serializers.

If you are familiar with both frameworks, code structure is pretty simple and self-explaining and easy to set-up.

If not familiar, I suggest you check the excellent angular tutorial first. Django has also great tutorials available.

Angular is awesome. I had used jQuery extensively before and Angular brings great structure to the front end.

Angular unit tests included require Node.js and Karma set up with proper modules. Angular tutortial tells how to install. Run in angular-chat folder: 
> karma start ./config/karma.conf.js


REST API setup
==============

Rest API app requires Django 1.5, Django rest framework 2.3.9, Python 2.7 and PIL.

Whole Django project is included, just clone this repo and go to django-chat folder and:
> python manage.py syncdb 

> python manage.py runserver

Angular files are static files from web-server point of view. REST API is called thru /chat-api/xxx urls with GET and POST methods.

Django app serves angular files when in debug mode. It uses standard Django authentication. Note: Django login and user account view are still in old school format in separate pages.

Create chat rooms and manage users with Django admin. 

Django rest unit tests included. Run as normal Django tests. Note tests.py requires Selenium.
> python manage.py test chat

E2e tests
==========

Django tests require python selenium webdriver and firefox browser.

Django livetestserver runs with included settings.py and can serve angular files.

E2e tests Angular modules using Selenium webdriver. No need to create separate e2e testing scheme for Angular using karma, which would have required extra backend work.
