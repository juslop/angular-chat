'use strict';

/* App Module */

var chatApp = angular.module('chatApp', [
  'ngRoute',
  'chatControllers',
  'chatServices',
  'chatDirectives',
  'chatFilters',
  'chatErrors'
]);

chatApp.config(['$routeProvider', '$locationProvider',
  function($routeProvider, $locationProvider) {
    $routeProvider.
      when('/lobby', {
        templateUrl: 'partials/lobby.html',
        controller: 'LobbyCtrl'
      }).
      when('/room/:roomId/:pageId?', {
        templateUrl: 'partials/room.html',
        controller: 'MessageListCtrl'
      }).
      otherwise({
        redirectTo: '/lobby'
      });
  }]);

//django xsite forgery protection
chatApp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'; 
  }
]);
