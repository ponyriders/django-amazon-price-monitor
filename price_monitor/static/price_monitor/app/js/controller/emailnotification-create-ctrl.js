PriceMonitorApp.controller('EmailNotificationCreateCtrl', function ($scope, $modalInstance, EmailNotification) {
    $scope.email_notification = {};

    $scope.ok = function (email_notification) {
        EmailNotification.save(email_notification, function() {
            $modalInstance.close();
        });
    };
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});
