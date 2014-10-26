PriceMonitorApp.controller('ProductListCtrl', function($scope, Product) {
    $scope.products = Product.query(function() {
        $scope.productCount = $scope.products.length;
        $scope.currentPage = 1;
        $scope.maxPageCount = SETTINGS.pagination.maxPageCount;
        $scope.itemsPerPage = SETTINGS.pagination.itemsPerPage;
        $scope.paginationBoundaryLinks = SETTINGS.pagination.paginationBoundaryLinks; 
        $scope.paginationRotate = SETTINGS.pagination.paginationRotate;
        $scope.pagesTotal = 0;
    });
});
