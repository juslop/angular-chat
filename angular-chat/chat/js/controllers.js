'use strict';

/* Controllers */

var chatControllers = angular.module('chatControllers', []);

chatControllers.controller('MainCtrl', ['$scope', '$location', 'Main', 'User',
  function ($scope, $location, Main, User) {
	$scope.rooms = Main.query({},function(){},function(data){
        console.log(data);
    });
	$scope.user = User.get();
    $location.path('#/lobby');
    $scope.sel = {sel:'lobby',id:''};
  }]);

chatControllers.controller('LobbyCtrl', ['$scope', 'Lobby',
  function ($scope, Lobby) {
    $scope.newest = Lobby.query();
  }]);

chatControllers.controller('MessageListCtrl', ['$scope', '$routeParams', '$timeout', 'Room', 'Message',
  function ($scope, $routeParams, $timeout, Room, Message) {
    $scope.comment = {cmt: "", curMsg: null, elem: null};
    $scope.scroll = {disabled: true};
    $scope.page = 1;
    $scope.pages = [];
	$scope.pages[0] = Room.query({roomId:$routeParams.roomId,
        pageId: $scope.page},
        function() {
            $timeout(function(){$scope.scroll.disabled = false;}, 1000);
        });
    $scope.loadMore = function() {
        $scope.page++;
        console.log('page now:' + $scope.page);
        var page = Room.query({roomId:$routeParams.roomId,
            pageId: $scope.page},
            function() {
                if (page.length) {
                    //works close enough for tutorial.
                    //if added dynamically posts handle paging offset
                    if ($scope.pages[0].length > 10) {
                        page = page.slice(
                            ($scope.pages[0].length % 10));
                    }
                    $scope.pages.push(page)
                    $timeout(function(){$scope.scroll.disabled = false;}, 1000);
                }
        });
    };
	$scope.newPost = function() {
        if ($scope.newMsg) {
            var dct = {
                content:$scope.newMsg,
                room:$scope.sel.id
            };
            var msg = new Message(dct);
            msg.$save({}, function(data) {
            	console.log(data);
                $scope.pages[0].unshift(data);
            }, function(errorData) {
            	console.log(errorData);
            });
            console.log('new message', $scope.newMsg);
            $scope.newMsg = "";
        }
	};
    $scope.close = function() {
        $scope.comment.elem.remove();
        $scope.comment.cmt = "";
        $scope.comment.curMsg = null;
    };
    $scope.newComment = function() {
		var dct = {content:$scope.comment.cmt, 
                room:$scope.sel.id,
				responseTo: $scope.comment.curMsg.id };
        if ($scope.comment.cmt) {
            var msg = new Message(dct);
            msg.$save({}, function(data) {
            	console.log('new page received: ', data);
                $scope.comment.curMsg.children.push(data);
                $scope.close();
            }, function(errorData) {
            	console.log(errorData);
                $scope.close();
            });
        }
    };
  }]);
