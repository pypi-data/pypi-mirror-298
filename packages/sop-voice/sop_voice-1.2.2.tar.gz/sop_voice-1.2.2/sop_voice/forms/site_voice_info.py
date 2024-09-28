from django import forms
from django.utils.translation import gettext_lazy as _

from dcim.models import Site

from ..models import SiteVoiceInfo, VoiceMaintainer


__all__ = (
    'SiteVoiceInfoForm',
)


class SiteVoiceInfoForm(forms.ModelForm):
    '''
    creates a form for a Site Voice Info object
    '''
    maintainer = forms.ModelChoiceField(
        queryset=VoiceMaintainer.objects.all(),
        label=_('Voice Maintainer'),
        help_text=_('The voice maintainer of the site.'),
        required=True,
    )
    site = forms.ModelChoiceField(
        queryset=Site.objects.all(),
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = SiteVoiceInfo
        fields = ('maintainer', )
