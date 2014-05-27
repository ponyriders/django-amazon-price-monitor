'use strict';

var PriceMonitorServerConnector = angular.module('PriceMonitorServerConnector', ['ngResource']);

PriceMonitorServerConnector.factory('Product', ['$resource', function($resource) {
    return $resource(SETTINGS.uris.product, {'pk': '@pk'}, {
    });
}]);

PriceMonitorServerConnector.factory('Subscription', ['$resource', function($resource, URIS) {
    return $resource(SETTINGS.uris.subscription, {'pk': '@pk'}, {
    });
}]);
