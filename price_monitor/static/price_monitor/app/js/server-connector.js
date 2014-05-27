'use strict';

var PriceMonitorServerConnector = angular.module('PriceMonitorServerConnector', ['ngResource']);

PriceMonitorServerConnector.factory('Product', ['$resource', function($resource, URIS) {
    return $resource('/monitor/api/product-crud/', {'pk': '@pk'}, {
    });
}]);

PriceMonitorServerConnector.factory('Subscription', ['$resource', function($resource, URIS) {
    return $resource('/monitor/api/subscription-crud/', {'pk': '@pk'}, {
    });
}]);
