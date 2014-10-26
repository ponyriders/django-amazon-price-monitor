PriceMonitorApp.controller('ProductDetailCtrl', function($scope, $routeParams, Product) {
    $scope.product = Product.get({asin: $routeParams.asin});
});
