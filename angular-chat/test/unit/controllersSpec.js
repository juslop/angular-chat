'use strict';

/* jasmine specs for controllers go here */
describe('Angularchat controllers', function() {

  beforeEach(function(){
    this.addMatchers({
      toEqualData: function(expected) {
        return angular.equals(this.actual, expected);
      }
    });
  });

  beforeEach(module('chatApp'));
  beforeEach(module('chatServices'));

  describe('MainCtrl', function(){
    var scope, ctrl, $httpBackend;

    beforeEach(inject(function(_$httpBackend_, $rootScope, $controller) {
      $httpBackend = _$httpBackend_;
      $httpBackend.expectGET('/chat-api/main').
          respond([{id: 1, name: 'huu'}, {id: 2, name: 'haa'}]);
      $httpBackend.expectGET('/chat-api/user').
          respond({username: 'aaa', short_name: 'aaa', name: 'aaa bbb'});

      scope = $rootScope.$new();
      ctrl = $controller('MainCtrl', {$scope: scope});
    }));


    it('should create "rooms" model with 2 rooms fetched from xhr', function() {
      $httpBackend.flush();

      expect(scope.rooms).toEqualData(
          [{id: 1, name: 'huu'}, {id: 2, name: 'haa'}]);

      expect(scope.user).toEqualData(
          {username: 'aaa', short_name: 'aaa', name: 'aaa bbb'});

    });

  });

  describe('LobbytCtrl', function(){
    var scope, ctrl, $httpBackend;

    beforeEach(inject(function(_$httpBackend_, $rootScope, $controller) {
      $httpBackend = _$httpBackend_;
      $httpBackend.expectGET('/chat-api/lobby').
          respond([{name: 'huu', newest: [{id: 1, content: 'zzz', room: 1, writer: {name: 'zzz'}}]},
                   {name: 'haa', newest: [{id: 2, content: 'yyy', room: 2, writer: {name: 'zzz'}}]}
          ]);

      scope = $rootScope.$new();
      ctrl = $controller('LobbyCtrl', {$scope: scope});
    }));

    it('should create "newest" model with info fetched from xhr', function() {
      $httpBackend.flush();

      expect(scope.newest).toEqualData(
          [{name: 'huu', newest: [{id: 1, content: 'zzz', room: 1, writer: {name: 'zzz'}}]},
           {name: 'haa', newest: [{id: 2, content: 'yyy', room: 2, writer: {name: 'zzz'}}]}
          ]);
    });
  });

  describe('MessageListCtrl', function(){
    var scope, ctrl, $httpBackend, routeP;

    beforeEach(inject(function(_$httpBackend_, $rootScope, $controller) {
      $httpBackend = _$httpBackend_;
      scope = $rootScope.$new();
      routeP = {roomId: 1};
      ctrl = $controller('MessageListCtrl', {$scope: scope, $routeParams: routeP});
    }));

    it('should fetch messages for room as pages from xhr', function() {
      $httpBackend.expectGET('/chat-api/room/1/1/ ').
          respond([{id: '1', content: 'zzz', writer: {name: 'zzz'}, children: []},
                   {id: '2', content: 'yyy', writer: {name: 'zzz'}, children: []}
          ]);
      $httpBackend.flush();
      expect(scope.pages.length).toEqual(1);
      expect(scope.page).toEqual(1);

      expect(scope.pages[0]).toEqualData(
          [{id: '1', content: 'zzz', writer: {name: 'zzz'}, children: []},
           {id: '2', content: 'yyy', writer: {name: 'zzz'}, children: []}
          ]);

      $httpBackend.expectGET('/chat-api/room/1/2/ ').
          respond([{id: '3', content: 'zzz', writer: {name: 'zzz'}, children: []},
                   {id: '4', content: 'yyy', writer: {name: 'zzz'}, children: []}
          ]);
      scope.loadMore();
      $httpBackend.flush();
      scope.$apply();
      expect(scope.page).toEqual(2);
      expect(scope.pages.length).toEqual(2);
      expect(scope.pages[1]).toEqualData(
          [{id: '3', content: 'zzz', writer: {name: 'zzz'}, children: []},
           {id: '4', content: 'yyy', writer: {name: 'zzz'}, children: []}
          ]);

      $httpBackend.expectGET('/chat-api/room/1/3/ ').respond([]);
      scope.loadMore();
      $httpBackend.flush();
      scope.$apply();
      expect(scope.page).toEqual(3);
      expect(scope.pages.length).toEqual(2);
    });
  });


});
