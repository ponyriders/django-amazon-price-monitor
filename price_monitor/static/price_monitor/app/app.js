'use strict';

var PriceMonitorApp = angular.module(
    'PriceMonitorApp', 
    [
        'ngCookies',
        'ngRoute',
        'ngResource'
    ]
);

PriceMonitorApp.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
        .when('/products', {
            controller: 'ProductsCtrl',
            templateUrl: 'partials/products.html'
        })
        .when('/subscriptions', {
            controller: 'SubscriptionCtrl',
            templateUrl: 'partials/subscriptions.html'
        })
        .otherwise({redirectTo: '/products'});
}]);

/**
 * Setting X-Requested-With header to enable Django to identify the request as asyncronous.
 */
//PriceMonitorApp.config('$httpProvider', function($httpProvider) {
//    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
//});

/* Controllers */
PriceMonitorApp.controller('MainCtrl', function ($scope, $location) {
    $scope.isActive = function (route) {
        return route === $location.path();
    }
});

/**
 * Adding value of CSRF cookie to request headers
 */
//PriceMonitorApp.run(function($http, $cookies) {
//    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
//    // Add the following two lines
//    $http.defaults.xsrfCookieName = 'csrftoken';
//    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
//});
