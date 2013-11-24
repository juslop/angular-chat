'use strict';

/* Directives */

var chatDirectives = angular.module('chatDirectives', []);

chatDirectives.directive('whenScrolled', ['$window', function($window) {
    return function(scope, elm, attr) {
        $window = angular.element($window);
        var handler = function() {
            if (!scope.scroll.disabled && ($window.scrollTop() +
                $window.height() > $(document).height() - 50)) {
                scope.scroll.disabled = true;
                scope.$apply(attr.whenScrolled);
            }
        };
        $window.on('scroll', handler);
        scope.$on('$destroy', function() {
          return $window.off('scroll', handler);
        });
    };
}]);

chatDirectives.directive("newComment", function($compile) {
    return {
        restrict: "E",
        scope: {
    		msg:"=",
    		current:"=",
    		cb:"="
		},
       	template: '<button><i class="icon-comment" ' +
       		'title="Click to comment."></i></button>',
        link: function(scope, element, attrs) {
            $(element).on('click', function () {
            	if (scope.current.curMsg !== scope.msg) {
            		if (scope.current.elem) {
                		scope.current.elem.remove();
            		}
                    var elem = $compile("<li><div class='row-fluid'>"+
                    		"<input type='text' class='span6 in-line' ng-model='current.cmt'>" +
                    		"<button class='btn in-line' ng-click='cb()'>Post" +
                    		"</button></div></li>")(scope);
                	$(element).closest('li').find('ul:first').prepend(elem);
            		scope.$apply(function() {
                    	scope.current.cmt = "";
                    	scope.current.elem = elem;
                    	scope.current.curMsg = scope.msg;
            		});
            	} else {
                    scope.current.elem.remove();
                    scope.current.cmt = "";
                    scope.current.curMsg = null;
                };
            });
        }
    };
});
