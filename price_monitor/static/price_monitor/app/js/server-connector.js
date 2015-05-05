'use strict';

var PriceMonitorServerConnector = angular.module('PriceMonitorServerConnector', ['ngResource', 'djangoRESTResources']);

PriceMonitorServerConnector.factory('Product', ['djResource', function(djResource) {
    var Product = djResource(SETTINGS.uris.product, {'asin': '@asin'}, {
        'update': {
            method:'PUT'
        }
    });
    
    Product.prototype.getSparklineUrl = function() {
        return SETTINGS.uris.sparkline.replace(':asin', this.asin);
    };
    
    Product.prototype.getChartUrl = function(size) {
        if (SETTINGS.uris.chart[size]) {
            return SETTINGS.uris.chart[size].replace(':asin', this.asin)
        }
        return '';
    };

    Product.prototype.removeSubscription = function(index) {
        this.subscription_set.splice(index, 1);
    };
    
    return Product;
}]);

PriceMonitorServerConnector.factory('Subscription', ['djResource', 'Product', function(djResource) {
    return djResource(SETTINGS.uris.subscription, {'public_id': '@public_id'}, {});
}]);

PriceMonitorServerConnector.factory('Price', ['djResource', function(djResource) {
    return djResource(SETTINGS.uris.price, {'asin': '@asin'}, {});
}]);
