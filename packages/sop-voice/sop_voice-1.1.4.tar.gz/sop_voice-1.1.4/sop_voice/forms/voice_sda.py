from django import forms
from django.utils.translation import gettext_lazy as _

from netbox.forms import NetBoxModelFilterSetForm
from utilities.forms.fields import DynamicModelChoiceField
from dcim.models import Site

from ..models import *


__all__ = (
    'VoiceSdaForm',
    'VoiceSdaImportForm',
    'VoiceSdaFilterForm',
    'VoiceSdaBulkEditForm'
)


class VoiceSdaBulkEditForm(forms.ModelForm):
    delivery = forms.ModelChoiceField(
        queryset=VoiceDelivery.objects.all()
    )

    class Meta:
        model = VoiceSda
        fields = ('delivery', )


class VoiceSdaFilterForm(NetBoxModelFilterSetForm):
    model = VoiceSda
    
    site_id = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label=_('Site')
    )
    maintainer_id = forms.ModelChoiceField(
        queryset=VoiceMaintainer.objects.all(),
        required=False,
        label=_('Maintainer')
    )
    delivery_id = forms.ModelChoiceField(
        queryset=VoiceDelivery.objects.all(),
        required=False,
        label=_('Delivery')
    )
    start = forms.CharField(
        label=_('Start number'),
        required=False
    )
    end = forms.CharField(
        label=_('End number'),
        required=False
    )


class VoiceSdaForm(forms.ModelForm):
    ''''
    creates a form for a SDA List instance
    '''
    start = forms.CharField(
        label=_('Start number'),
        required=True,
        help_text=_('E164 format'),
    )
    end = forms.CharField(
        label=_('End number'),
        required=False,
        help_text=_('E164 format - can be left blank if the range is only one number.'),
    )
    delivery = forms.ModelChoiceField(
        label=_('Delivery'),
        queryset=VoiceDelivery.objects.all(),
        required=True,
        help_text=_('Specify how this range is delivered.'),
    )

    class Meta:
        model = VoiceSda
        fields = ('start', 'end', 'delivery', )


class VoiceSdaImportForm(forms.ModelForm):
    '''
    creates a form for importing a list of SDA List objects
    '''
    json_import = forms.JSONField(
        label=_('JSON'),
        help_text=('\
Enter the SDA List range number in a JSON format.\
[\
    "start >> end",\
    "start >> end",\
]'),
        required=True,
    )
    delivery = forms.ModelChoiceField(
        label=_('Delivery'),
        queryset=VoiceDelivery.objects.all(),
        required=True,
        help_text=_('The voice delivery the voice number range is assigned to.'),
    )

    class Meta:
        model = VoiceSda
        fields = ('json_import', 'delivery', )
