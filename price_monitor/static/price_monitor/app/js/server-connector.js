'use strict';

var PriceMonitorServerConnector = angular.module('PriceMonitorServerConnector', ['ngResource']);

PriceMonitorServerConnector.factory('Product', ['$resource', function($resource) {
    return $resource(SETTINGS.uris.product, {'pk': '@pk'}, {
    });
}]);

PriceMonitorServerConnector.factory('Subscription', ['$resource', 'Product', function($resource, Product) {
    var Subscription = $resource(SETTINGS.uris.subscription, {'pk': '@pk'}, {});
    Subscription._fetched_product = null;
    Subscription.prototype.get_product = function() {
        if (this._fetched_product == null) {
            this._fetched_product = Product.get({'pk': this.product});
        }
        return this._fetched_product;
    }
    return Subscription;
}]);
