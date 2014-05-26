'use strict';

var PriceMonitorServerConnector = angular.module('PriceMonitorServerConnector', ['ngResource']);

PriceMonitorServerConnector.factory('Product', ['$resource', function($resource) {
    return $resource(URIS['product'], {'pk': '@pk'}, {
    });
}]);

PriceMonitorServerConnector.factory('Subscription', ['$resource', function($resource) {
    return $resource(URIS['subscription'], {'pk': '@pk'}, {
    });
}]);
