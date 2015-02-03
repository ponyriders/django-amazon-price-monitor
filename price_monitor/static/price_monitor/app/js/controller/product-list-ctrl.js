PriceMonitorApp.controller('ProductListCtrl', function($scope, Product) {
    $scope.products = Product.query(function() {
        $scope.productCount = $scope.products.length;
        $scope.currentPage = 1;
        $scope.maxPageCount = SETTINGS.pagination.maxPageCount;
        $scope.itemsPerPage = SETTINGS.pagination.itemsPerPage;
        $scope.paginationBoundaryLinks = SETTINGS.pagination.paginationBoundaryLinks; 
        $scope.paginationRotate = SETTINGS.pagination.paginationRotate;
        $scope.pagesTotal = 0;

        var emptyProduct = {
            asin: null,
            subscription_set: [{
                price_limit: null,
                email_notification: {
                    email: null
                }
            }]
        };

        $scope.newProducts = [emptyProduct];

        $scope.addNewProduct = function() {
            $scope.newProducts.push(emptyProduct);
        }

        $scope.removeFormLine = function(product) {
            var index = $scope.newProducts.indexOf(product);
            if (index != -1) {
                $scope.newProducts.splice(index, 1);
            }
        }

        $scope.saveNewProducts = function() {
            angular.forEach($scope.newProducts, function(newProduct) {
                Product.save(newProduct);
            });
        }
    });
});
