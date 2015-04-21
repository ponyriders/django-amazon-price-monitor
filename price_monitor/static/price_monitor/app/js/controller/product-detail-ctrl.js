PriceMonitorApp.controller('ProductDetailCtrl', function ($scope, $routeParams, $location, $modal, Product) {
    $scope.product = Product.get({asin: $routeParams.asin});

    $scope.open = function () {

        var modalInstance = $modal.open({
            templateUrl: SETTINGS.uris.static + '/price_monitor/app/partials/product-delete.html',
            controller: 'ProductDeleteCtrl',
            size: 'sm',
            resolve: {
                product: function () {
                    return $scope.product;
                }
            }
        });

        modalInstance.result.then(function () {
            $location.path('#products');
        });
    };
});
