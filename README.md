angular-chat
============

I created this chatroom app project to learn angular front end framework and django-rest framework.

This is a backend independent angular app. Requires a REST backend. One implemented with django-rest included, but it is easy to set-up backend with any REST capable web server. The required resources can be checked from resources.js and from django urls, models and serializers.

If you are familiar with both frameworks, code structure is pretty simple and self-explaining and easy to set-up.

If not familiar, I suggest you check the excellent angular tutorial first. Django has also great tutorials available.

I became Angular fan through this project. I had used jQuery extensively before and Angular brings great structure to the front end.

I had issues with Karma set up in my Mac so module tests are missing,  sorry for that.

REST API setup
==============

Angular files are static files from web-server point of view. REST API is called thru /chat-api/xxx urls with GET and POST methods.

Django app serves angular files when in debug mode. It uses standard Django authentication. Create chat rooms and manage users with Django admin.

