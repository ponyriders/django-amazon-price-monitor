PriceMonitorApp.controller('ProductDeleteCtrl', function ($scope, $modalInstance, product) {
    $scope.product = product;
    $scope.ok = function () {
        $scope.product.$delete();
        $modalInstance.close();
    };
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});
