PriceMonitorApp.controller('ProductCtrl', function($scope, Product, Subscription) {
    // do the loading of products after subscriptions
    $scope.subscriptions = Subscription.query(function() {
        // do the combination of subscriptions and products after both are loaded
        var queryProducts = Product.query(function() {
            var sortedProducts = {};
            
            angular.forEach(queryProducts, function(product) {
                sortedProducts[product.asin] = product;
            });
            
            angular.forEach($scope.subscriptions, function(subscription) {
                subscription.fetchedProduct = sortedProducts[subscription.product];
            });
        });
    });
});
