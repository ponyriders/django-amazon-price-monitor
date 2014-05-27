PriceMonitorApp.controller('MainCtrl', function ($scope, $location) {
    $scope.URIS = window.URIS;
    $scope.isActive = function (route) {
        return route === $location.path();
    }
});
