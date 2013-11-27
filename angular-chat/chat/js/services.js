'use strict';

/* Services */
var chatServices = angular.module('chatServices', ['ngResource']);

/* note: the space in end of url keeps trailing slash, required by Django */
chatServices.factory('Room', ['$resource', function($resource){
    return $resource('/chat-api/room/:roomId/:pageId/ ',{pageId:'@pageId'}, {});
}]);

chatServices.factory('Message', ['$resource', function($resource){
	return $resource('/chat-api/message/:messageId',
		{
			messageId:'@id'
		});
}]);

chatServices.factory('Main', ['$resource', function($resource){
	return $resource('/chat-api/main/',
		{});
}]);

chatServices.factory('Lobby', ['$resource', function($resource){
	return $resource('/chat-api/lobby/',
		{});
}]);

chatServices.factory('User', ['$resource', function($resource){
	return $resource('/chat-api/user',
		{});
}]);

//http://blog.tomaka17.com/2012/12/random-tricks-when-using-angularjs/

var chatErrors = angular
    .module('chatErrors', [])
    .config(function($provide, $httpProvider, $compileProvider) {
        var elementsList = $();

        var showMessage = function(content, cl, time) {
            $('<div/>')
                .addClass('message')
                .addClass('alert')
                .addClass(cl)
                .hide()
                .fadeIn('fast')
                .delay(time)
                .fadeOut('fast', function() { $(this).remove(); })
                .on('click', function() { $(this).remove(); })
                .appendTo(elementsList)
                .text(content);
        };

        $httpProvider.responseInterceptors.push(function($timeout, $q) {
            return function(promise) {
                return promise.then(function(successResponse) {
                    if (successResponse.config.method.toUpperCase() != 'GET')
                        showMessage('Success', 'alert-success', 5000);
                    return successResponse;

                }, function(errorResponse) {
                    switch (errorResponse.status) {
                        case 401:
                            showMessage('Wrong usename or password', 'alert-error', 20000);
                            break;
                        case 403:
                            showMessage('You are not logged in or do not have permission for the data', 'alert-error', 20000);
                            break;
                        case 500:
                            showMessage('Server internal error: ' + errorResponse.data.slice(0,200), 'alert-error', 20000);
                            break;
                        default:
                            showMessage('Failed to contact server ' + errorResponse.status + ': ' + errorResponse.data.slice(0,200), 'alert-error', 20000);
                    }
                    return $q.reject(errorResponse);
                });
            };
        });

        $compileProvider.directive('appMessages', function() {
            var directiveDefinitionObject = {
                link: function(scope, element, attrs) { elementsList.push($(element)); }
            };
            return directiveDefinitionObject;
        });
    });
