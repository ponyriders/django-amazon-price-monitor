PriceMonitorApp.controller('ProductListCtrl', function($scope, $modal, Product, EmailNotification) {
    $scope.products = Product.query(function() {
        $scope.emailNotifications = EmailNotification.query(function() {
            $scope.productCount = $scope.products.length;
            $scope.currentPage = 1;
            $scope.maxPageCount = SETTINGS.pagination.maxPageCount;
            $scope.itemsPerPage = SETTINGS.pagination.itemsPerPage;
            $scope.paginationBoundaryLinks = SETTINGS.pagination.paginationBoundaryLinks;
            $scope.paginationRotate = SETTINGS.pagination.paginationRotate;
            $scope.pagesTotal = 0;
            $scope.siteName = SETTINGS.siteName;

            var emptyProduct = {
                asin: null,
                subscription_set: [{
                    price_limit: null,
                    email_notification: {
                        email: $scope.emailNotifications.length > 0 ? $scope.emailNotifications[0].email : ''
                    }
                }]
            };

            $scope.newProducts = [angular.copy(emptyProduct)];

            $scope.addNewProduct = function() {
                $scope.newProducts.push(emptyProduct);
            };

            $scope.removeFormLine = function(product) {
                var index = $scope.newProducts.indexOf(product);
                if (index != -1) {
                    $scope.newProducts.splice(index, 1);
                }
            };

            $scope.saveNewProducts = function() {
                angular.forEach($scope.newProducts, function(newProduct) {
                    Product.save(newProduct, function() {
                        $scope.products = Product.query();
                        $scope.newProducts = [angular.copy(emptyProduct)];
                    });
                });
            };

            $scope.openProductDelete = function (product) {
                var modalInstance = $modal.open({
                    templateUrl: SETTINGS.uris.static + '/price_monitor/app/partials/product-delete.html',
                    controller: 'ProductDeleteCtrl',
                    resolve: {
                        product: function () {
                            return product;
                        }
                    }
                });

                modalInstance.result.then(function () {
                    $scope.products = Product.query();
                });
            };

            $scope.openEmailNotificationCreate = function() {
                var modalInstance = $modal.open({
                    templateUrl: SETTINGS.uris.static + '/price_monitor/app/partials/emailnotification-create.html',
                    controller: 'EmailNotificationCreateCtrl'
                });

                modalInstance.result.then(function () {
                    $scope.emailNotifications = EmailNotification.query();
                });
            };
        });
    });
});
