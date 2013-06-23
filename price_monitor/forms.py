import re

from . import app_settings as settings

from django import forms
from django.utils.translation import ugettext as _


class MultiASINForm(forms.Form):
    asins = forms.CharField(
        label=_('ASINs'),
        widget=forms.Textarea(
            attrs={'rows': 1}
        )
    )

    def clean(self):
        """
        Validates, that field asins to comma separated ASINs
        """
        cleaned_data = super(MultiASINForm, self).clean()
        asins = cleaned_data.get('asins')
        for asin_separator in settings.ASIN_SEPARATORS:
            if re.match('([a-zA-Z0-9]+\\' + asin_separator + ' )*[a-zA-Z0-9]+', asins):
                return cleaned_data
        raise forms.ValidationError(_('Not a valid ASIN list'))


