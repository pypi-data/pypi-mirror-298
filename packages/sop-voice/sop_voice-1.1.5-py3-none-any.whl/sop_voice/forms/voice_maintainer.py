from django import forms
from django.utils.translation import gettext_lazy as _

from utilities.forms.fields import CommentField

from sop_utils.models import VoiceMaintainerStatusChoice
from netbox.forms import NetBoxModelFilterSetForm

from ..models import VoiceMaintainer


__all__ = (
    'VoiceMaintainerForm',
    'VoiceMaintainerImportForm',
    'VoiceMaintainerFilterForm'
)


class VoiceMaintainerFilterForm(NetBoxModelFilterSetForm):
    model = VoiceMaintainer
    status = forms.ChoiceField(
        choices=VoiceMaintainerStatusChoice,
        required=False,
        label=_('Status'),
    )


class VoiceMaintainerForm(forms.ModelForm):
    name = forms.CharField(label=_('Maintainer'))
    status = forms.ChoiceField(
        choices=VoiceMaintainerStatusChoice,
        required=True
    )
    comments = CommentField()

    class Meta:
        model = VoiceMaintainer
        fields = ('name', 'status', 'description', 'comments')


class VoiceMaintainerImportForm(forms.ModelForm):
    json_import = forms.JSONField(
        label=_('JSON'),
        help_text=('\
Enter the SDA List range number in a JSON format.\
[\
    "Quonex",\
    "Alcatel"\
]'),
        required=True
    )
    status = forms.ChoiceField(
        choices=VoiceMaintainerStatusChoice,
        required=True
    )
    comments = CommentField()

    class Meta:
        model = VoiceMaintainer
        fields = ('json_import', 'status', 'description', 'comments')
