from django.db.models import Prefetch
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from netbox.api.fields import ChoiceField
from netbox.api.serializers import NetBoxModelSerializer
from dcim.api.serializers import SiteSerializer
from circuits.api.serializers import ProviderSerializer
from dcim.models import Site

from ..models import *


__all__ = (
    'VoiceDeliverySerializer',
    'VoiceSdaSerializer',
    'SiteVoiceInfoSerializer',
    'VoiceMaintainerSerializer',
)


# Briefs Serializers
# -> | for addditional infos
#    | without modifying original


class SiteBriefSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='dcim-api:site-detail')
    
    class Meta:
        model = Site
        fields = ('id', 'url', 'slug', 'name', 'description')


#_______________________________
# Voice Maintainer


class VoiceMaintainerSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:sop_voice-api:voicemaintainer-detail'
    )
    status = ChoiceField(
        choices=VoiceMaintainerStatusChoice
    )
    site = serializers.SerializerMethodField()

    class Meta:
        model = VoiceMaintainer
        fields = (
            'id', 'url', 'slug', 'display', 'name', 'status', 'description', 'created', 'last_updated',
            'site',
        )
        brief_fields = ('id', 'url', 'slug', 'name', 'description')

    def get_site(self, obj):
        site_voice_infos = SiteVoiceInfo.objects.filter(maintainer=obj).prefetch_related(
            Prefetch('site', queryset=Site.objects.all())
        )
        site = [svi.site for svi in site_voice_infos if svi.site]
        return SiteBriefSerializer(site, many=True, context=self.context).data


#_______________________________
# Site Voice Info (Informations)


class SiteVoiceInfoSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:sop_voice-api:sitevoiceinfo-detail'
    )
    site = serializers.SerializerMethodField()
    maintainer = serializers.SerializerMethodField()

    class Meta:
        model = SiteVoiceInfo
        fields = ('id', 'url', 'display', 'site', 'maintainer')

    def get_site(self, obj):
        if not obj.site:
            return None
        return SiteSerializer(obj.site, nested=True, many=False, context=self.context).data

    def get_maintainer(self, obj):
        if not obj.maintainer:
            return None
        maintainer_id = VoiceMaintainer.objects.filter(pk=obj.maintainer.id)
        return VoiceMaintainerSerializer(maintainer_id, nested=True, many=True, context=self.context).data


#_______________________________
# Voice Sda (DIDs)


class VoiceSdaSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:sop_voice-api:voicesda-detail'
    )
    delivery = serializers.SerializerMethodField(read_only=True)
    site = serializers.SerializerMethodField()

    class Meta:
        model = VoiceSda
        fields = ('id', 'url', 'site', 'delivery', 'start', 'end')

    def get_site(self, obj):
        if not obj.site:
            return None
        return SiteSerializer(obj.site, nested=True, many=False, context=self.context).data

    def get_delivery(self, obj):
        if not obj.delivery:
            return None
        deliv = VoiceDelivery.objects.filter(pk=obj.delivery.id)
        return VoiceDeliverySerializer(deliv, nested=True, many=True, context=self.context).data


#_______________________________
# Voice Delivery


class VoiceDeliverySerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:sop_voice-api:voicedelivery-detail'
    )
    provider = serializers.SerializerMethodField()
    site = serializers.SerializerMethodField()

    class Meta:
        model = VoiceDelivery
        fields = ('id', 'url', 'display', 'site', 'delivery', 'provider',
            'channel_count', 'status',
        )
        brief_fields = ('id', 'url', 'display', 'provider', 'delivery',)

    def get_provider(self, obj):
        if not obj.provider:
            return None
        return ProviderSerializer(obj.provider, nested=True, many=False, context=self.context).data


    def get_site(self, obj):
        if not obj.site:
            return None
        return SiteSerializer(obj.site, nested=True, many=False, context=self.context).data
