'use strict';

var PriceMonitorServerConnector = angular.module('PriceMonitorServerConnector', ['ngResource', 'djangoRESTResources']);

PriceMonitorServerConnector.factory('Product', ['djResource', function(djResource) {
    return djResource(SETTINGS.uris.product, {'asin': '@asin'}, {
    });
}]);

PriceMonitorServerConnector.factory('Subscription', ['djResource', 'Product', function(djResource) {
    return djResource(SETTINGS.uris.subscription, {'public_id': '@public_id'}, {});
}]);
