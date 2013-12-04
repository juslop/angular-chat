'use strict';

/* jasmine specs for directives go here */

describe('Chat directives', function() {
  var $compile, $rootScope;

  beforeEach(module('chatApp', 'chat/partials/msg-node.html'));

  beforeEach(inject(function(_$compile_, _$rootScope_) {
    $compile = _$compile_;
    $rootScope = _$rootScope_;
  }));

  it("should display comment button field", function() {
      $rootScope.message = {id:1, content:'zzz', writer:{username: 'xxx'}, children: [], room: 1};
      $rootScope.counter = 1;
      $rootScope.newComment = function(){$rootScope.counter++;};
      $rootScope.current = {elem: null, cmt: "", curMsg: null};
      var html = angular.element('<ul><li>' +
          '<new-comment cnt="counter" current="comment" msg="message" cb="newComment"  ng-hide="cnt > 7"></new-comment>' +
           '</li><ul></ul></ul>');
      var elem = $compile(html)($rootScope);
      $rootScope.$digest();
      expect(elem.find('button').length).toEqual(1);
      //more dynamic fetures to e2e tests
  });

});

