import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable
from ..models import VoiceSda


__all__ = (
    'VoiceSdaTable',
)


class VoiceSdaTable(NetBoxTable):
    '''
    table for all SDA List
    '''
    delivery = tables.Column(verbose_name=_('Delivery'), linkify=True)
    start = tables.Column(verbose_name=_('Start number'), linkify=True)
    end = tables.Column(verbose_name=_('End number'), linkify=True)

    class Meta(NetBoxTable.Meta):
        model = VoiceSda
        fields = ('actions', 'pk', 'id', 'delivery', 'start', 'end')
        default_columns = ('delivery', 'start', 'end')
