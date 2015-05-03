PriceMonitorApp.controller('ProductDetailCtrl', function ($scope, $routeParams, $location, $modal, Product) {
    $scope.product = Product.get(
        {asin: $routeParams.asin},
        // called when product can be retrieved
        function () {
            $scope.open = function () {
                var modalInstance = $modal.open({
                    templateUrl: SETTINGS.uris.static + '/price_monitor/app/partials/product-delete.html',
                    controller: 'ProductDeleteCtrl',
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
        },
        // called if asin is not found
        function () {
            $location.path('#products');
        }
    );


});
