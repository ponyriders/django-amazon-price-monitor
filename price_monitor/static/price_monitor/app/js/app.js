'use strict';

var PriceMonitorApp = angular.module(
    'PriceMonitorApp', 
    [
//        'ngCookies',
        'ngRoute',
        'ngResource',
        'ui.bootstrap',
        'djangoRESTResources',
        'ngResponsiveImages',
        'PriceMonitorServerConnector'
    ]
);

PriceMonitorApp.config(function ($routeProvider) {
    $routeProvider
        .when('/products', {
            controller: 'ProductListCtrl',
            templateUrl: SETTINGS.uris.static + 'price_monitor/app/partials/product-list.html'
        })
        .when('/products/:asin', {
            controller: 'ProductDetailCtrl',
            templateUrl: SETTINGS.uris.static + 'price_monitor/app/partials/product-detail.html'
        })
        .otherwise({redirectTo: '/products'});
});

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
