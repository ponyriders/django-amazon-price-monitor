'use strict';

var PriceMonitorApp = angular.module(
    'PriceMonitorApp', 
    [
//        'ngCookies',
        'ngRoute',
        'ngResource',
        'ui.bootstrap',
        'PriceMonitorServerConnector'
    ]
);

PriceMonitorApp.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
        .when('/products', {
            controller: 'ProductCtrl',
            templateUrl: '/static/price_monitor/app/partials/products.html'
        })
        .otherwise({redirectTo: '/products'});
}]);

/**
 * Setting X-Requested-With header to enable Django to identify the request as asyncronous.
 */
//PriceMonitorApp.config('$httpProvider', function($httpProvider) {
//    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
//});

/**
 * Adding value of CSRF cookie to request headers
 */
//PriceMonitorApp.run(function($http, $cookies) {
//    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
//    // Add the following two lines
//    $http.defaults.xsrfCookieName = 'csrftoken';
//    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
//});
