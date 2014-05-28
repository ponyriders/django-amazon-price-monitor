PriceMonitorApp.controller('ProductCtrl', function($scope, Product, Subscription) {
    $scope.subscriptions = Subscription.query();
});
