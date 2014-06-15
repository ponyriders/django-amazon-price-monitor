from price_monitor.api.serializers.EmailNotificationSerializer import EmailNotificationSerializer
from price_monitor.models.EmailNotification import EmailNotification

from rest_framework import generics, permissions


class EmailNotificationListView(generics.ListAPIView):
    model = EmailNotification
    serializer_class = EmailNotificationSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        return super(EmailNotificationListView, self).get_queryset().filter(owner=self.request.user)
