module.exports = function(config){
    config.set({
    basePath : '../',

    port: 9877,

    files : [
      'chat/lib/angular/angular.js',
      'chat/lib/angular/angular-*.js',
      'chat/lib/jquery/jquery-*.js',
      'test/lib/angular/angular-mocks.js',
      'chat/js/*.js',
      'chat/partials/*.html',
      'test/unit/*.js'
    ],

    preprocessors: {
      'chat/partials/*.html': ['ng-html2js']
    },

    exclude: ['chat/lib/angular/angular-scenario.js'],

    autoWatch : true,

    frameworks: ['jasmine'],

    browsers : ['Firefox'],

    plugins : [
      'karma-junit-reporter',
      'karma-chrome-launcher',
      //'karma-safari-launcher',
      'karma-firefox-launcher',
      'karma-jasmine',
      'karma-ng-html2js-preprocessor'
    ],

    junitReporter : {
      outputFile: 'unit.xml',
      suite: 'unit'
    }

})}
