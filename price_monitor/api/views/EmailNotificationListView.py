"""View for listing email notifications"""
from ..serializers.EmailNotificationSerializer import EmailNotificationSerializer
from ...models.EmailNotification import EmailNotification

from rest_framework import generics, mixins, permissions


class EmailNotificationListView(mixins.CreateModelMixin, generics.ListAPIView):

    """View for rendering list of EmailNotification objects"""

    model = EmailNotification
    serializer_class = EmailNotificationSerializer
    permission_classes = [
        # only return the list if user is authenticated
        permissions.IsAuthenticated
    ]

    def post(self, request, *args, **kwargs):
        """
        Add post method to create object

        :param request: the request
        :type request:  HttpRequest
        :return:        Result of creation
        :rtype:         HttpResponse
        """
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        """
        Filters queryset by the authenticated user

        :returns: filtered EmailNotification objects
        :rtype:   QuerySet
        """
        return self.model.objects.filter(owner=self.request.user)
