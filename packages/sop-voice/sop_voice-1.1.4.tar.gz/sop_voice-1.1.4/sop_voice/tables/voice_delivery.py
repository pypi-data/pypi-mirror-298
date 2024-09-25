import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable, ChoiceFieldColumn

from sop_utils.utils import *

from ..models import VoiceDelivery


__all__ = (
    'VoiceDeliveryTable',
)

class VoiceDeliveryTable(NetBoxTable):
    '''
    table for all Voice Deliveries
    '''
    delivery = tables.Column(verbose_name=_('Delivery Method'), linkify=True)
    provider = tables.Column(verbose_name=_('Provider'), linkify=True)
    site = tables.Column(verbose_name=_('Site'), linkify=True)
    channel_count = tables.Column(verbose_name=_('Channel Count'), linkify=True)
    status = ChoiceFieldColumn(linkify=True)
    ndi = tables.Column(verbose_name=_('MBN / NDI'), linkify=True)
    dto = tables.Column(verbose_name=_('DTO'), linkify=True)

    class Meta(NetBoxTable.Meta):
        model = VoiceDelivery
        fields = ('pk', 'id', 'actions', 'delivery', 'provider', 'site',
            'channel_count', 'status', 'ndi', 'dto')
        default_columns = ('actions', 'delivery', 'provider', 'status', 'channel_count')
