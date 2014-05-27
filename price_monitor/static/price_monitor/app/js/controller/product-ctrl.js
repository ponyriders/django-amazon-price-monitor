PriceMonitorApp.controller('ProductCtrl', function($scope, Product, Subscription) {
    $scope.subscriptions = Subscription.query();
    $scope.products = {};
    
    $scope.getProduct = function(productId) {
        if ($scope.products[productId]) {
            return $scope.products[productId];
        } else {
            $scope.products[productId] = Product.get({'pk': productId});
            return $scope.products[productId];
        }
    };
});
