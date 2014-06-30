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
            
            $scope.productCount = $scope.subscriptions.length;
            $scope.currentPage = 1;
            $scope.maxPageCount = SETTINGS.pagination.maxPageCount;
            $scope.itemsPerPage = SETTINGS.pagination.itemsPerPage;
            $scope.paginationBoundaryLinks = SETTINGS.pagination.paginationBoundaryLinks; 
            $scope.paginationRotate = SETTINGS.pagination.paginationRotate;
            $scope.pagesTotal = 0;
        });
    });
});

//We already have a limitTo filter built-in to angular,
//let's make a startFrom filter
PriceMonitorApp.filter('startFrom', function() {
    return function(input, start) {
        start = parseInt(start); //parse to int
        return input.slice(start);
    }
});
