from price_monitor.api.serializers.EmailNotificationSerializer import EmailNotificationSerializer
from price_monitor.models.EmailNotification import EmailNotification

from rest_framework import generics, permissions


class EmailNotificationListView(generics.ListAPIView):
    """
    View for rendering list of EmailNotification objects
    """
    
    model = EmailNotification
    serializer_class = EmailNotificationSerializer
    permission_classes = [
        # only return the list if user is authenticated
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        """
        Filters queryset by the authenticated user
        :returns: filtered EmailNotification objects
        :rtype:   QuerySet
        """
        return super(EmailNotificationListView, self).get_queryset().filter(owner=self.request.user)
