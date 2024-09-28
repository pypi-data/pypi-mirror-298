import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from netbox.tables import NetBoxTable, ChoiceFieldColumn

from ..models import VoiceMaintainer


__all__ = (
    'VoiceMaintainerTable',
)

class VoiceMaintainerTable(NetBoxTable):
    '''
    table for all Voice Deliveries
    '''
    name = tables.Column(
        verbose_name=_('Name'), linkify=True
    )
    status = ChoiceFieldColumn(
        linkify=True
    )
    description = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = VoiceMaintainer
        fields = ('pk', 'id', 'actions', 'name', 'status', 'description', 'comments', )
        default_columns = ('name', 'status', 'description',)
