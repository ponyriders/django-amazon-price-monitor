from django.forms.models import BaseModelFormSet

from .models.EmailNotification import EmailNotification


class SubscriptionModelFormset(BaseModelFormSet):
    """
    Formset helper class for custom filtering operations on form fields
    """

    def __init__(self, user, *args, **kwargs):
        """
        Overwritten init method to filter email notifications so a user only
        sees his own objects
        """
        super(SubscriptionModelFormset, self).__init__(*args, **kwargs)
        self.user = user
        notifications = EmailNotification.objects.filter(owner=self.user)

        for form in self.forms:
            form.fields['email_notification'].queryset = notifications


class EmailNotificationFormset(BaseModelFormSet):
    """
    Formset class needed for views. Does nothing specific
    """
    pass
