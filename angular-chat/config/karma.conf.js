module.exports = function(config){
    config.set({
    basePath : '../',

    files : [
      'chat/lib/angular/angular.js',
      'chat/lib/angular/angular-*.js',
      'chat/lib/jquery/jquery-*.js',
      'test/lib/angular/angular-mocks.js',
      'chat/js/*.js',
      'test/unit/*.js'
    ],

    exclude: ['chat/lib/angular/angular-scenario.js'],

    autoWatch : true,

    frameworks: ['jasmine'],

    browsers : ['Firefox'],

    plugins : [
      'karma-junit-reporter',
      'karma-chrome-launcher',
      //'karma-safari-launcher',
      'karma-firefox-launcher',
      'karma-jasmine'
    ],

    junitReporter : {
      outputFile: 'unit.xml',
      suite: 'unit'
    }

})}
