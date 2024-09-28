from netbox.api.viewsets import NetBoxModelViewSet
from netbox.api.metadata import ContentTypeMetadata

from ..models import *
from ..filtersets import *
from .serializers import *


__all__ = (
    'VoiceDeliveryViewSet',
    'VoiceSdaViewSet',
    'SiteVoiceInfoViewSet',
    'VoiceMaintainerViewSet',
)

class VoiceMaintainerViewSet(NetBoxModelViewSet):
    metadata_class = ContentTypeMetadata
    queryset = VoiceMaintainer.objects.all()
    serializer_class = VoiceMaintainerSerializer
    filterset_class = VoiceMaintainerFilterSet


class SiteVoiceInfoViewSet(NetBoxModelViewSet):
    metadata_class = ContentTypeMetadata
    queryset = SiteVoiceInfo.objects.all()
    serializer_class = SiteVoiceInfoSerializer
    filterset_class = SiteVoiceInfoFilterSet


class VoiceSdaViewSet(NetBoxModelViewSet):
    metadata_class = ContentTypeMetadata
    queryset = VoiceSda.objects.all()
    serializer_class = VoiceSdaSerializer
    filterset_class = VoiceSdaFilterSet


class VoiceDeliveryViewSet(NetBoxModelViewSet):
    metadata_class = ContentTypeMetadata
    queryset = VoiceDelivery.objects.all()
    serializer_class = VoiceDeliverySerializer
    filterset_class = VoiceDeliveryFilterSet
