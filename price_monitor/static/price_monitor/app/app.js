'use strict';

var PriceMonitorApp = angular.module(
    'PriceMonitorApp', 
    [
        'ngCookies',
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
PriceMonitorApp.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
});

/**
 * Adding value of CSRF cookie to request headers
 */
PriceMonitorApp.run(function($http, $cookies) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    // Add the following two lines
    $http.defaults.xsrfCookieName = 'csrftoken';
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
});
