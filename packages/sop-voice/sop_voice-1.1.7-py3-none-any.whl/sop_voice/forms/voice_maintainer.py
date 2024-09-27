from django import forms
from django.utils.translation import gettext_lazy as _

from utilities.forms.fields import CommentField, SlugField

from netbox.forms import NetBoxModelFilterSetForm, NetBoxModelForm, NetBoxModelBulkEditForm

from ..models import *


__all__ = (
    'VoiceMaintainerForm',
    'VoiceMaintainerFilterForm',
    'VoiceMaintainerBulkEditForm',
)


class VoiceMaintainerFilterForm(NetBoxModelFilterSetForm):
    model = VoiceMaintainer
    status = forms.ChoiceField(
        choices=VoiceMaintainerStatusChoice,
        required=False,
        label=_('Status'),
    )


class VoiceMaintainerBulkEditForm(NetBoxModelBulkEditForm):
    model = VoiceMaintainer
    status = forms.ChoiceField(
        choices=VoiceMaintainerStatusChoice,
        required=True,
    )

    class Meta:
        fields = ('status', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'add_tags' in self.fields:
            del self.fields['add_tags']
        if 'remove_tags' in self.fields:
            del self.fields['remove_tags']


class VoiceMaintainerForm(NetBoxModelForm):
    name = forms.CharField(label=_('Maintainer'))
    slug = SlugField()
    status = forms.ChoiceField(
        choices=VoiceMaintainerStatusChoice,
        required=True
    )
    comments = CommentField()

    class Meta:
        model = VoiceMaintainer
        fields = ('name', 'slug', 'status', 'description', 'comments')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'tags' in self.fields:
            del self.fields['tags']
