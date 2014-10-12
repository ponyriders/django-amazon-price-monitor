PriceMonitorApp.controller('ProductCtrl', function($scope, Product, Subscription) {
    // do the loading of products after subscriptions
    $scope.subscriptions = Subscription.query(function() {
        // do the combination of subscriptions and products after both are loaded
        var queryProducts = Product.query(function() {
            var sortedProducts = {};
            
            angular.forEach(queryProducts, function(product) {
                sortedProducts[product.asin] = product;
                sortedProducts[product.asin].sparklineUrl = SETTINGS.uris.sparkline.replace(':asin', product.asin);
            });
            
            angular.forEach($scope.subscriptions, function(subscription) {
                subscription.fetchedProduct = sortedProducts[subscription.product];
            });

            $scope.subscriptionCount = $scope.subscriptions.length;
            $scope.currentPage = 1;
            $scope.maxPageCount = SETTINGS.pagination.maxPageCount;
            $scope.itemsPerPage = SETTINGS.pagination.itemsPerPage;
            $scope.paginationBoundaryLinks = SETTINGS.pagination.paginationBoundaryLinks; 
            $scope.paginationRotate = SETTINGS.pagination.paginationRotate;
            $scope.pagesTotal = 0;
        });
    });
});
